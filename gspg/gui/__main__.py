import logging
import sys

from PySide6.QtCore import QCoreApplication
from PySide6.QtWidgets import QApplication

from gspg import config
# from gspg.app import init_app, deinit_app
from gspg.gui.main_dialog import MainDialog

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

QCoreApplication.setOrganizationName(config.ORGANIZATION_NAME)
QCoreApplication.setOrganizationDomain(config.ORGANIZATION_DOMAIN)
QCoreApplication.setApplicationName(config.APPLICATION_NAME)

app = QApplication(sys.argv)

# init_app()

mainDlg = MainDialog()
mainDlg.show()

ret_code = app.exec()

# deinit_app()

sys.exit(ret_code)
