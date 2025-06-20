# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.5.3
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
from PySide6.QtWidgets import (QApplication, QDialog, QDoubleSpinBox, QGridLayout,
    QHBoxLayout, QLabel, QLineEdit, QProgressBar,
    QPushButton, QSizePolicy, QSpacerItem, QSplitter,
    QToolButton, QVBoxLayout, QWidget)

from git_stats_plate_gen.gui.preview_widget import PreviewWidget

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(784, 473)
        self.gridLayout_2 = QGridLayout(Dialog)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.splitter = QSplitter(Dialog)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.layoutWidget = QWidget(self.splitter)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.verticalLayout = QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_2 = QLabel(self.layoutWidget)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_2.addWidget(self.label_2)

        self.token = QLineEdit(self.layoutWidget)
        self.token.setObjectName(u"token")
        self.token.setEchoMode(QLineEdit.Password)

        self.horizontalLayout_2.addWidget(self.token)

        self.show_token_help = QPushButton(self.layoutWidget)
        self.show_token_help.setObjectName(u"show_token_help")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.show_token_help.sizePolicy().hasHeightForWidth())
        self.show_token_help.setSizePolicy(sizePolicy)
        self.show_token_help.setMinimumSize(QSize(16, 16))
        self.show_token_help.setMaximumSize(QSize(32, 32))
        self.show_token_help.setCheckable(True)
        self.show_token_help.setAutoDefault(False)

        self.horizontalLayout_2.addWidget(self.show_token_help)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.token_help = QLabel(self.layoutWidget)
        self.token_help.setObjectName(u"token_help")
        font = QFont()
        font.setPointSize(9)
        self.token_help.setFont(font)
        self.token_help.setWordWrap(True)
        self.token_help.setOpenExternalLinks(True)

        self.verticalLayout.addWidget(self.token_help)

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
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.preview.sizePolicy().hasHeightForWidth())
        self.preview.setSizePolicy(sizePolicy1)

        self.verticalLayout_2.addWidget(self.preview)

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

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_6 = QLabel(self.layoutWidget1)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 1, 0, 1, 1)

        self.label_5 = QLabel(self.layoutWidget1)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 2, 0, 1, 1)

        self.output_folder = QLineEdit(self.layoutWidget1)
        self.output_folder.setObjectName(u"output_folder")
        self.output_folder.setEnabled(False)
        self.output_folder.setCursorPosition(0)
        self.output_folder.setClearButtonEnabled(False)

        self.gridLayout.addWidget(self.output_folder, 0, 1, 1, 1)

        self.full_image_file_path = QLabel(self.layoutWidget1)
        self.full_image_file_path.setObjectName(u"full_image_file_path")

        self.gridLayout.addWidget(self.full_image_file_path, 2, 1, 1, 2)

        self.label_4 = QLabel(self.layoutWidget1)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 0, 0, 1, 1)

        self.choose_out_image_dir = QToolButton(self.layoutWidget1)
        self.choose_out_image_dir.setObjectName(u"choose_out_image_dir")

        self.gridLayout.addWidget(self.choose_out_image_dir, 0, 2, 1, 1)

        self.image_filename_template = QLineEdit(self.layoutWidget1)
        self.image_filename_template.setObjectName(u"image_filename_template")

        self.gridLayout.addWidget(self.image_filename_template, 1, 1, 1, 1)

        self.save_image = QPushButton(self.layoutWidget1)
        self.save_image.setObjectName(u"save_image")

        self.gridLayout.addWidget(self.save_image, 1, 2, 1, 1)


        self.verticalLayout_2.addLayout(self.gridLayout)

        self.splitter.addWidget(self.layoutWidget1)

        self.gridLayout_2.addWidget(self.splitter, 0, 0, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.program_name_n_version = QLabel(Dialog)
        self.program_name_n_version.setObjectName(u"program_name_n_version")
        self.program_name_n_version.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.program_name_n_version)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.copyright = QLabel(Dialog)
        self.copyright.setObjectName(u"copyright")
        self.copyright.setOpenExternalLinks(True)

        self.horizontalLayout_3.addWidget(self.copyright)


        self.gridLayout_2.addLayout(self.horizontalLayout_3, 3, 0, 1, 1)

        self.user_message = QLabel(Dialog)
        self.user_message.setObjectName(u"user_message")
        self.user_message.setTextFormat(Qt.RichText)

        self.gridLayout_2.addWidget(self.user_message, 1, 0, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.gridLayout_2.addItem(self.verticalSpacer_2, 2, 0, 1, 1)

        self.gridLayout_2.setRowStretch(0, 1)

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"GitHub User Token:", None))
        self.show_token_help.setText("")
        self.token_help.setText(QCoreApplication.translate("Dialog", u"<will be set programmatically>", None))
        self.stats_status.setText(QCoreApplication.translate("Dialog", u"<statistics status>", None))
        self.start_stop.setText(QCoreApplication.translate("Dialog", u"Collect Statistics", None))
        self.progress_bar.setFormat(QCoreApplication.translate("Dialog", u"%v/%m (%p%)", None))
        self.debug.setText("")
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Min Percent to be Shown:", None))
        self.label_6.setText(QCoreApplication.translate("Dialog", u"Filename Template:", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"Full Filename:", None))
        self.output_folder.setInputMask("")
        self.output_folder.setText("")
        self.output_folder.setPlaceholderText("")
        self.full_image_file_path.setText(QCoreApplication.translate("Dialog", u"<full tilename>", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Output Folder:", None))
        self.choose_out_image_dir.setText(QCoreApplication.translate("Dialog", u"...", None))
        self.save_image.setText(QCoreApplication.translate("Dialog", u"Save", None))
        self.program_name_n_version.setText(QCoreApplication.translate("Dialog", u"<program name & version>", None))
        self.copyright.setText(QCoreApplication.translate("Dialog", u"<copyright>", None))
        self.user_message.setText("")
    # retranslateUi

