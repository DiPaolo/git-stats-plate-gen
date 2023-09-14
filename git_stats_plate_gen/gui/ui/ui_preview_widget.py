# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'preview_widget.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCharts import QChartView
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QSizePolicy,
    QStackedWidget, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1280, 720)
        self.gridLayout_3 = QGridLayout(Form)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.stackedWidget = QStackedWidget(Form)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.page_no_data = QWidget()
        self.page_no_data.setObjectName(u"page_no_data")
        self.gridLayout_2 = QGridLayout(self.page_no_data)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label = QLabel(self.page_no_data)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)

        self.stackedWidget.addWidget(self.page_no_data)
        self.page_chart = QWidget()
        self.page_chart.setObjectName(u"page_chart")
        self.gridLayout = QGridLayout(self.page_chart)
        self.gridLayout.setObjectName(u"gridLayout")
        self.chart_view = QChartView(self.page_chart)
        self.chart_view.setObjectName(u"chart_view")

        self.gridLayout.addWidget(self.chart_view, 0, 0, 1, 1)

        self.stackedWidget.addWidget(self.page_chart)

        self.gridLayout_3.addWidget(self.stackedWidget, 0, 0, 1, 1)


        self.retranslateUi(Form)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"No statistics to plot graph", None))
    # retranslateUi

