import datetime
import getpass
import pprint

from PySide6 import QtCore
from PySide6.QtCore import Slot, Signal, QTimer, QThread
from PySide6.QtWidgets import QDialog

from gh_repo_stats import config
from gh_repo_stats.core.cache import load_stats
from gh_repo_stats.core.graph import plot_graph_to_buffer
from gh_repo_stats.gui import logger, settings
from gh_repo_stats.gui.log_window import LogWindow
from gh_repo_stats.gui.settings import SettingsKey
from gh_repo_stats.gui.thread_worker import ThreadWorker
from gh_repo_stats.gui.ui.ui_main_dialog_2 import Ui_Dialog


class MainDialog(QDialog):
    started = Signal()
    stopped = Signal()

    _thread = None
    _worker = None

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

        #
        # connections
        #

        # # log window
        # self.ui.show_log_window.toggled.connect(lambda checked: self.log_window.setVisible(checked))
        # self.ui.show_log_window.setChecked(True)

        self.ui.splitter.splitterMoved.connect(lambda x: self._replot())

        [elem.textChanged.connect(self._update_start_stop_status) for elem in [
            self.ui.username, self.ui.token, self.ui.output_base_name
        ]]

        self.ui.min_percent.valueChanged.connect(self._replot)

        # start/stop + exit
        self.ui.start_stop.clicked.connect(self._start)

        # after connections!
        self._init_controls()

        # change preview size to new size
        QTimer.singleShot(0, lambda: self._replot())

    def closeEvent(self, event):
        logger.info('Exiting application...')

        self._stop()

        # save window position and size
        settings.set_settings_byte_array_value(SettingsKey.WINDOW_GEOMETRY, self.saveGeometry())
        settings.set_settings_byte_array_value(SettingsKey.WINDOW_STATE, self.windowState())
        settings.set_settings_byte_array_value(SettingsKey.SPLITTER_STATE, self.ui.splitter.saveState())

        event.accept()

    def resizeEvent(self, event):
        self._replot()
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
    def _start(self):
        self._stop()

        logger.info('Start gathering statistics...')

        self._set_all_controls_enabled(False)
        self.started_time = datetime.datetime.now()
        self.started.emit()

        # if self._stats is None:
        #     self._stats = collect_data(self.ui.username.text(), self.ui.token.text())
        #     self._update_cur_stats_status()

        self.ui.debug.setText(pprint.pformat(self._stats))

        self.ui.start_stop.setText('Cancel')
        self.ui.start_stop.clicked.disconnect()
        self.ui.start_stop.clicked.connect(self._stop)

        self._thread = QThread()
        self._worker = ThreadWorker(self.ui.username.text(), self.ui.token.text())
        self._worker.moveToThread(self._thread)
        self._worker.started.connect(self.started)
        self._worker.finished.connect(self._stop)

        self._thread.started.connect(self._worker.run)
        self._worker.progress.connect(self.ui.progress_bar.setValue)

        self._thread.start()

        # self._timer = QTimer()
        # self._timer.timeout.connect(self._recalc)
        # self._timer.start(1000)

        logger.info('Gathering started')

    @Slot()
    def _stop(self):
        logger.info('Stopping gathering statistics...')

        if self._worker is not None:
            self._worker.stop()
            self._worker = None

        if self._thread is not None:
            self._thread.quit()
            self._thread.wait()
            self._thread = None

        self.started_time = None
        self._set_all_controls_enabled(True)
        self.stopped.emit()

        self.ui.start_stop.setText('Gather Statistics')
        self.ui.start_stop.clicked.disconnect()
        self.ui.start_stop.clicked.connect(self._start)

        logger.info('Gathering stopped')

    def _set_all_controls_enabled(self, enabled: bool = True):
        [elem.setEnabled(enabled) for elem in [
            self.ui.username, self.ui.token, self.ui.output_base_name, self.ui.use_cache, self.ui.min_percent
        ]]

        # self.ui.start_stop.setEnabled(enabled)

    def _replot(self):
        if not self._is_data_ready():
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
