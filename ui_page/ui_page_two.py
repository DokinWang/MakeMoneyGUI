# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'page_two.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDateEdit, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QProgressBar,
    QSizePolicy, QSpacerItem, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget)

from qfluentwidgets import PushButton

class Ui_page_two(object):
    def setupUi(self, page_two):
        if not page_two.objectName():
            page_two.setObjectName(u"page_two")
        page_two.resize(840, 605)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(page_two.sizePolicy().hasHeightForWidth())
        page_two.setSizePolicy(sizePolicy)
        self.horizontalLayout = QHBoxLayout(page_two)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.widget_9 = QWidget(page_two)
        self.widget_9.setObjectName(u"widget_9")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.widget_9.sizePolicy().hasHeightForWidth())
        self.widget_9.setSizePolicy(sizePolicy1)
        self.widget_9.setMinimumSize(QSize(0, 0))
        self.verticalLayout_2 = QVBoxLayout(self.widget_9)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.stockBackTestTable = QTableWidget(self.widget_9)
        self.stockBackTestTable.setObjectName(u"stockBackTestTable")
        sizePolicy1.setHeightForWidth(self.stockBackTestTable.sizePolicy().hasHeightForWidth())
        self.stockBackTestTable.setSizePolicy(sizePolicy1)

        self.verticalLayout_2.addWidget(self.stockBackTestTable)

        self.backTestProgress = QProgressBar(self.widget_9)
        self.backTestProgress.setObjectName(u"backTestProgress")
        self.backTestProgress.setMaximum(100)
        self.backTestProgress.setValue(0)
        self.backTestProgress.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.backTestProgress)


        self.horizontalLayout.addWidget(self.widget_9)

        self.widget = QWidget(page_two)
        self.widget.setObjectName(u"widget")
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setMinimumSize(QSize(0, 0))
        self.widget.setMaximumSize(QSize(16777215, 16777215))
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widget_2 = QWidget(self.widget)
        self.widget_2.setObjectName(u"widget_2")
        sizePolicy.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy)
        self.widget_2.setMaximumSize(QSize(16777215, 40))
        self.horizontalLayout_2 = QHBoxLayout(self.widget_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label = QLabel(self.widget_2)
        self.label.setObjectName(u"label")
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setStyleSheet(u"font: 11pt \"Microsoft YaHei UI\";")

        self.horizontalLayout_2.addWidget(self.label)

        self.policySelect = QComboBox(self.widget_2)
        self.policySelect.addItem("")
        self.policySelect.addItem("")
        self.policySelect.setObjectName(u"policySelect")
        self.policySelect.setMinimumSize(QSize(100, 0))
        self.policySelect.setStyleSheet(u"font: 11pt \"Microsoft YaHei UI\";\n"
"QComboBox \\n{\\n	combobox-popup: 0;\\n}")

        self.horizontalLayout_2.addWidget(self.policySelect)


        self.verticalLayout.addWidget(self.widget_2)

        self.widget_5 = QWidget(self.widget)
        self.widget_5.setObjectName(u"widget_5")
        sizePolicy.setHeightForWidth(self.widget_5.sizePolicy().hasHeightForWidth())
        self.widget_5.setSizePolicy(sizePolicy)
        self.widget_5.setMaximumSize(QSize(200, 40))
        self.horizontalLayout_5 = QHBoxLayout(self.widget_5)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_4 = QLabel(self.widget_5)
        self.label_4.setObjectName(u"label_4")
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setStyleSheet(u"font: 11pt \"Microsoft YaHei UI\";")

        self.horizontalLayout_5.addWidget(self.label_4)

        self.startTime = QDateEdit(self.widget_5)
        self.startTime.setObjectName(u"startTime")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.startTime.sizePolicy().hasHeightForWidth())
        self.startTime.setSizePolicy(sizePolicy2)
        self.startTime.setMinimumSize(QSize(100, 0))
        font = QFont()
        self.startTime.setFont(font)
        self.startTime.setStyleSheet(u"")
        self.startTime.setDateTime(QDateTime(QDate(2023, 1, 3), QTime(16, 0, 0)))
        self.startTime.setMinimumDateTime(QDateTime(QDate(2023, 1, 3), QTime(16, 0, 0)))
        self.startTime.setMinimumDate(QDate(2023, 1, 3))
        self.startTime.setCalendarPopup(True)

        self.horizontalLayout_5.addWidget(self.startTime)


        self.verticalLayout.addWidget(self.widget_5)

        self.widget_6 = QWidget(self.widget)
        self.widget_6.setObjectName(u"widget_6")
        sizePolicy.setHeightForWidth(self.widget_6.sizePolicy().hasHeightForWidth())
        self.widget_6.setSizePolicy(sizePolicy)
        self.widget_6.setMaximumSize(QSize(200, 40))
        self.horizontalLayout_6 = QHBoxLayout(self.widget_6)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_5 = QLabel(self.widget_6)
        self.label_5.setObjectName(u"label_5")
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setStyleSheet(u"font: 11pt \"Microsoft YaHei UI\";")

        self.horizontalLayout_6.addWidget(self.label_5, 0, Qt.AlignLeft)

        self.endTime = QDateEdit(self.widget_6)
        self.endTime.setObjectName(u"endTime")
        sizePolicy2.setHeightForWidth(self.endTime.sizePolicy().hasHeightForWidth())
        self.endTime.setSizePolicy(sizePolicy2)
        self.endTime.setMinimumSize(QSize(100, 0))
        self.endTime.setStyleSheet(u"")
        self.endTime.setDateTime(QDateTime(QDate(2025, 8, 12), QTime(8, 0, 0)))
        self.endTime.setMinimumDateTime(QDateTime(QDate(2023, 1, 3), QTime(0, 0, 0)))
        self.endTime.setMinimumDate(QDate(2023, 1, 3))
        self.endTime.setMinimumTime(QTime(0, 0, 0))
        self.endTime.setCalendarPopup(True)

        self.horizontalLayout_6.addWidget(self.endTime)


        self.verticalLayout.addWidget(self.widget_6)

        self.widget_3 = QWidget(self.widget)
        self.widget_3.setObjectName(u"widget_3")
        sizePolicy.setHeightForWidth(self.widget_3.sizePolicy().hasHeightForWidth())
        self.widget_3.setSizePolicy(sizePolicy)
        self.widget_3.setMaximumSize(QSize(200, 40))
        self.horizontalLayout_3 = QHBoxLayout(self.widget_3)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_2 = QLabel(self.widget_3)
        self.label_2.setObjectName(u"label_2")
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setStyleSheet(u"font: 11pt \"Microsoft YaHei UI\";")

        self.horizontalLayout_3.addWidget(self.label_2, 0, Qt.AlignLeft)

        self.shMin = QLineEdit(self.widget_3)
        self.shMin.setObjectName(u"shMin")
        self.shMin.setMinimumSize(QSize(100, 0))
        self.shMin.setMaximumSize(QSize(16777215, 16777215))
        self.shMin.setStyleSheet(u"font: 11pt \"Microsoft YaHei UI\";")
        self.shMin.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_3.addWidget(self.shMin)


        self.verticalLayout.addWidget(self.widget_3, 0, Qt.AlignLeft)

        self.widget_4 = QWidget(self.widget)
        self.widget_4.setObjectName(u"widget_4")
        sizePolicy.setHeightForWidth(self.widget_4.sizePolicy().hasHeightForWidth())
        self.widget_4.setSizePolicy(sizePolicy)
        self.widget_4.setMaximumSize(QSize(200, 40))
        self.horizontalLayout_4 = QHBoxLayout(self.widget_4)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_3 = QLabel(self.widget_4)
        self.label_3.setObjectName(u"label_3")
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setStyleSheet(u"font: 11pt \"Microsoft YaHei UI\";")

        self.horizontalLayout_4.addWidget(self.label_3, 0, Qt.AlignLeft)

        self.shMax = QLineEdit(self.widget_4)
        self.shMax.setObjectName(u"shMax")
        self.shMax.setMinimumSize(QSize(100, 0))
        self.shMax.setMaximumSize(QSize(16777215, 16777215))
        self.shMax.setStyleSheet(u"font: 11pt \"Microsoft YaHei UI\";")
        self.shMax.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_4.addWidget(self.shMax)


        self.verticalLayout.addWidget(self.widget_4, 0, Qt.AlignLeft)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.backTestBtn = PushButton(self.widget)
        self.backTestBtn.setObjectName(u"backTestBtn")
        sizePolicy2.setHeightForWidth(self.backTestBtn.sizePolicy().hasHeightForWidth())
        self.backTestBtn.setSizePolicy(sizePolicy2)
        self.backTestBtn.setMinimumSize(QSize(150, 0))
        self.backTestBtn.setMaximumSize(QSize(16777215, 16777215))
        self.backTestBtn.setStyleSheet(u"font: 11pt \"Microsoft YaHei UI\";")

        self.verticalLayout.addWidget(self.backTestBtn, 0, Qt.AlignHCenter)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.widget_7 = QWidget(self.widget)
        self.widget_7.setObjectName(u"widget_7")
        sizePolicy.setHeightForWidth(self.widget_7.sizePolicy().hasHeightForWidth())
        self.widget_7.setSizePolicy(sizePolicy)
        self.widget_7.setMaximumSize(QSize(200, 40))
        self.horizontalLayout_7 = QHBoxLayout(self.widget_7)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_6 = QLabel(self.widget_7)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setStyleSheet(u"font: 11pt \"Microsoft YaHei UI\";")

        self.horizontalLayout_7.addWidget(self.label_6, 0, Qt.AlignLeft)

        self.avg_ret = QLineEdit(self.widget_7)
        self.avg_ret.setObjectName(u"avg_ret")
        self.avg_ret.setMinimumSize(QSize(70, 0))
        self.avg_ret.setMaximumSize(QSize(16777215, 16777215))
        self.avg_ret.setStyleSheet(u"font: 11pt \"Microsoft YaHei UI\";")
        self.avg_ret.setAlignment(Qt.AlignCenter)
        self.avg_ret.setReadOnly(True)

        self.horizontalLayout_7.addWidget(self.avg_ret)


        self.verticalLayout.addWidget(self.widget_7, 0, Qt.AlignLeft)

        self.widget_8 = QWidget(self.widget)
        self.widget_8.setObjectName(u"widget_8")
        sizePolicy.setHeightForWidth(self.widget_8.sizePolicy().hasHeightForWidth())
        self.widget_8.setSizePolicy(sizePolicy)
        self.widget_8.setMaximumSize(QSize(200, 40))
        self.horizontalLayout_8 = QHBoxLayout(self.widget_8)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label_7 = QLabel(self.widget_8)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setStyleSheet(u"font: 11pt \"Microsoft YaHei UI\";")

        self.horizontalLayout_8.addWidget(self.label_7, 0, Qt.AlignLeft)

        self.avg_days = QLineEdit(self.widget_8)
        self.avg_days.setObjectName(u"avg_days")
        self.avg_days.setMinimumSize(QSize(70, 0))
        self.avg_days.setMaximumSize(QSize(16777215, 16777215))
        self.avg_days.setStyleSheet(u"font: 11pt \"Microsoft YaHei UI\";")
        self.avg_days.setAlignment(Qt.AlignCenter)
        self.avg_days.setReadOnly(True)

        self.horizontalLayout_8.addWidget(self.avg_days)


        self.verticalLayout.addWidget(self.widget_8, 0, Qt.AlignLeft)

        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 1)
        self.verticalLayout.setStretch(2, 1)
        self.verticalLayout.setStretch(3, 1)
        self.verticalLayout.setStretch(4, 1)
        self.verticalLayout.setStretch(6, 1)
        self.verticalLayout.setStretch(7, 1)
        self.verticalLayout.setStretch(8, 1)
        self.verticalLayout.setStretch(9, 1)

        self.horizontalLayout.addWidget(self.widget, 0, Qt.AlignRight)

        self.horizontalLayout.setStretch(0, 1)

        self.retranslateUi(page_two)

        QMetaObject.connectSlotsByName(page_two)
    # setupUi

    def retranslateUi(self, page_two):
        page_two.setWindowTitle(QCoreApplication.translate("page_two", u"Form", None))
        self.label.setText(QCoreApplication.translate("page_two", u"\u7b56\u7565\u5468\u671f\uff1a", None))
        self.policySelect.setItemText(0, QCoreApplication.translate("page_two", u"\u4e09\u65e5\u7ebf", None))
        self.policySelect.setItemText(1, QCoreApplication.translate("page_two", u"\u5468\u7ebf", None))

        self.label_4.setText(QCoreApplication.translate("page_two", u"\u8d77\u59cb\u65e5\u671f\uff1a", None))
        self.label_5.setText(QCoreApplication.translate("page_two", u"\u7ed3\u675f\u65e5\u671f\uff1a", None))
        self.label_2.setText(QCoreApplication.translate("page_two", u"\u4e0a\u8bc1\u6700\u4f4e\uff1a", None))
        self.shMin.setText(QCoreApplication.translate("page_two", u"3100", None))
        self.label_3.setText(QCoreApplication.translate("page_two", u"\u4e0a\u8bc1\u6700\u9ad8\uff1a", None))
        self.shMax.setText(QCoreApplication.translate("page_two", u"3600", None))
        self.backTestBtn.setText(QCoreApplication.translate("page_two", u"\u56de\u6d4b", None))
        self.label_6.setText(QCoreApplication.translate("page_two", u"\u5e73\u5747\u6536\u76ca\u7387(%)\uff1a", None))
        self.avg_ret.setText(QCoreApplication.translate("page_two", u"0", None))
        self.label_7.setText(QCoreApplication.translate("page_two", u"\u5e73\u5747\u6301\u6709\u5929\u6570\uff1a  ", None))
        self.avg_days.setText(QCoreApplication.translate("page_two", u"0", None))
    # retranslateUi

