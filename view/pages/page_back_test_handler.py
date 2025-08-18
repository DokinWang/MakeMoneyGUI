from PySide6.QtCore import Qt , QObject, Signal
from PySide6.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
from typing import List, Dict, Tuple
from api.api import demo_api
import pandas as pd
from common.utils import show_dialog
from workers.TaskManager import task_manager
from view.policy.stock import get_stock_data
from view.policy.boll_break import boll_reverse_backtest
#from common.my_logger import my_logger as logger

class PageBackTestHandler(QObject):
    progress_signal = Signal(int)
    back_reverse_data_signal = Signal(pd.DataFrame)
    back_reverse_fail = Signal()

    def __init__(self, parent: 'PageBackTest'):
        super().__init__(parent)
        self._parent = parent
        self.all_res = []
        self.progress_signal.connect(self.set_progress)
        self.back_reverse_data_signal.connect(self.back_reverse_data_handle)
        self.back_reverse_fail.connect(self.back_reverse_test_fail)

    def boll_reverse_backtest_task(self,
                                   policySelect :int,   # 0:三日线 1:周线 2:月线
                                   sellPos: int,        # 0:中轨 1:上轨
                                   upperBreak: bool,
                                   startTime: str,
                                   endTime: str,
                                   shMin: int,
                                   shMax: int):
        self.progress_signal.emit(0)
        stock_data = get_stock_data()
        if stock_data is not None:
            total = len(stock_data)
            cnt = 0
            for code, df in stock_data.items():
                df_trades = boll_reverse_backtest(code, df, policySelect, sellPos, upperBreak, startTime, endTime, shMin, shMax)
                if df_trades.empty:
                    continue
                self.back_reverse_data_signal.emit(df_trades)
                cnt = cnt + 1
                progress = cnt * 100 / total
                self.progress_signal.emit(progress)
            self.progress_signal.emit(100)
        else:
            self.back_reverse_fail.emit()
                #all_res.append(df_trades)
        #combined_df = pd.concat(all_res, ignore_index=True)
        #sorted_df = combined_df.sort_values(by='收益率', ascending=False)  # 按照收益率降序排列
        #self.data_signal.emit(sorted_df)

    def back_test(self):
        self.set_progress(0)
        policySelect = self._parent.policySelect.currentIndex()
        sellPos = self._parent.sellPos.currentIndex()
        upperBreak = self._parent.breakUp.isChecked()
        startTime = ''
        endTime = ''
        shMin = 0
        shMax = 0
        try:
            startTime = self._parent.startTime.date().toString("yyyyMMdd")
            endTime = self._parent.endTime.date().toString("yyyyMMdd")
            shMin = int(self._parent.shMin.text())
            shMax = int(self._parent.shMax.text())
        except ValueError:
            show_dialog(self._parent, '输入了非法数据')
            return

        try:
            self._parent.show_state_tooltip('正在回测', '请稍后...')
            self._parent.clear_stock_table()
            self.all_res = []
            task_manager.submit_task(
                self.boll_reverse_backtest_task, args=(policySelect, sellPos, upperBreak, startTime, endTime, shMin, shMax),
                kwargs={},
                on_success=self.back_reverse_test_success, 
                on_error=lambda msg: self._parent.on_common_error(msg)
            )
        except RuntimeError as e:
            self._parent.close_state_tooltip()
            self._parent.on_common_error(str(e))

    def back_reverse_data_handle(self, df: pd.DataFrame):
        table = self._parent.stockBackTestTable
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

                table.setItem(pos, 2, QTableWidgetItem(str(row['买入价'])))
                table.item(pos, 2).setTextAlignment(Qt.AlignCenter)  # 买入价居中

                table.setItem(pos, 3, QTableWidgetItem(str(row['卖出价'])))
                table.item(pos, 3).setTextAlignment(Qt.AlignCenter)  # 卖出价居中

                table.setItem(pos, 4, QTableWidgetItem(row['买入日期']))
                table.item(pos, 4).setTextAlignment(Qt.AlignCenter)  # 买入日期居中

                table.setItem(pos, 5, QTableWidgetItem(row['卖出日期']))
                table.item(pos, 5).setTextAlignment(Qt.AlignCenter)  # 卖出日期居中

                table.setItem(pos, 6, QTableWidgetItem(f"{row['收益率']:.2%}"))
                table.item(pos, 6).setTextAlignment(Qt.AlignCenter)  # 收益率居中

                table.setItem(pos, 7, QTableWidgetItem(str(row['持有天数'])))
                table.item(pos, 7).setTextAlignment(Qt.AlignCenter)  # 持有天数居中

                table.setItem(pos, 8, QTableWidgetItem(str(row['上证指数'])))
                table.item(pos, 8).setTextAlignment(Qt.AlignCenter)  # 上证指数居中

                table.scrollToBottom()

    def set_progress(self, progress):
        self._parent.backTestProgress.setValue(progress)

    def back_reverse_test_fail(self):
        self._parent.close_state_tooltip()
        if not self.all_res:
            show_dialog(self._parent, '没有任何交易记录')

    def back_reverse_test_success(self):
        self._parent.close_state_tooltip()
        if not self.all_res:
            show_dialog(self._parent, '回测结束, 没有任何交易记录')
            return
        result = pd.concat(self.all_res, ignore_index=True)
        avg_ret = result['收益率'].mean()
        avg_days = result['持有天数'].mean()

        day_ret = round(avg_ret * 100 / avg_days, 3)
        avg_ret = round(avg_ret * 100, 2)
        avg_days = round(avg_days, 2)
        
        self._parent.day_ret.setText(str(day_ret))
        self._parent.avg_ret.setText(str(avg_ret))
        self._parent.avg_days.setText(str(avg_days))
        show_dialog(self._parent, '回测结束')
