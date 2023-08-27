import copy
import logging
from typing import Dict

from PySide6.QtCore import QObject, Signal, Slot

from git_stats_plate_gen import config
from git_stats_plate_gen.core.data import collect_data_gen

_l = logging.getLogger('gui.worker')


class ThreadWorker(QObject):
    started = Signal()
    finished = Signal(bool)
    progress = Signal(float)

    _cur_stats = None
    _cancel_requested = False
    _username: str = None
    _token: str = None
    _progress: float = 0.0
    _processed = 0
    _left = 0

    def __init__(self, username: str, token: str):
        super().__init__()

        self._username = username
        self._token = token

    @property
    def total_progress(self) -> float:
        return self._progress

    @property
    def processed(self) -> int:
        return self._processed

    @property
    def left(self) -> int:
        return self._left

    @property
    def total(self) -> int:
        return self._processed + self._left

    @property
    def cur_stats(self) -> Dict:
        return copy.deepcopy(self._cur_stats)

    def run(self):
        _l.info('starting...')
        self._cur_stats = dict()

        self.started.emit()

        gen = collect_data_gen(self._username, self._token)
        while not self._cancel_requested:
            self._processed, self._left, self._cur_stats = next(gen)

            # use local to reduce the potential risk of race conditions
            processed = self._processed
            left = self._left

            _l.debug(f'{processed}/{processed + left}')

            total = min(processed + left, config.MAX_REPOS_TO_PROCESS if config.DEBUG else processed + left)
            total = max(total, 1)  # use 1 to avoid division by zero
            self.progress.emit(processed * 100.0 / total)

            if left == 0:
                self.progress.emit(100.0)
                break

            if config.DEBUG and processed >= config.MAX_REPOS_TO_PROCESS:
                break

        _l.info('done' if not self._cancel_requested else 'canceled')

        self.finished.emit(not self._cancel_requested)

    @Slot()
    def stop(self):
        self._cancel_requested = True
