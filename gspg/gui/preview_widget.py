from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget

from gspg import config
from gspg.gui.ui.ui_preview_widget import Ui_Form


class PreviewWidget(QWidget):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self._pixmap = QPixmap()
        self.ui.label.setPixmap(self._pixmap)

    def set_data(self, data: bytes):
        self._pixmap.loadFromData(data, format=config.INTERNAL_IMAGE_TYPE)
        self.ui.label.setPixmap(self._pixmap)
