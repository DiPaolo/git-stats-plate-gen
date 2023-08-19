# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_dialog.ui'
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
    QFrame, QGridLayout, QHBoxLayout, QLabel,
    QLineEdit, QProgressBar, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(1027, 313)
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalSpacer = QSpacerItem(20, 45, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 1, 0, 1, 1)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.username = QLineEdit(Dialog)
        self.username.setObjectName(u"username")

        self.horizontalLayout.addWidget(self.username)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_2.addWidget(self.label_2)

        self.token = QLineEdit(Dialog)
        self.token.setObjectName(u"token")
        self.token.setEchoMode(QLineEdit.Password)

        self.horizontalLayout_2.addWidget(self.token)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_4 = QLabel(Dialog)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_3.addWidget(self.label_4)

        self.output_base_name = QLineEdit(Dialog)
        self.output_base_name.setObjectName(u"output_base_name")

        self.horizontalLayout_3.addWidget(self.output_base_name)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.use_cache = QCheckBox(Dialog)
        self.use_cache.setObjectName(u"use_cache")

        self.horizontalLayout_4.addWidget(self.use_cache)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_3 = QLabel(Dialog)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_5.addWidget(self.label_3)

        self.min_percent = QDoubleSpinBox(Dialog)
        self.min_percent.setObjectName(u"min_percent")

        self.horizontalLayout_5.addWidget(self.min_percent)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_4)

        self.start = QPushButton(Dialog)
        self.start.setObjectName(u"start")

        self.horizontalLayout_6.addWidget(self.start)


        self.verticalLayout.addLayout(self.horizontalLayout_6)

        self.progress_bar = QProgressBar(Dialog)
        self.progress_bar.setObjectName(u"progress_bar")
        self.progress_bar.setValue(0)

        self.verticalLayout.addWidget(self.progress_bar)


        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.preview = QLabel(Dialog)
        self.preview.setObjectName(u"preview")
        self.preview.setFrameShape(QFrame.StyledPanel)
        self.preview.setFrameShadow(QFrame.Raised)

        self.gridLayout.addWidget(self.preview, 0, 1, 2, 1)

        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 1)

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"GitHub User Name:", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Token:", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Output Image Base Name:", None))
        self.use_cache.setText(QCoreApplication.translate("Dialog", u"Use Cached Data if Possible", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Min Percent:", None))
        self.start.setText(QCoreApplication.translate("Dialog", u"Start", None))
        self.preview.setText("")
    # retranslateUi

