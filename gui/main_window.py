# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QLabel,
    QLineEdit, QMainWindow, QPushButton, QRadioButton,
    QSizePolicy, QStackedWidget, QStatusBar, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(930, 561)
        self.container = QWidget(MainWindow)
        self.container.setObjectName(u"container")
        self.run_button = QPushButton(self.container)
        self.run_button.setObjectName(u"run_button")
        self.run_button.setEnabled(False)
        self.run_button.setGeometry(QRect(250, 470, 101, 41))
        self.main_widget = QStackedWidget(self.container)
        self.main_widget.setObjectName(u"main_widget")
        self.main_widget.setGeometry(QRect(140, 30, 351, 371))
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.generate_widget = QWidget(self.page)
        self.generate_widget.setObjectName(u"generate_widget")
        self.generate_widget.setGeometry(QRect(30, 20, 281, 301))
        self.widget = QWidget(self.generate_widget)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(0, 20, 271, 271))
        self.generate_layout = QGridLayout(self.widget)
        self.generate_layout.setObjectName(u"generate_layout")
        self.generate_layout.setContentsMargins(0, 0, 0, 0)
        self.max_cpu_burst_duration = QLineEdit(self.widget)
        self.max_cpu_burst_duration.setObjectName(u"max_cpu_burst_duration")

        self.generate_layout.addWidget(self.max_cpu_burst_duration, 6, 1, 1, 1)

        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")

        self.generate_layout.addWidget(self.label, 0, 0, 1, 1)

        self.max_no_of_cpu_bursts = QLineEdit(self.widget)
        self.max_no_of_cpu_bursts.setObjectName(u"max_no_of_cpu_bursts")

        self.generate_layout.addWidget(self.max_no_of_cpu_bursts, 2, 1, 1, 1)

        self.label_10 = QLabel(self.widget)
        self.label_10.setObjectName(u"label_10")

        self.generate_layout.addWidget(self.label_10, 6, 0, 1, 1)

        self.label_5 = QLabel(self.widget)
        self.label_5.setObjectName(u"label_5")

        self.generate_layout.addWidget(self.label_5, 1, 0, 1, 1)

        self.max_number_of_processes = QLineEdit(self.widget)
        self.max_number_of_processes.setObjectName(u"max_number_of_processes")

        self.generate_layout.addWidget(self.max_number_of_processes, 0, 1, 1, 1)

        self.label_6 = QLabel(self.widget)
        self.label_6.setObjectName(u"label_6")

        self.generate_layout.addWidget(self.label_6, 2, 0, 1, 1)

        self.min_io_burst_duration = QLineEdit(self.widget)
        self.min_io_burst_duration.setObjectName(u"min_io_burst_duration")

        self.generate_layout.addWidget(self.min_io_burst_duration, 3, 1, 1, 1)

        self.label_8 = QLabel(self.widget)
        self.label_8.setObjectName(u"label_8")

        self.generate_layout.addWidget(self.label_8, 4, 0, 1, 1)

        self.max_io_burst_duration = QLineEdit(self.widget)
        self.max_io_burst_duration.setObjectName(u"max_io_burst_duration")

        self.generate_layout.addWidget(self.max_io_burst_duration, 4, 1, 1, 1)

        self.min_cpu_burst_duration = QLineEdit(self.widget)
        self.min_cpu_burst_duration.setObjectName(u"min_cpu_burst_duration")

        self.generate_layout.addWidget(self.min_cpu_burst_duration, 5, 1, 1, 1)

        self.label_7 = QLabel(self.widget)
        self.label_7.setObjectName(u"label_7")

        self.generate_layout.addWidget(self.label_7, 3, 0, 1, 1)

        self.label_9 = QLabel(self.widget)
        self.label_9.setObjectName(u"label_9")

        self.generate_layout.addWidget(self.label_9, 5, 0, 1, 1)

        self.max_arrival_time = QLineEdit(self.widget)
        self.max_arrival_time.setObjectName(u"max_arrival_time")

        self.generate_layout.addWidget(self.max_arrival_time, 1, 1, 1, 1)

        self.save_processes = QPushButton(self.page)
        self.save_processes.setObjectName(u"save_processes")
        self.save_processes.setGeometry(QRect(80, 320, 141, 32))
        self.main_widget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.widget1 = QWidget(self.page_2)
        self.widget1.setObjectName(u"widget1")
        self.widget1.setGeometry(QRect(0, 210, 331, 81))
        self.file_layout = QVBoxLayout(self.widget1)
        self.file_layout.setObjectName(u"file_layout")
        self.file_layout.setContentsMargins(0, 0, 0, 0)
        self.choose_file = QPushButton(self.widget1)
        self.choose_file.setObjectName(u"choose_file")

        self.file_layout.addWidget(self.choose_file)

        self.file_name = QLabel(self.widget1)
        self.file_name.setObjectName(u"file_name")

        self.file_layout.addWidget(self.file_name)

        self.main_widget.addWidget(self.page_2)
        self.widget2 = QWidget(self.container)
        self.widget2.setObjectName(u"widget2")
        self.widget2.setGeometry(QRect(590, 110, 202, 218))
        self.gridLayout = QGridLayout(self.widget2)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.label_2 = QLabel(self.widget2)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)

        self.q1 = QLineEdit(self.widget2)
        self.q1.setObjectName(u"q1")

        self.gridLayout.addWidget(self.q1, 0, 1, 1, 1)

        self.label_3 = QLabel(self.widget2)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)

        self.q2 = QLineEdit(self.widget2)
        self.q2.setObjectName(u"q2")

        self.gridLayout.addWidget(self.q2, 1, 1, 1, 1)

        self.label_4 = QLabel(self.widget2)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)

        self.alpha = QLineEdit(self.widget2)
        self.alpha.setObjectName(u"alpha")

        self.gridLayout.addWidget(self.alpha, 2, 1, 1, 1)

        self.widget3 = QWidget(self.container)
        self.widget3.setObjectName(u"widget3")
        self.widget3.setGeometry(QRect(160, 420, 301, 20))
        self.horizontalLayout = QHBoxLayout(self.widget3)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.file_radio = QRadioButton(self.widget3)
        self.file_radio.setObjectName(u"file_radio")

        self.horizontalLayout.addWidget(self.file_radio)

        self.generate_radio = QRadioButton(self.widget3)
        self.generate_radio.setObjectName(u"generate_radio")

        self.horizontalLayout.addWidget(self.generate_radio)

        MainWindow.setCentralWidget(self.container)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.main_widget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Simulator app", None))
        self.run_button.setText(QCoreApplication.translate("MainWindow", u"Run App", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Max Number Of Processes", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Max CPU Burst Duration", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Max Arrival Time", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Max Number Of CPU Bursts", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Max IO Burst Duration", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Min IO Burst Duration", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Min CPU Burst Duration", None))
        self.save_processes.setText(QCoreApplication.translate("MainWindow", u"Save Processes", None))
        self.choose_file.setText(QCoreApplication.translate("MainWindow", u"Choose File", None))
        self.file_name.setText("")
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Quantum 1", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Quantum 2", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Alpha", None))
        self.file_radio.setText(QCoreApplication.translate("MainWindow", u"Processes From File", None))
        self.generate_radio.setText(QCoreApplication.translate("MainWindow", u"Generate Processes", None))
    # retranslateUi

