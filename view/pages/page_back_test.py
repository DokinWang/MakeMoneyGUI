from PySide6.QtWidgets import QWidget
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
        self.stockBackTestTable.setColumnCount(9)
        self.stockBackTestTable.setHorizontalHeaderLabels(['股票代码', '名称', '买入价', '卖出价', '买入日期',
                                                           '卖出日期', '收益率', '持有天数', '上证指数'])
        self.stockBackTestTable.setColumnWidth(0, 80)
        self.stockBackTestTable.setColumnWidth(1, 100)
        self.stockBackTestTable.setColumnWidth(2, 100)
        self.stockBackTestTable.setColumnWidth(3, 100)
        self.stockBackTestTable.setColumnWidth(4, 100)
        self.stockBackTestTable.setColumnWidth(5, 100)
        self.stockBackTestTable.setColumnWidth(6, 100)
        self.stockBackTestTable.setColumnWidth(7, 100)
        self.stockBackTestTable.setColumnWidth(8, 100)
        self.stockBackTestTable.setAlternatingRowColors(True)

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