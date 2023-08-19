import logging
import pprint

from PySide6.QtCore import QObject, Signal, Slot

from gh_repo_stats import config
from gh_repo_stats.core.data import collect_data_gen

_l = logging.getLogger('gui.worker')


class ThreadWorker(QObject):
    started = Signal()
    finished = Signal()
    progress = Signal(float)

    _cur_stats = None
    _cancel_requested = False
    _username: str = None
    _token: str = None
    _progress: float = 0.0

    def __init__(self, username: str, token: str):
        super().__init__()

        self._username = username
        self._token = token

    @property
    def total_progress(self) -> float:
        return self._progress

    def run(self):
        _l.info('starting...')
        self._cur_stats = dict()

        self.started.emit()

        gen = collect_data_gen(self._username, self._token)
        while not self._cancel_requested:
            processed, left, self._cur_stats = next(gen)

            _l.debug(f'{processed}/{processed + left}')

            total = max(processed + left, 1)  # use 1 to avoid division by zero
            self.progress.emit(processed * 100.0 / total)

            if left == 0:
                self.progress.emit(100.0)
                break

            if config.DEBUG and processed == config.MAX_REPOS_TO_PROCESS:
                break

        _l.info('done' if not self._cancel_requested else 'canceled')

        self.finished.emit()

    @Slot()
    def stop(self):
        self._cancel_requested = True
