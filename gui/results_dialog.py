# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'results_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
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
from PySide6.QtWidgets import (QApplication, QDialog, QHBoxLayout, QHeaderView,
    QLabel, QSizePolicy, QTableWidget, QTableWidgetItem,
    QWidget)

class Ui_results_dialog(object):
    def setupUi(self, results_dialog):
        if not results_dialog.objectName():
            results_dialog.setObjectName(u"results_dialog")
        results_dialog.setWindowModality(Qt.WindowModal)
        results_dialog.resize(1920, 1080)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(results_dialog.sizePolicy().hasHeightForWidth())
        results_dialog.setSizePolicy(sizePolicy)
        results_dialog.setMinimumSize(QSize(1920, 1080))
        results_dialog.setBaseSize(QSize(1920, 1080))
        results_dialog.setModal(True)
        self.results_table = QTableWidget(results_dialog)
        self.results_table.setObjectName(u"results_table")
        self.results_table.setEnabled(True)
        self.results_table.setGeometry(QRect(20, 130, 911, 231))
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(1)
        sizePolicy1.setVerticalStretch(1)
        sizePolicy1.setHeightForWidth(self.results_table.sizePolicy().hasHeightForWidth())
        self.results_table.setSizePolicy(sizePolicy1)
        self.label = QLabel(results_dialog)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(30, 90, 211, 31))
        font = QFont()
        font.setPointSize(18)
        self.label.setFont(font)
        self.guant_chart = QTableWidget(results_dialog)
        self.guant_chart.setObjectName(u"guant_chart")
        self.guant_chart.setGeometry(QRect(20, 420, 921, 431))
        self.label_2 = QLabel(results_dialog)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(20, 380, 271, 31))
        self.label_2.setFont(font)
        self.label_3 = QLabel(results_dialog)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(1020, 30, 241, 31))
        self.label_3.setFont(font)
        self.log = QTableWidget(results_dialog)
        self.log.setObjectName(u"log")
        self.log.setGeometry(QRect(1000, 70, 661, 801))
        self.widget = QWidget(results_dialog)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(30, 60, 481, 21))
        self.horizontalLayout_2 = QHBoxLayout(self.widget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.cpu_utilization = QLabel(self.widget)
        self.cpu_utilization.setObjectName(u"cpu_utilization")
        font1 = QFont()
        font1.setPointSize(14)
        font1.setBold(True)
        self.cpu_utilization.setFont(font1)
        self.cpu_utilization.setStyleSheet(u"color: orange;")

        self.horizontalLayout_2.addWidget(self.cpu_utilization)

        self.average_waiting = QLabel(self.widget)
        self.average_waiting.setObjectName(u"average_waiting")
        self.average_waiting.setFont(font1)
        self.average_waiting.setStyleSheet(u"color: green;")

        self.horizontalLayout_2.addWidget(self.average_waiting)


        self.retranslateUi(results_dialog)

        QMetaObject.connectSlotsByName(results_dialog)
    # setupUi

    def retranslateUi(self, results_dialog):
        results_dialog.setWindowTitle(QCoreApplication.translate("results_dialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("results_dialog", u"Results Table", None))
        self.label_2.setText(QCoreApplication.translate("results_dialog", u"Guant Chart", None))
        self.label_3.setText(QCoreApplication.translate("results_dialog", u"Log", None))
        self.cpu_utilization.setText(QCoreApplication.translate("results_dialog", u"CPU Utilization:", None))
        self.average_waiting.setText(QCoreApplication.translate("results_dialog", u"Average Waiting", None))
    # retranslateUi

