import datetime
import getpass
import os.path
import pprint
from typing import Optional, Dict

from PySide6 import QtCore
from PySide6.QtCore import Slot, Signal, QTimer, QThread, QStandardPaths
from PySide6.QtWidgets import QDialog, QFileDialog, QMessageBox

from git_stats_plate_gen import __version__
from git_stats_plate_gen.config import config
from git_stats_plate_gen.core import cache, utils
from git_stats_plate_gen.core.common import DataType, get_data_type_name
from git_stats_plate_gen.core.graph import plot_graph_to_buffer
from git_stats_plate_gen.gui import logger, settings
from git_stats_plate_gen.gui.log_window import LogWindow
from git_stats_plate_gen.gui.settings import SettingsKey
from git_stats_plate_gen.gui.thread_worker import ThreadWorker
from git_stats_plate_gen.gui.ui.ui_main_dialog import Ui_Dialog


def replace_output_image_filename_template(template: str, dt: datetime.datetime) -> str:
    allowed_directives = [
        ('Y', f'{dt.year:04}'),
        ('m', f'{dt.month:02}'),
        ('d', f'{dt.day:02}'),
        ('H', f'{dt.hour:02}'),
        ('M', f'{dt.minute:02}'),
        ('S', f'{dt.second:02}')
    ]

    out_str = template
    for item in allowed_directives:
        d = item[0]
        value = item[1]
        out_str = out_str.replace(f'%{d}', str(value))

    return out_str


class MainDialog(QDialog):
    started = Signal()
    stopped = Signal()
    _stats_changed = Signal()

    _stats: Optional[Dict] = None
    _stats_datetime_utc: Optional[datetime.datetime] = None

    _thread = None
    _worker = None
    _timer = None

    def __init__(self):
        super(MainDialog, self).__init__()

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.setWindowTitle(f'{config.application_name} {config.app_version.as_str(2)}')

        self.log_window = LogWindow(self)
        # self.log_window.visibility_changed.connect(self.ui.show_log_window.setChecked)
        # self.log_window.show()

        logger.info('Application starting...')

        # restore position and state
        self.setWindowState(settings.get_settings_byte_array_value(SettingsKey.WINDOW_STATE, QtCore.Qt.WindowNoState))
        self.restoreGeometry(settings.get_settings_byte_array_value(SettingsKey.WINDOW_GEOMETRY))
        self.ui.splitter.restoreState(settings.get_settings_byte_array_value(SettingsKey.SPLITTER_STATE))

        #
        # connections
        #

        # # log window
        # self.ui.show_log_window.toggled.connect(lambda checked: self.log_window.setVisible(checked))
        # self.ui.show_log_window.setChecked(True)

        self._stats_changed.connect(self._update_cur_stats_status)
        self._stats_changed.connect(self._replot_graph)
        self._stats_changed.connect(self._update_save_image_related_controls)

        self.ui.splitter.splitterMoved.connect(lambda x: self._replot_graph())

        [elem.textChanged.connect(self._update_start_stop_status) for elem in [
            self.ui.username, self.ui.token
        ]]

        self.ui.min_percent.valueChanged.connect(self._replot_graph)

        self.ui.output_folder.textChanged.connect(self._update_full_image_file_path)
        self.ui.image_filename_template.textChanged.connect(self._update_full_image_file_path)

        # start/stop + exit
        self.ui.start_stop.clicked.connect(self._start_collect)

        # controls for saving image
        self.ui.choose_out_image_dir.clicked.connect(self._choose_out_image_dir)
        self.ui.save_image.clicked.connect(self._save_image)

        #
        # initialization of controls
        #

        # after connections!
        self._init_controls()
        stats_datetime_utc, stats = cache.load_stats()
        self._set_stats(stats_datetime_utc, stats)

        # change preview size to new size
        QTimer.singleShot(0, lambda: self._replot_graph())

        self.ui.token.setFocus()

    def closeEvent(self, event):
        logger.info('Exiting application...')

        self._cancel_collect()

        # save window position and size
        settings.set_settings_byte_array_value(SettingsKey.WINDOW_GEOMETRY, self.saveGeometry())
        settings.set_settings_byte_array_value(SettingsKey.WINDOW_STATE, self.windowState())
        settings.set_settings_byte_array_value(SettingsKey.SPLITTER_STATE, self.ui.splitter.saveState())

        event.accept()

    def resizeEvent(self, event):
        self._replot_graph()
        event.accept()

    def _set_stats(self, stats_datetime_utc: Optional[datetime.datetime], stats: Optional[Dict]):
        self._stats = stats
        self._stats_datetime_utc = stats_datetime_utc

        self._stats_changed.emit()

    def _init_controls(self):
        username = settings.get_settings_str_value(SettingsKey.USERNAME, getpass.getuser())
        self.ui.username.setText(username)

        out_image_path = settings.get_settings_str_value(SettingsKey.OUT_IMAGE_PATH, config.defaults.out_image_path)
        abs_out_image_path = os.path.abspath(out_image_path)
        self.ui.output_folder.setText(abs_out_image_path)

        out_image_name = settings.get_settings_str_value(SettingsKey.OUT_IMAGE_BASE_NAME,
                                                         config.defaults.out_image_base_name)
        self.ui.image_filename_template.setText(out_image_name)

        min_percent = settings.get_settings_float_value(SettingsKey.MIN_PERCENT, config.defaults.min_percent)
        self.ui.min_percent.setValue(min_percent)

        self._init_about_program()

    def _init_about_program(self):
        self.ui.program_name_n_version.setText(
            f'<p style="color:gray;">'
            f'{config.application_name} {config.app_version.as_str(4)}'
            f'</p>'
        )

        self.ui.copyright.setText(
            f"<p style='color:gray;'>"
            f"Copyright 2023 {__version__.__author__} "
            f"(<a href='mailto:{__version__.__author_email__}'>{__version__.__author_email__}</a>)"
            f"</p>"
        )

    def _update_start_stop_status(self):
        elems = [self.ui.username, self.ui.token]
        filled_elem_count = list(filter(lambda elem: len(elem.text()) > 0, elems))
        self.ui.start_stop.setEnabled(len(filled_elem_count) == len(elems))

    def _choose_out_image_dir(self):
        cur_out_image_folder = self.ui.output_folder.text()
        out_image_folder = cur_out_image_folder if cur_out_image_folder else QStandardPaths.standardLocations(
            QStandardPaths.StandardLocation.HomeLocation)[0]
        selected_folder = QFileDialog.getExistingDirectory(self, 'Choose Output Folder', out_image_folder)
        if not selected_folder:
            return

        self.ui.output_folder.setText(selected_folder)
        settings.set_settings_str_value(SettingsKey.OUT_IMAGE_PATH, selected_folder)

    def _save_image(self):
        if not self._is_data_ready():
            msg = "Failed to save image: stats data is not ready"
            logger.error(msg)
            QMessageBox.critical(self, "Save Image", msg, QMessageBox.StandardButton.Close)
            return

        out_image_folder = self.ui.output_folder.text()
        if not os.path.exists(out_image_folder) or not os.path.isdir(out_image_folder):
            msg = f"Failed to save image: output folder ({out_image_folder}) doesn't exist or not a folder"
            logger.error(msg)
            QMessageBox.critical(self, "Save Image", msg, QMessageBox.StandardButton.Close)
            return

        out_filename = self._get_output_image_filename(utils.convert_datetime_utc_to_local(self._stats_datetime_utc))
        if not out_filename:
            msg = "Failed to save image: output filename is invalid"
            logger.error(msg)
            QMessageBox.critical(self, "Save Image", msg, QMessageBox.StandardButton.Close)
            return

        full_filename = os.path.join(out_image_folder, out_filename)
        ret = self.ui.preview.save_image(full_filename)
        if not ret:
            msg = "Failed to save image"
            logger.error(msg)
            QMessageBox.critical(self, "Save Image", msg, QMessageBox.StandardButton.Close)
            return

        msg = f"Image saved as {full_filename}"
        logger.info(msg)
        QMessageBox.information(self, "Save Image", msg, QMessageBox.StandardButton.Close)

    def _update_full_image_file_path(self):
        if self._stats and self._stats_datetime_utc:
            self.ui.full_image_file_path.setText(
                os.path.join(self.ui.output_folder.text(), self._get_output_image_filename(
                    utils.convert_datetime_utc_to_local(self._stats_datetime_utc))))
        else:
            full_filename = os.path.join(self.ui.output_folder.text(),
                                         self._get_output_image_filename(datetime.datetime.now()))
            self.ui.full_image_file_path.setText(f'{full_filename} (example)')

    def _get_output_image_filename(self, dt: datetime.datetime) -> str:
        return replace_output_image_filename_template(self.ui.image_filename_template.text(), dt)

    @Slot()
    def _start_collect(self):
        self._cancel_collect()

        logger.info('Start collecting statistics...')

        self._set_stats(None, None)

        self._set_all_controls_enabled(False)

        self.started_time = datetime.datetime.now()
        self.started.emit()

        self.ui.start_stop.setText('Cancel')
        self.ui.start_stop.clicked.disconnect()
        self.ui.start_stop.clicked.connect(self._cancel_collect)

        self._thread = QThread()
        self._worker = ThreadWorker(self.ui.username.text(), self.ui.token.text())
        self._worker.moveToThread(self._thread)
        self._worker.started.connect(self.started)
        self._worker.finished.connect(self._stop_collect)

        self._thread.started.connect(self._worker.run)
        self._worker.progress.connect(self.ui.progress_bar.setValue)

        self._thread.start()

        self._timer = QTimer()
        self._timer.timeout.connect(self._update_cur_stats_info)
        self._timer.start(1000)

        logger.info('Collect started')

    @Slot()
    def _cancel_collect(self):
        self._stop_collect(False)

    @Slot()
    def _stop_collect(self, done: bool = True):
        """

        :param done: done/finished if True; canceled if False
        :return:
        """

        logger.info(f"{'Finishing' if done else 'Stopping'} collecting statistics...")

        if self._timer:
            self._timer.stop()
            self._timer = None

        if self._worker:
            # use it as the current stats if done + update cache
            if done:
                self._set_stats(datetime.datetime.utcnow(), self._worker.cur_stats)
                cache.save_stats(self._stats_datetime_utc, self._stats)
                self._update_cur_stats_info()

            self._worker.stop()
            # self._worker = None

        if self._thread:
            self._thread.quit()
            self._thread.wait()
            self._thread = None

        self.started_time = None
        self._set_all_controls_enabled(True)
        self.stopped.emit()

        self.ui.start_stop.setText('Collect Statistics')
        self.ui.start_stop.clicked.disconnect()
        self.ui.start_stop.clicked.connect(self._start_collect)

        logger.info(f"Collecting {'done' if done else 'canceled'}")

    def _is_collecting(self) -> bool:
        return self._thread is not None and self._thread.isRunning()

    def _set_all_controls_enabled(self, enabled: bool = True):
        [elem.setEnabled(enabled) for elem in [
            self.ui.username, self.ui.token, self.ui.image_filename_template, self.ui.choose_out_image_dir
        ]]

        self._update_save_image_related_controls()

    def _replot_graph(self):
        if not self._is_data_ready():
            # clear the image
            self.ui.preview.set_data(None)
            return

        size = self.ui.preview.size()
        plot_data = plot_graph_to_buffer(self._stats, min_percent=self.ui.min_percent.value(),
                                         width=size.width(), height=size.height())
        self.ui.preview.set_data(plot_data)

    def _is_data_ready(self) -> bool:
        return bool(self._stats and self._stats_datetime_utc)

    @Slot()
    def _update_cur_stats_status(self):
        if self._is_data_ready():
            local_datetime = utils.convert_datetime_utc_to_local(self._stats_datetime_utc)
            gen_datetime_str = local_datetime.strftime('%Y-%m-%d, %H:%M:%S')
            self.ui.stats_status.setText(f'<p style="color:green;">Statistics Ready (gen. {gen_datetime_str})</p')
        else:
            self.ui.stats_status.setText('<p style="color:tomato;">Statistics Not Ready</p')

    @Slot()
    def _update_cur_stats_info(self):
        if not self._worker:
            return

        cur_stats = self._worker.cur_stats

        param_name = get_data_type_name(DataType.LINES)
        lang_stats_lines = list(
            filter(lambda x: x, [(k, v[param_name]) if param_name in v else None for k, v in cur_stats.items()])
        )
        sorted_lang_stats_lines = sorted(lang_stats_lines, key=lambda x: x[1], reverse=True)

        text = f'{self._worker.processed} / {self._worker.total} repos\n'
        text += '\n'
        text += '\n'.join([f'{v[0]}: {v[1]} LOC' for v in sorted_lang_stats_lines])

        self.ui.debug.setText(text)

    @Slot()
    def _update_save_image_related_controls(self):
        [elem.setEnabled(self._is_data_ready() and not self._is_collecting()) for elem in [
            self.ui.min_percent,
            self.ui.save_image,
        ]]
