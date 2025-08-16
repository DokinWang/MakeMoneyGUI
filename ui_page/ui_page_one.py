# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'page_one.ui'
##
## Created by: Qt User Interface Compiler version 6.7.0
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
from PySide6.QtWidgets import (QApplication, QDateEdit, QGroupBox, QHBoxLayout,
    QHeaderView, QProgressBar, QSizePolicy, QSpacerItem,
    QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget)

from qfluentwidgets import PushButton

class Ui_page_one(object):
    def setupUi(self, page_one):
        if not page_one.objectName():
            page_one.setObjectName(u"page_one")
        page_one.resize(861, 622)
        self.horizontalLayout = QHBoxLayout(page_one)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.widget_2 = QWidget(page_one)
        self.widget_2.setObjectName(u"widget_2")
        self.verticalLayout_2 = QVBoxLayout(self.widget_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.stockUpdataTable = QTableWidget(self.widget_2)
        self.stockUpdataTable.setObjectName(u"stockUpdataTable")

        self.verticalLayout_2.addWidget(self.stockUpdataTable)

        self.updateProgress = QProgressBar(self.widget_2)
        self.updateProgress.setObjectName(u"updateProgress")
        self.updateProgress.setValue(0)
        self.updateProgress.setAlignment(Qt.AlignCenter)
        self.updateProgress.setTextVisible(True)
        self.updateProgress.setOrientation(Qt.Horizontal)
        self.updateProgress.setTextDirection(QProgressBar.TopToBottom)

        self.verticalLayout_2.addWidget(self.updateProgress)


        self.horizontalLayout.addWidget(self.widget_2)

        self.widget = QWidget(page_one)
        self.widget.setObjectName(u"widget")
        self.widget.setMinimumSize(QSize(160, 0))
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.groupBox = QGroupBox(self.widget)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_3 = QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 9, 0, 9)
        self.update_day = QDateEdit(self.groupBox)
        self.update_day.setObjectName(u"update_day")
        self.update_day.setStyleSheet(u"font: 11pt \"Microsoft YaHei UI\";")
        self.update_day.setDateTime(QDateTime(QDate(2025, 8, 14), QTime(16, 0, 0)))
        self.update_day.setCalendarPopup(True)

        self.verticalLayout_3.addWidget(self.update_day)

        self.verticalSpacer_5 = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_3.addItem(self.verticalSpacer_5)

        self.updateLocalBtn = PushButton(self.groupBox)
        self.updateLocalBtn.setObjectName(u"updateLocalBtn")
        self.updateLocalBtn.setStyleSheet(u"font: 11pt \"Microsoft YaHei UI\";")

        self.verticalLayout_3.addWidget(self.updateLocalBtn)


        self.verticalLayout.addWidget(self.groupBox)

        self.verticalSpacer_4 = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout.addItem(self.verticalSpacer_4)

        self.loadLocalBtn = PushButton(self.widget)
        self.loadLocalBtn.setObjectName(u"loadLocalBtn")
        self.loadLocalBtn.setStyleSheet(u"font: 11pt \"Microsoft YaHei UI\";")

        self.verticalLayout.addWidget(self.loadLocalBtn)

        self.verticalSpacer_3 = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout.addItem(self.verticalSpacer_3)

        self.updateClearBtn = PushButton(self.widget)
        self.updateClearBtn.setObjectName(u"updateClearBtn")
        self.updateClearBtn.setStyleSheet(u"font: 11pt \"Microsoft YaHei UI\";")

        self.verticalLayout.addWidget(self.updateClearBtn)


        self.horizontalLayout.addWidget(self.widget)


        self.retranslateUi(page_one)

        QMetaObject.connectSlotsByName(page_one)
    # setupUi

    def retranslateUi(self, page_one):
        page_one.setWindowTitle(QCoreApplication.translate("page_one", u"Form", None))
        self.groupBox.setTitle(QCoreApplication.translate("page_one", u"\u66f4\u65b0\u81f3", None))
        self.updateLocalBtn.setText(QCoreApplication.translate("page_one", u"\u66f4\u65b0\u672c\u5730\u6570\u636e", None))
        self.loadLocalBtn.setText(QCoreApplication.translate("page_one", u"\u52a0\u8f7d\u672c\u5730\u6570\u636e", None))
        self.updateClearBtn.setText(QCoreApplication.translate("page_one", u"\u6e05\u7a7a", None))
    # retranslateUi

