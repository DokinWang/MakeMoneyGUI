from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget

from api.api import demo_api
from common.utils import show_dialog
from workers.TaskManager import task_manager
from view.policy.stock import *

class PageOneHandler(QObject):
    progress_signal = Signal(int)
    row_ready = Signal(str, str, pd.Series)

    def __init__(self, parent: 'PageOne'):
        super().__init__(parent)
        self._parent = parent
        self.progress_signal.connect(self.set_progress)
        self.row_ready.connect(self.add_row_to_table)

    def load_show_stock_task(self, codes, update=False):
        total = len(codes)
        cnt = 0
        try:
            self.progress_signal.emit(0)
            for code in codes:
                df = load_or_update(code, update)

                # 确保日期列是 datetime 类型（虽然代码中已经转换过了，但这里再确认一下）
                df['日期'] = pd.to_datetime(df['日期'])

                # 找到最新一天的日期
                latest_date = df['日期'].max()

                # 筛选出最新一天的数据
                latest_data = df[df['日期'] == latest_date]

                # 获取最新一天的数据，包括 '日期', '开盘', '最高', '最低', '收盘'
                latest_data = latest_data[['日期', '开盘', '最高', '最低', '收盘']]
                if not latest_data.empty:
                    latest_data_row = latest_data.iloc[0]
                    # 将日期转换为字符串格式
                    latest_date_str = latest_data_row['日期'].strftime("%Y-%m-%d")
                    self.row_ready.emit(code, latest_date_str, latest_data_row)
                    cnt = cnt + 1
                    progress = cnt * 100 / total
                    self.progress_signal.emit(progress)
        except RuntimeError as e:
            show_dialog(self._parent, '加载失败')

    def load_local_stock(self):
        try:
            codes = get_all_stock_from_cache()
            self._parent.show_state_tooltip('正在加载', '请稍后...')
            self._parent.clear_stock_table()
            self._parent.updateProgress.setValue(0)
            task_manager.submit_task(
                self.load_show_stock_task,args=(codes,),
                kwargs={'update': False},
                on_success=self.load_stock_success,
                on_error=lambda msg: self._parent.on_common_error(msg)
            )
        except RuntimeError as e:
            self._parent.close_state_tooltip()
            self._parent.on_common_error(str(e))

    def update_stock(self):
        try:
            codes,names = get_all_stock()
            self._parent.show_state_tooltip('正在更新', '请稍后...')
            self._parent.clear_stock_table()
            self._parent.updateProgress.setValue(0)
            task_manager.submit_task(
                self.load_show_stock_task,args=(codes,),
                kwargs={'update': True},
                on_success=self.update_stock_success,
                on_error=lambda msg: self._parent.on_common_error(msg)
            )
        except RuntimeError as e:
            self._parent.close_state_tooltip()
            self._parent.on_common_error(str(e))

    def clear_stock(self):
        self._parent.clear_stock_table()

    def load_stock_success(self):
        self._parent.close_state_tooltip()
        show_dialog(self._parent, '加载成功')

    def update_stock_success(self, result):
        self._parent.close_state_tooltip()
        show_dialog(self._parent, '更新成功')

    def set_progress(self, progress):
        self._parent.updateProgress.setValue(progress)

    def add_row_to_table(self, code: str, date_str: str, row: pd.Series):
        table = self._parent.stockUpdataTable
        pos = table.rowCount()
        table.insertRow(pos)
        table.setItem(pos, 0, QTableWidgetItem(code))
        table.setItem(pos, 1, QTableWidgetItem(date_str))
        table.setItem(pos, 2, QTableWidgetItem(str(row['开盘'])))
        table.setItem(pos, 3, QTableWidgetItem(str(row['最高'])))
        table.setItem(pos, 4, QTableWidgetItem(str(row['最低'])))
        table.setItem(pos, 5, QTableWidgetItem(str(row['收盘'])))
        table.scrollToBottom()