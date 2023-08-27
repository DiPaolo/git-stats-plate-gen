from typing import Optional

from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget

from git_stats_plate_gen import config
from git_stats_plate_gen.gui.ui.ui_preview_widget import Ui_Form


class PreviewWidget(QWidget):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self._pixmap = QPixmap()
        self.ui.label.setPixmap(self._pixmap)

    def set_data(self, data: Optional[bytes]):
        if data:
            if not self._pixmap:
                self._pixmap = QPixmap()
            self._pixmap.loadFromData(data, format=config.INTERNAL_IMAGE_TYPE)
            self.ui.label.setPixmap(self._pixmap)
        else:
            self._pixmap = None
            self.ui.label.setText('No statistics to plot graph')

    def save_image(self, file_path: str) -> bool:
        if not self._pixmap:
            return False

        ret = self._pixmap.save(file_path)
        return ret
