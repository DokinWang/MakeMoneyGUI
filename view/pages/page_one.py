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

    def bind_event(self):
        self.pushButton.clicked.connect(self.handler.do_something) # 绑定事件
        self.pushButton_2.clicked.connect(self.handler.do_something_async)

    def show_state_tooltip(self, title, content):
        self.loading_bar = ProgressInfoBar(title, content, self)
        self.loading_bar.show()

    def close_state_tooltip(self):
        if self.loading_bar:
            self.loading_bar.hide()
            self.loading_bar = None

    def on_common_error(self, msg):
        show_dialog(self, msg, '提示')
