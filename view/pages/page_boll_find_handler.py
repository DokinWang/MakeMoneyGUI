from PySide6.QtCore import Qt , QObject, Signal
from PySide6.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
from typing import List, Dict, Tuple
from api.api import demo_api
import pandas as pd
from common.utils import show_dialog
from workers.TaskManager import task_manager
from view.policy.stock import get_stock_data, get_current_stock_info
from view.policy.boll_break import boll_find
#from common.my_logger import my_logger as logger

class PageBollFindHandler(QObject):
    progress_signal = Signal(int)
    boll_find_data_signal = Signal(pd.DataFrame)
    boll_find_fail_signal = Signal()

    def __init__(self, parent: 'PageBollFind'):
        super().__init__(parent)
        self._parent = parent
        self.all_res = []
        self.progress_signal.connect(self.set_progress)
        self.boll_find_data_signal.connect(self.boll_find_data_handle)
        self.boll_find_fail_signal.connect(self.boll_find_fail)

    def boll_find_task(self,
                       policySelect :int,   # 0:三日线 1:周线 2:月线
                       upperBreak: bool,
                       marketValMin: int,
                       marketValMax: int,
                       peRatioMin: int,
                       peRatioMax: int):
        self.progress_signal.emit(0)
        stock_data = get_stock_data()
        curr_data = get_current_stock_info(update=True)
        if stock_data is not None:
            total = len(stock_data)
            cnt = 0
            for code, df in stock_data.items():
                df_trades = boll_find(code, df, curr_data, policySelect,  upperBreak,
                                      marketValMin, marketValMax, peRatioMin, peRatioMax)
                if df_trades.empty:
                    continue
                self.boll_find_data_signal.emit(df_trades)
                cnt = cnt + 1
                progress = cnt * 100 / total
                self.progress_signal.emit(progress)
            self.progress_signal.emit(100)
        else:
            self.boll_find_fail_signal.emit()

    def find_boll_codes(self):
        self.set_progress(0)
        policySelect = self._parent.policySelect.currentIndex()
        upperBreak = self._parent.breakUp.isChecked()
        marketValMin = 0
        marketValMax = 0
        peRatioMin = 0
        peRatioMax = 0
        try:
            marketValMin = int(self._parent.marketValMin.text())
            marketValMax = int(self._parent.marketValMax.text())
            peRatioMin = int(self._parent.peRatioMin.text())
            peRatioMax = int(self._parent.peRatioMax.text())
        except ValueError:
            show_dialog(self._parent, '输入了非法数据')
            return

        try:
            self._parent.show_state_tooltip('正在查找', '请稍后...')
            self._parent.clear_stock_table()
            self.all_res = []
            task_manager.submit_task(
                self.boll_find_task, args=(policySelect, upperBreak,
                                            marketValMin, marketValMax, peRatioMin, peRatioMax),
                kwargs={},
                on_success=self.boll_find_success, 
                on_error=lambda msg: self._parent.on_common_error(msg)
            )
        except RuntimeError as e:
            self._parent.close_state_tooltip()
            self._parent.on_common_error(str(e))

    def boll_find_data_handle(self, df: pd.DataFrame):
        table = self._parent.stockBollTable
        if not df.empty:
            self.all_res.append(df)
            for index, row in df.iterrows():
                pos = table.rowCount()
                table.insertRow(pos)

                # 创建并设置每个单元格的内容和居中对齐
                table.setItem(pos, 0, QTableWidgetItem(row['代码']))
                table.item(pos, 0).setTextAlignment(Qt.AlignCenter)  # 股票代码居中

                table.setItem(pos, 1, QTableWidgetItem(row['名称']))
                table.item(pos, 1).setTextAlignment(Qt.AlignCenter)  # 股票名称居中

                table.setItem(pos, 2, QTableWidgetItem(str(row['市值'])))
                table.item(pos, 2).setTextAlignment(Qt.AlignCenter)  # 市值居中

                table.setItem(pos, 3, QTableWidgetItem(str(row['市盈率'])))
                table.item(pos, 3).setTextAlignment(Qt.AlignCenter)  # 市盈率居中

                table.setItem(pos, 4, QTableWidgetItem(str(row['日期'])))
                table.item(pos, 4).setTextAlignment(Qt.AlignCenter)  # 日期居中

                table.setItem(pos, 5, QTableWidgetItem(str(row['价格'])))
                table.item(pos, 5).setTextAlignment(Qt.AlignCenter)  # 价格居中
                
                table.scrollToBottom()

    def set_progress(self, progress):
        self._parent.backTestProgress.setValue(progress)

    def boll_find_fail(self):
        self._parent.close_state_tooltip()
        if not self.all_res:
            show_dialog(self._parent, '查找结束, 没有符合策略的股票')

    def boll_find_success(self):
        self._parent.close_state_tooltip()
        if not self.all_res:
            show_dialog(self._parent, '查找结束, 没有符合策略的股票')
            return
        show_dialog(self._parent, '查找结束')
