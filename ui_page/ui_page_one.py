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
from PySide6.QtWidgets import (QApplication, QHeaderView, QSizePolicy, QTableWidget,
    QTableWidgetItem, QWidget)

from qfluentwidgets import PushButton

class Ui_page_one(object):
    def setupUi(self, page_one):
        if not page_one.objectName():
            page_one.setObjectName(u"page_one")
        page_one.resize(723, 456)
        self.pushButton = PushButton(page_one)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(10, 10, 111, 31))
        self.pushButton_2 = PushButton(page_one)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(10, 50, 111, 31))
        self.stockUpdataTable = QTableWidget(page_one)
        self.stockUpdataTable.setObjectName(u"stockUpdataTable")
        self.stockUpdataTable.setGeometry(QRect(140, 10, 511, 431))

        self.retranslateUi(page_one)

        QMetaObject.connectSlotsByName(page_one)
    # setupUi

    def retranslateUi(self, page_one):
        page_one.setWindowTitle(QCoreApplication.translate("page_one", u"Form", None))
        self.pushButton.setText(QCoreApplication.translate("page_one", u"\u66f4\u65b0\u6240\u6709\u80a1\u7968\u6570\u636e", None))
        self.pushButton_2.setText(QCoreApplication.translate("page_one", u"\u66f4\u65b0\u672c\u5730\u80a1\u7968\u6570\u636e", None))
    # retranslateUi

