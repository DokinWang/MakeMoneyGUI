from PySide6.QtWidgets import QWidget, QMenu
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from common.utils import show_dialog
from components.bar import ProgressInfoBar
from ui_page.ui_page_two import Ui_page_two
from view.pages.page_back_test_handler import PageBackTestHandler

# 从ui文件生成的Ui_page_one类继承
class PageBackTest(QWidget, Ui_page_two):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.handler = PageBackTestHandler(self)
        self.form_init()
        self.bind_event()

    def form_init(self):
        self.stockBackTestTable.setColumnCount(11)
        self.stockBackTestTable.setHorizontalHeaderLabels(['股票代码', '名称', '买入价', '卖出价', '买入日期',
                                                           '卖出日期', '收益率（%）', '持有天数', '上证指数',
                                                           '当前市值(亿)', '当前市盈率'])
        self.stockBackTestTable.setColumnWidth(0, 80)
        self.stockBackTestTable.setColumnWidth(1, 80)
        self.stockBackTestTable.setColumnWidth(2, 60)
        self.stockBackTestTable.setColumnWidth(3, 60)
        self.stockBackTestTable.setColumnWidth(4, 100)
        self.stockBackTestTable.setColumnWidth(5, 100)
        self.stockBackTestTable.setColumnWidth(6, 80)
        self.stockBackTestTable.setColumnWidth(7, 80)
        self.stockBackTestTable.setColumnWidth(8, 80)
        self.stockBackTestTable.setColumnWidth(9, 80)
        self.stockBackTestTable.setColumnWidth(10, 80)
        self.stockBackTestTable.setAlternatingRowColors(True)

        # 让表头接收右键事件
        header = self.stockBackTestTable.horizontalHeader()
        header.setContextMenuPolicy(Qt.CustomContextMenu)
        header.customContextMenuRequested.connect(self.header_context_menu)

    def header_context_menu(self, pos):
        col = self.stockBackTestTable.horizontalHeader().logicalIndexAt(pos)

        menu = QMenu(self.stockBackTestTable)
        asc_act = QAction("⬆ 升序排列", self.stockBackTestTable)
        desc_act = QAction("⬇ 降序排列", self.stockBackTestTable)
        menu.addAction(asc_act)
        menu.addAction(desc_act)

        asc_act.triggered.connect(lambda: self.stockBackTestTable.sortByColumn(col, Qt.AscendingOrder))
        desc_act.triggered.connect(lambda: self.stockBackTestTable.sortByColumn(col, Qt.DescendingOrder))

        menu.exec(self.stockBackTestTable.horizontalHeader().viewport().mapToGlobal(pos))

    def bind_event(self):
        self.backTestBtn.clicked.connect(self.handler.back_test)

    def show_state_tooltip(self, title, content):
        self.loading_bar = ProgressInfoBar(title, content, self)
        self.loading_bar.show()

    def close_state_tooltip(self):
        try:
            if self.loading_bar:
                self.loading_bar.hide()
                self.loading_bar = None
        except RuntimeError as e:
            pass

    def clear_stock_table(self):
        self.stockBackTestTable.setRowCount(0)

    def on_common_error(self, msg):
        show_dialog(self, msg, '提示')
