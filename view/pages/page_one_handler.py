from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget

from api.api import demo_api
from common.utils import show_dialog
from workers.TaskManager import task_manager
from view.policy.stock import *

class PageOneHandler(QObject):
    progress_signal = Signal(int)

    def __init__(self, parent: 'PageOne'):
        super().__init__(parent)
        self._parent = parent
        self.progress_signal.connect(self.update_progress)

    def load_local_stock(self):
        codes = get_all_stock_from_cache()
        total = len(codes)
        cnt = 0
        try:
            self._parent.show_state_tooltip('正在加载', '请稍后...')
            self._parent.clear_stock_table()
            self._parent.updateProgress.setValue(0)
            QApplication.processEvents()
            for code in codes:
                df = load_or_update(code, False)

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
                    row_position = self._parent.stockUpdataTable.rowCount()
                    self._parent.stockUpdataTable.insertRow(row_position)
                    self._parent.stockUpdataTable.setItem(row_position, 0, QTableWidgetItem(code))
                    self._parent.stockUpdataTable.setItem(row_position, 1, QTableWidgetItem(latest_date_str))
                    self._parent.stockUpdataTable.setItem(row_position, 2, QTableWidgetItem(str(latest_data_row['开盘'])))
                    self._parent.stockUpdataTable.setItem(row_position, 3, QTableWidgetItem(str(latest_data_row['最高'])))
                    self._parent.stockUpdataTable.setItem(row_position, 4, QTableWidgetItem(str(latest_data_row['最低'])))
                    self._parent.stockUpdataTable.setItem(row_position, 5, QTableWidgetItem(str(latest_data_row['收盘'])))
                    self._parent.stockUpdataTable.scrollToBottom()
                    cnt = cnt + 1
                    progress = cnt * 100 / total
                    self._parent.updateProgress.setValue(int(progress))
                    QApplication.processEvents()
            self._parent.close_state_tooltip()

        except RuntimeError as e:
            self._parent.close_state_tooltip()
            self._parent.on_common_error(str(e))
            show_dialog(self._parent, '加载失败')

    def update_stock_task(self):
        codes,names = get_all_stock()
        total = len(codes)
        cnt = 0
        for code in codes:
            df = load_or_update(code, True)

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
                row_position = self._parent.stockUpdataTable.rowCount()
                self._parent.stockUpdataTable.insertRow(row_position)
                self._parent.stockUpdataTable.setItem(row_position, 0, QTableWidgetItem(code))
                self._parent.stockUpdataTable.setItem(row_position, 1, QTableWidgetItem(latest_date_str))
                self._parent.stockUpdataTable.setItem(row_position, 2, QTableWidgetItem(str(latest_data_row['开盘'])))
                self._parent.stockUpdataTable.setItem(row_position, 3, QTableWidgetItem(str(latest_data_row['最高'])))
                self._parent.stockUpdataTable.setItem(row_position, 4, QTableWidgetItem(str(latest_data_row['最低'])))
                self._parent.stockUpdataTable.setItem(row_position, 5, QTableWidgetItem(str(latest_data_row['收盘'])))
                self._parent.stockUpdataTable.scrollToBottom()
                cnt = cnt + 1
                progress = cnt * 100 / total
                #self._parent.updateProgress.setValue(int(progress))
                self.progress_signal.emit(progress)

    def update_stock(self):
        try:
            self._parent.show_state_tooltip('正在加载', '请稍后...')
            self._parent.clear_stock_table()
            self._parent.updateProgress.setValue(0)
            task_manager.submit_task(
                self.update_stock_task,
                on_success=self.update_async_success,
                on_error=lambda msg: self._parent.on_common_error(msg)
            )
        except RuntimeError as e:
            self._parent.close_state_tooltip()
            self._parent.on_common_error(str(e))

    def clear_stock(self):
        self._parent.clear_stock_table()

    def update_async_success(self, result):
        self._parent.close_state_tooltip()
        show_dialog(self._parent, '更新成功')

    def update_progress(self, progress):
        self._parent.updateProgress.setValue(progress)