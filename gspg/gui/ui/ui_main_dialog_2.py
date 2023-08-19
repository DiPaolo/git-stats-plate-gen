# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_dialog_2.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QDialog, QDoubleSpinBox,
    QGridLayout, QHBoxLayout, QLabel, QLineEdit,
    QProgressBar, QPushButton, QSizePolicy, QSpacerItem,
    QSplitter, QVBoxLayout, QWidget)

from gspg.gui.preview_widget import PreviewWidget

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(1333, 607)
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.splitter = QSplitter(Dialog)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.layoutWidget = QWidget(self.splitter)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.verticalLayout = QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.layoutWidget)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.username = QLineEdit(self.layoutWidget)
        self.username.setObjectName(u"username")

        self.horizontalLayout.addWidget(self.username)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_2 = QLabel(self.layoutWidget)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_2.addWidget(self.label_2)

        self.token = QLineEdit(self.layoutWidget)
        self.token.setObjectName(u"token")
        self.token.setEchoMode(QLineEdit.Password)

        self.horizontalLayout_2.addWidget(self.token)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.stats_status = QLabel(self.layoutWidget)
        self.stats_status.setObjectName(u"stats_status")
        self.stats_status.setTextFormat(Qt.RichText)

        self.horizontalLayout_6.addWidget(self.stats_status)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_4)

        self.start_stop = QPushButton(self.layoutWidget)
        self.start_stop.setObjectName(u"start_stop")

        self.horizontalLayout_6.addWidget(self.start_stop)


        self.verticalLayout.addLayout(self.horizontalLayout_6)

        self.progress_bar = QProgressBar(self.layoutWidget)
        self.progress_bar.setObjectName(u"progress_bar")
        self.progress_bar.setValue(0)

        self.verticalLayout.addWidget(self.progress_bar)

        self.debug = QLabel(self.layoutWidget)
        self.debug.setObjectName(u"debug")

        self.verticalLayout.addWidget(self.debug)

        self.verticalSpacer = QSpacerItem(20, 45, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.splitter.addWidget(self.layoutWidget)
        self.layoutWidget1 = QWidget(self.splitter)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.verticalLayout_2 = QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.preview = PreviewWidget(self.layoutWidget1)
        self.preview.setObjectName(u"preview")

        self.verticalLayout_2.addWidget(self.preview)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_4 = QLabel(self.layoutWidget1)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_3.addWidget(self.label_4)

        self.output_base_name = QLineEdit(self.layoutWidget1)
        self.output_base_name.setObjectName(u"output_base_name")

        self.horizontalLayout_3.addWidget(self.output_base_name)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.use_cache = QCheckBox(self.layoutWidget1)
        self.use_cache.setObjectName(u"use_cache")

        self.horizontalLayout_4.addWidget(self.use_cache)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer)


        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_3 = QLabel(self.layoutWidget1)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_5.addWidget(self.label_3)

        self.min_percent = QDoubleSpinBox(self.layoutWidget1)
        self.min_percent.setObjectName(u"min_percent")

        self.horizontalLayout_5.addWidget(self.min_percent)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_2)


        self.verticalLayout_2.addLayout(self.horizontalLayout_5)

        self.verticalLayout_2.setStretch(0, 1)
        self.splitter.addWidget(self.layoutWidget1)

        self.gridLayout.addWidget(self.splitter, 0, 0, 1, 1)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"GitHub User Name:", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Token:", None))
        self.stats_status.setText(QCoreApplication.translate("Dialog", u"<statistics status>", None))
        self.start_stop.setText(QCoreApplication.translate("Dialog", u"Gather Statistics", None))
        self.progress_bar.setFormat(QCoreApplication.translate("Dialog", u"%v/%m (%p%)", None))
        self.debug.setText("")
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Output Image Base Name:", None))
        self.use_cache.setText(QCoreApplication.translate("Dialog", u"Use Cached Data if Possible", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Min Percent:", None))
    # retranslateUi

