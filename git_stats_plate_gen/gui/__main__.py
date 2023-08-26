import logging
import sys

from PySide6.QtCore import QCoreApplication
from PySide6.QtWidgets import QApplication

from git_stats_plate_gen import config
# from git_stats_plate_gen.app import init_app, deinit_app
from git_stats_plate_gen.gui.main_dialog import MainDialog

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
