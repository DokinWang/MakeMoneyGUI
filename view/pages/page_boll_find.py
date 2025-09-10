from PySide6.QtWidgets import QWidget, QMenu
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from common.utils import show_dialog
from components.bar import ProgressInfoBar
from ui_page.ui_page_three import Ui_page_three
from view.pages.page_boll_find_handler import PageBollFindHandler

# 从ui文件生成的Ui_page_one类继承
class PageBollFind(QWidget, Ui_page_three):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.handler = PageBollFindHandler(self)
        self.form_init()
        self.bind_event()

    def form_init(self):
        self.stockBollTable.setColumnCount(6)
        self.stockBollTable.setHorizontalHeaderLabels(['股票代码', '名称', '当前市值(亿)', '当前市盈率', '日期', '价格'])
        self.stockBollTable.setColumnWidth(0, 80)   #股票代码
        self.stockBollTable.setColumnWidth(1, 80)   #名称
        self.stockBollTable.setColumnWidth(2, 80)   #当前市值
        self.stockBollTable.setColumnWidth(3, 80)  #市盈率
        self.stockBollTable.setColumnWidth(4, 80)  #日期
        self.stockBollTable.setColumnWidth(5, 80)  #价格
        self.stockBollTable.setAlternatingRowColors(True)

    def bind_event(self):
        self.bollFindBtn.clicked.connect(self.handler.find_boll_codes)

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
        self.stockBollTable.setRowCount(0)

    def on_common_error(self, msg):
        show_dialog(self, msg, '提示')
