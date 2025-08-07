from PySide6.QtCore import QObject

from api.api import demo_api
from common.utils import show_dialog
from workers.TaskManager import task_manager
from view.policy.stock import *

class PageOneHandler(QObject):
    def __init__(self, parent: 'PageOne'):
        super().__init__(parent)
        self._parent = parent

    def do_something(self):
        #codes,names = get_all_stock()
        codes = get_all_stock_from_cache()
        #print(codes)
        #show_dialog (self._parent, 'do something')
        #self._parent.textEdit_codes.setText(codes)

    def do_something_async(self):
        self._parent.show_state_tooltip('正在加载', '请稍后...')
        try:
            task_manager.submit_task(
                demo_api.sleep, args=(2,),
                on_success=self.on_do_something_async_success,
                on_error=lambda msg: self._parent.on_common_error(msg)
            )
        except RuntimeError as e:
            self._parent.close_state_tooltip()
            self._parent.on_common_error(str(e))

    def on_do_something_async_success(self, result):
        self._parent.close_state_tooltip()
        show_dialog(self._parent, 'do something async success')
