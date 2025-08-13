import sys

from PySide6.QtCore import QRect
from PySide6.QtGui import QIcon

from qfluentwidgets import FluentWindow, NavigationItemPosition

from components.icon import MyIcon
from qfluentwidgets import FluentIcon as FIF
from view.pages.page_stock_update import PageStockUpdate
from view.pages.page_back_test import PageBackTest
from view.pages.setting_page import SettingInterface


class MainWindow(FluentWindow):
    """ 主界面 """

    def __init__(self):
        super().__init__()
        if sys.platform == "darwin":
            self.navigationInterface.panel.setReturnButtonVisible(False)
            self.navigationInterface.panel.topLayout.setContentsMargins(4, 24, 4, 0)
        else:
            self.navigationInterface.setExpandWidth(150)
        # 创建子界面，实际使用时将 Widget 换成自己的子界面
        self.settingInterface = SettingInterface(self)

        self.pageStockUpdate = PageStockUpdate(self)
        self.pageBackTest = PageBackTest(self)
        self.init_navigation()
        self.init_window()

    def systemTitleBarRect(self, size):
        return QRect(0, 0, 75, size.height())

    def init_navigation(self):
        # 新增页面需要再此处添加
        sub_interface_list = [
            {'widget': self.pageStockUpdate, 'icon': MyIcon.EXCEL, 'text': '数据管理'},
            {'widget': self.pageBackTest, 'icon': MyIcon.CLICK, 'text': '数据回测'}
        ]
        for item in sub_interface_list:
            self.addSubInterface(item['widget'], item['icon'], item['text'])

        self.addSubInterface(self.settingInterface, FIF.SETTING, '设置', NavigationItemPosition.BOTTOM)

    def init_window(self):
        if sys.platform != "darwin":
            self.setWindowIcon(QIcon(':/resource/images/logo.png'))
            self.setWindowTitle('屎里淘金V2.0')
        self.resize(1200, 800)
        # 把窗口放在屏幕中间
        self.move((self.screen().size().width() - self.width()) / 2,
                  (self.screen().size().height() - self.height()) / 2)