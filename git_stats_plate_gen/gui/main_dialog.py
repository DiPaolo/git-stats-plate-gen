import datetime
import getpass

from PySide6 import QtCore
from PySide6.QtCore import Slot, Signal, QTimer, QThread
from PySide6.QtWidgets import QDialog

from git_stats_plate_gen import config
from git_stats_plate_gen.core.cache import load_stats
from git_stats_plate_gen.core.common import DataType, get_data_type_name
from git_stats_plate_gen.core.graph import plot_graph_to_buffer
from git_stats_plate_gen.gui import logger, settings
from git_stats_plate_gen.gui.log_window import LogWindow
from git_stats_plate_gen.gui.settings import SettingsKey
from git_stats_plate_gen.gui.thread_worker import ThreadWorker
from git_stats_plate_gen.gui.ui.ui_main_dialog import Ui_Dialog


class MainDialog(QDialog):
    started = Signal()
    stopped = Signal()

    _thread = None
    _worker = None
    _timer = None

    def __init__(self):
        super(MainDialog, self).__init__()

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.setWindowTitle(config.APPLICATION_NAME)

        self.log_window = LogWindow(self)
        # self.log_window.visibility_changed.connect(self.ui.show_log_window.setChecked)
        # self.log_window.show()

        logger.info('Application starting...')

        # restore position and state
        self.setWindowState(settings.get_settings_byte_array_value(SettingsKey.WINDOW_STATE, QtCore.Qt.WindowNoState))
        self.restoreGeometry(settings.get_settings_byte_array_value(SettingsKey.WINDOW_GEOMETRY))
        self.ui.splitter.restoreState(settings.get_settings_byte_array_value(SettingsKey.SPLITTER_STATE))

        self._stats = load_stats()
        self._update_cur_stats_status()
        self._replot_graph()

        #
        # connections
        #

        # # log window
        # self.ui.show_log_window.toggled.connect(lambda checked: self.log_window.setVisible(checked))
        # self.ui.show_log_window.setChecked(True)

        self.ui.splitter.splitterMoved.connect(lambda x: self._replot_graph())

        [elem.textChanged.connect(self._update_start_stop_status) for elem in [
            self.ui.username, self.ui.token, self.ui.output_base_name
        ]]

        self.ui.min_percent.valueChanged.connect(self._replot_graph)

        # start/stop + exit
        self.ui.start_stop.clicked.connect(self._start_collect)

        # after connections!
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

    def _init_controls(self):
        self.ui.username.setText(settings.get_settings_str_value(SettingsKey.USERNAME, getpass.getuser()))
        self.ui.output_base_name.setText(settings.get_settings_str_value(SettingsKey.OUT_IMAGE_BASE_NAME,
                                                                         config.DEFAULT_OUT_IMAGE_BASE_NAME))
        self.ui.use_cache.setChecked(settings.get_settings_bool_value(SettingsKey.USE_CACHE, config.DEFAULT_USE_CACHE))
        self.ui.min_percent.setValue(
            settings.get_settings_float_value(SettingsKey.MIN_PERCENT, config.DEFAULT_MIN_PERCENT))

    def _update_start_stop_status(self):
        elems = [self.ui.username, self.ui.token, self.ui.output_base_name]
        filled_elem_count = list(filter(lambda elem: len(elem.text()) > 0, elems))
        self.ui.start_stop.setEnabled(len(filled_elem_count) == len(elems))

    @Slot()
    def _start_collect(self):
        self._cancel_collect()

        logger.info('Start collecting statistics...')

        self._stats = None

        self._set_all_controls_enabled(False)
        self._update_cur_stats_status()
        self._replot_graph()

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
            self._stats = self._worker.cur_stats
            self._update_cur_stats_info()
            self._worker.stop()
            # self._worker = None

        if self._thread:
            self._thread.quit()
            self._thread.wait()
            self._thread = None

        self.started_time = None
        self._set_all_controls_enabled(True)
        self._update_cur_stats_status()
        self._replot_graph()
        self.stopped.emit()

        self.ui.start_stop.setText('Collect Statistics')
        self.ui.start_stop.clicked.disconnect()
        self.ui.start_stop.clicked.connect(self._start_collect)

        logger.info(f"Collecting {'done' if done else 'canceled'}")

    def _set_all_controls_enabled(self, enabled: bool = True):
        [elem.setEnabled(enabled) for elem in [
            self.ui.username, self.ui.token, self.ui.output_base_name, self.ui.use_cache, self.ui.min_percent
        ]]

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
        return self._stats is not None

    def _update_cur_stats_status(self):
        if self._is_data_ready():
            self.ui.stats_status.setText('<p style="color:green;">Statistics Ready</p')
        else:
            self.ui.stats_status.setText('<p style="color:tomato;">Statistics Not Ready</p')

    def _update_cur_stats_info(self):
        if not self._worker:
            logger.debug(f'_update_cur_stats_info() DONE')
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
