# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'page_three.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QProgressBar,
    QSizePolicy, QSpacerItem, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget)

from qfluentwidgets import PushButton

class Ui_page_three(object):
    def setupUi(self, page_three):
        if not page_three.objectName():
            page_three.setObjectName(u"page_three")
        page_three.resize(840, 605)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(page_three.sizePolicy().hasHeightForWidth())
        page_three.setSizePolicy(sizePolicy)
        self.horizontalLayout = QHBoxLayout(page_three)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.widget_9 = QWidget(page_three)
        self.widget_9.setObjectName(u"widget_9")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.widget_9.sizePolicy().hasHeightForWidth())
        self.widget_9.setSizePolicy(sizePolicy1)
        self.widget_9.setMinimumSize(QSize(0, 0))
        self.verticalLayout_2 = QVBoxLayout(self.widget_9)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.stockBollTable = QTableWidget(self.widget_9)
        self.stockBollTable.setObjectName(u"stockBollTable")
        sizePolicy1.setHeightForWidth(self.stockBollTable.sizePolicy().hasHeightForWidth())
        self.stockBollTable.setSizePolicy(sizePolicy1)

        self.verticalLayout_2.addWidget(self.stockBollTable)

        self.backTestProgress = QProgressBar(self.widget_9)
        self.backTestProgress.setObjectName(u"backTestProgress")
        self.backTestProgress.setMaximum(100)
        self.backTestProgress.setValue(0)
        self.backTestProgress.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.backTestProgress)


        self.horizontalLayout.addWidget(self.widget_9)

        self.widget = QWidget(page_three)
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
        self.policySelect.addItem("")
        self.policySelect.setObjectName(u"policySelect")
        self.policySelect.setMinimumSize(QSize(100, 0))
        self.policySelect.setStyleSheet(u"font: 11pt \"Microsoft YaHei UI\";\n"
"QComboBox \\n{\\n	combobox-popup: 0;\\n}")

        self.horizontalLayout_2.addWidget(self.policySelect)


        self.verticalLayout.addWidget(self.widget_2)

        self.widget_11 = QWidget(self.widget)
        self.widget_11.setObjectName(u"widget_11")
        self.horizontalLayout_10 = QHBoxLayout(self.widget_11)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.breakUp = QCheckBox(self.widget_11)
        self.breakUp.setObjectName(u"breakUp")
        self.breakUp.setStyleSheet(u"font: 11pt \"Microsoft YaHei UI\";")

        self.horizontalLayout_10.addWidget(self.breakUp)


        self.verticalLayout.addWidget(self.widget_11)

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

        self.horizontalLayout_4.addWidget(self.label_3)

        self.marketValMin = QLineEdit(self.widget_4)
        self.marketValMin.setObjectName(u"marketValMin")
        self.marketValMin.setMinimumSize(QSize(50, 0))
        self.marketValMin.setMaximumSize(QSize(50, 16777215))
        self.marketValMin.setStyleSheet(u"font: 11pt \"Microsoft YaHei UI\";")
        self.marketValMin.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_4.addWidget(self.marketValMin)

        self.marketValMax = QLineEdit(self.widget_4)
        self.marketValMax.setObjectName(u"marketValMax")
        self.marketValMax.setMinimumSize(QSize(50, 0))
        self.marketValMax.setMaximumSize(QSize(50, 16777215))
        self.marketValMax.setStyleSheet(u"font: 11pt \"Microsoft YaHei UI\";")
        self.marketValMax.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_4.addWidget(self.marketValMax)


        self.verticalLayout.addWidget(self.widget_4)

        self.widget_13 = QWidget(self.widget)
        self.widget_13.setObjectName(u"widget_13")
        sizePolicy.setHeightForWidth(self.widget_13.sizePolicy().hasHeightForWidth())
        self.widget_13.setSizePolicy(sizePolicy)
        self.widget_13.setMaximumSize(QSize(200, 40))
        self.horizontalLayout_12 = QHBoxLayout(self.widget_13)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.label_10 = QLabel(self.widget_13)
        self.label_10.setObjectName(u"label_10")
        sizePolicy.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy)
        self.label_10.setStyleSheet(u"font: 11pt \"Microsoft YaHei UI\";")

        self.horizontalLayout_12.addWidget(self.label_10)

        self.peRatioMin = QLineEdit(self.widget_13)
        self.peRatioMin.setObjectName(u"peRatioMin")
        self.peRatioMin.setMinimumSize(QSize(50, 0))
        self.peRatioMin.setMaximumSize(QSize(50, 16777215))
        self.peRatioMin.setStyleSheet(u"font: 11pt \"Microsoft YaHei UI\";")
        self.peRatioMin.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_12.addWidget(self.peRatioMin)

        self.peRatioMax = QLineEdit(self.widget_13)
        self.peRatioMax.setObjectName(u"peRatioMax")
        self.peRatioMax.setMinimumSize(QSize(50, 0))
        self.peRatioMax.setMaximumSize(QSize(50, 16777215))
        self.peRatioMax.setStyleSheet(u"font: 11pt \"Microsoft YaHei UI\";")
        self.peRatioMax.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_12.addWidget(self.peRatioMax)


        self.verticalLayout.addWidget(self.widget_13)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.bollFindBtn = PushButton(self.widget)
        self.bollFindBtn.setObjectName(u"bollFindBtn")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.bollFindBtn.sizePolicy().hasHeightForWidth())
        self.bollFindBtn.setSizePolicy(sizePolicy2)
        self.bollFindBtn.setMinimumSize(QSize(150, 0))
        self.bollFindBtn.setMaximumSize(QSize(16777215, 16777215))
        self.bollFindBtn.setStyleSheet(u"font: 11pt \"Microsoft YaHei UI\";")

        self.verticalLayout.addWidget(self.bollFindBtn, 0, Qt.AlignHCenter)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(5, 1)
        self.verticalLayout.setStretch(6, 1)

        self.horizontalLayout.addWidget(self.widget, 0, Qt.AlignRight)

        self.horizontalLayout.setStretch(0, 1)

        self.retranslateUi(page_three)

        QMetaObject.connectSlotsByName(page_three)
    # setupUi

    def retranslateUi(self, page_three):
        page_three.setWindowTitle(QCoreApplication.translate("page_three", u"Form", None))
        self.label.setText(QCoreApplication.translate("page_three", u"\u7b56\u7565\u5468\u671f\uff1a", None))
        self.policySelect.setItemText(0, QCoreApplication.translate("page_three", u"\u4e09\u65e5\u7ebf", None))
        self.policySelect.setItemText(1, QCoreApplication.translate("page_three", u"\u5468\u7ebf", None))
        self.policySelect.setItemText(2, QCoreApplication.translate("page_three", u"\u6708\u7ebf", None))

        self.breakUp.setText(QCoreApplication.translate("page_three", u"\u4e70\u5165\u70b9\u5148\u7a81\u7834\u4e0a\u8f68", None))
        self.label_3.setText(QCoreApplication.translate("page_three", u"\u5e02\u503c\u8303\u56f4\uff1a", None))
        self.marketValMin.setText(QCoreApplication.translate("page_three", u"50", None))
        self.marketValMax.setText(QCoreApplication.translate("page_three", u"5000", None))
        self.label_10.setText(QCoreApplication.translate("page_three", u"\u5e02\u76c8\u7387\uff1a", None))
        self.peRatioMin.setText(QCoreApplication.translate("page_three", u"20", None))
        self.peRatioMax.setText(QCoreApplication.translate("page_three", u"80", None))
        self.bollFindBtn.setText(QCoreApplication.translate("page_three", u"\u67e5\u627e", None))
    # retranslateUi

