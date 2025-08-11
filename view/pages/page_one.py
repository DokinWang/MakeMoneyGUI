from PySide6.QtWidgets import QWidget

from common.utils import show_dialog
from components.bar import ProgressInfoBar
from ui_page.ui_page_one import Ui_page_one
from view.pages.page_one_handler import PageOneHandler

class PageOne(QWidget, Ui_page_one):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.loading_bar = None
        self.setupUi(self)
        self.handler = PageOneHandler(self)
        self.bind_event()
        self.stockUpdataTable.setColumnCount(6)
        self.stockUpdataTable.setHorizontalHeaderLabels(['股票代码', '日期', '开盘', '最高', '最低', '收盘'])
        self.stockUpdataTable.setColumnWidth(0, 100)
        self.stockUpdataTable.setColumnWidth(1, 150)
        self.stockUpdataTable.setColumnWidth(2, 100)
        self.stockUpdataTable.setColumnWidth(3, 100)
        self.stockUpdataTable.setColumnWidth(4, 100)
        self.stockUpdataTable.setColumnWidth(5, 100)
        self.stockUpdataTable.setAlternatingRowColors(True)

    def bind_event(self):
        self.loadLocalBtn.clicked.connect(self.handler.load_local_stock)
        self.updateLocalBtn.clicked.connect(self.handler.update_stock)
        self.updateClearBtn.clicked.connect(self.handler.clear_stock)

    def show_state_tooltip(self, title, content):
        self.loading_bar = ProgressInfoBar(title, content, self)
        self.loading_bar.show()

    def close_state_tooltip(self):
        if self.loading_bar:
            self.loading_bar.hide()
            self.loading_bar = None

    def clear_stock_table(self):
        self.stockUpdataTable.setRowCount(0)

    def on_common_error(self, msg):
        show_dialog(self, msg, '提示')
