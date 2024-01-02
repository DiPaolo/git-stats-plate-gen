import datetime
import enum
import getpass
import os.path
import uuid
from dataclasses import dataclass
from typing import Optional, Dict, Tuple, List

from PySide6 import QtCore
from PySide6.QtCore import Slot, Signal, QTimer, QThread, QStandardPaths
from PySide6.QtWidgets import QDialog, QFileDialog, QMessageBox

from git_stats_plate_gen import __version__
from git_stats_plate_gen.config import config
from git_stats_plate_gen.core import cache, utils
from git_stats_plate_gen.core.common import DataType, get_data_type_name, get_output_image_filename
from git_stats_plate_gen.gui import logger, settings
from git_stats_plate_gen.gui.log_window import LogWindow
from git_stats_plate_gen.gui.settings import SettingsKey
from git_stats_plate_gen.gui.thread_worker import ThreadWorker
from git_stats_plate_gen.gui.ui.ui_main_dialog import Ui_Dialog


class MainDialog(QDialog):
    @dataclass
    class UserMessageId(object):
        _uuid = uuid.uuid4()

        def __eq__(self, other):
            return self._uuid == other._uuid

    class UserMessage(enum.Enum):
        INFO = 0
        WARNING = 1
        ERROR = 2

    started = Signal()
    stopped = Signal()
    _stats_changed = Signal()

    _stats: Optional[Dict] = None
    _stats_datetime_utc: Optional[datetime.datetime] = None

    _thread = None
    _worker = None
    _timer = None

    _user_messages: List[Tuple[UserMessageId, UserMessage, str]]

    def __init__(self):
        super(MainDialog, self).__init__()

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self._user_messages = list()

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

        self.ui.username.textChanged.connect(lambda text: settings.set_settings_str_value(SettingsKey.USERNAME, text))

        self._stats_changed.connect(self._update_cur_stats_status)
        self._stats_changed.connect(self._replot_graph)
        self._stats_changed.connect(self._update_save_image_related_controls)

        self.ui.splitter.splitterMoved.connect(lambda x: self._replot_graph())

        [elem.textChanged.connect(self._update_start_stop_status) for elem in [
            self.ui.username, self.ui.token
        ]]

        self.ui.min_percent.valueChanged.connect(self._replot_graph)
        self.ui.min_percent.valueChanged.connect(
            lambda value: settings.set_settings_float_value(SettingsKey.MIN_PERCENT, value))

        self.ui.output_folder.textChanged.connect(self._update_full_image_file_path)
        self.ui.output_folder.textChanged.connect(self._check_access_to_output_folder)
        self.ui.output_folder.textChanged.connect(self._update_save_image_related_controls)
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
        stats_datetime_utc, stats = cache.load_stats()
        self._set_stats(stats_datetime_utc, stats)
        # after stats is set to correctly enable/disable some controls
        self._init_controls()

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
        #
        # left part
        #

        username = settings.get_settings_str_value(SettingsKey.USERNAME, getpass.getuser())
        self.ui.username.setText(username)

        #
        # right part
        #

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
            f"Copyright 2023-2024 {__version__.__author__} "
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

        out_filename = get_output_image_filename(utils.convert_datetime_utc_to_local(self._stats_datetime_utc),
                                                 self.ui.image_filename_template.text())
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

    @Slot()
    def _update_full_image_file_path(self):
        if self._is_data_ready():
            self.ui.full_image_file_path.setText(
                os.path.join(self.ui.output_folder.text(),
                             get_output_image_filename(utils.convert_datetime_utc_to_local(self._stats_datetime_utc)),
                             self.ui.image_filename_template.text()))
        else:
            full_filename = os.path.join(self.ui.output_folder.text(),
                                         get_output_image_filename(datetime.datetime.now(),
                                                                   self.ui.image_filename_template.text()))
            self.ui.full_image_file_path.setText(f'{full_filename} (example)')

    @Slot()
    def _check_access_to_output_folder(self):
        if not self._has_access_to_output_folder():
            self._check_access_to_output_folder_user_msg_id = (
                self._add_user_message(self.UserMessage.WARNING,
                                       'You have no write access to the output folder'))
        else:
            try:
                self._remove_user_message(self._check_access_to_output_folder_user_msg_id)
            except AttributeError:
                pass

    def _has_access_to_output_folder(self) -> bool:
        return os.access(self.ui.output_folder.text(), os.W_OK)

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

        self.ui.preview.set_data(self._stats, self.ui.min_percent.value())

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

        # additional requirement for save image button
        if not self._has_access_to_output_folder():
            self.ui.save_image.setEnabled(False)

    def _add_user_message(self, msg_type: UserMessage, msg: str) -> UserMessageId:
        user_msg_id = self.UserMessageId()
        self._user_messages.append((user_msg_id, msg_type, msg))
        self._update_user_message()
        return user_msg_id

    def _remove_user_message(self, user_msg_id: UserMessageId):
        self._user_messages = list(filter(lambda item: item[0] != user_msg_id, self._user_messages))
        self._update_user_message()

    def _update_user_message(self):
        if len(self._user_messages) == 0:
            self.ui.user_message.clear()
            return

        prefix = ''
        color = 'gray'

        (msg_id, msg_type, msg) = self._user_messages[-1]

        if msg_type == self.UserMessage.INFO:
            prefix = 'INFO: '
        elif msg_type == self.UserMessage.WARNING:
            prefix = 'WARNING: '
            color = 'orange'
        elif msg_type == self.UserMessage.ERROR:
            prefix = 'ERROR: '
            color = 'tomato'
        else:
            logger.error(f'Unhandled user message type (type={msg_type}, msg={msg})')

        style_begin = f"<p style='color:{color};'>" if color else ''
        style_end = '</p>' if color else ''

        self.ui.user_message.setText(f"{style_begin}{prefix}{msg}{style_end}")
