from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget

from gh_repo_stats.gui.ui.ui_preview_widget import Ui_Form


class PreviewWidget(QWidget):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self._pixmap = QPixmap()
        self.ui.label.setPixmap(self._pixmap)

    def set_data(self, data: bytes):
        self._pixmap.loadFromData(data, format='png')
        self.ui.label.setPixmap(self._pixmap)

    def resizeEvent(self, event):
        print(f'resizeEvent: size={event}')
        event.accept()
