# main.py
import os
import re
import pickle
import datetime
import random
import akshare as ak
import pandas as pd
from tqdm import tqdm
from typing import Tuple
import time
from typing import List, Dict, Tuple

# ----------- 全局参数 -----------
CACHE_DIR = "./cache"
os.makedirs(CACHE_DIR, exist_ok=True)

START_DATE = "20230103"          # 首次下载起点
ADJUST = "qfq"                   # 前复权
PE_LOW, PE_HIGH = 20, 45         # PE 过滤
BOLL_WINDOW = 20                 # 布林周期（基于 3 日线）
_sh_cache = None  # 保存已加载的 Series

def _get_sh_series() -> pd.Series:
    """延迟加载上证指数日线"""
    global _sh_cache
    if _sh_cache is None:
        df = load_or_update("000001", False, '')
        _sh_cache = df.set_index('日期')['收盘']
    return _sh_cache

#在买入 / 卖出判断前，先写一个小工具函数
def _sh_ok(dt):
    val = _get_sh_series().get(dt)
    return val is not None and 3180 <= val <= 3600



CACHE_DIR = "cache"  # 本地缓存根目录（可改成绝对路径）

def get_all_a_codes_from_cache(
    pe_low: float = 20,
    pe_high: float = 45
) -> List[str]:
    import warnings
    warnings.filterwarnings("ignore", category=FutureWarning)

    codes, names = [], {}
    pe_pattern = re.compile(r"\d{6}")

    for file in os.listdir(CACHE_DIR):
        # 只处理 6 位数字 .pkl 文件
        m = pe_pattern.fullmatch(file.split(".")[0])
        if not m:
            continue
        code = m.group(0)
        codes.append(code)

    return codes


# =============================================================================
# 1. 股票列表过滤
# =============================================================================
def get_all_a_codes(pe_low: float = 20, pe_high: float = 45) -> Tuple[List[str], Dict[str, str]]:
    spot = ak.stock_zh_a_spot_em()
    spot = spot[spot['代码'].str.fullmatch(r'\d{6}')]
    spot = spot[~spot['名称'].str.contains('ST', na=False)]
    spot = spot[~spot['代码'].str.startswith(('30', '83', '87', '43', '688', '689', '9'))]
    spot = spot[~spot['名称'].str.contains('指数', na=False)]

    # 剔除常见指数代码
    index_codes = {
        '000001', '000300', '000905', '399001',
        '399006', '399101', '399102', '399106',
        '399300', '399905'
    }
    spot = spot[~spot['代码'].isin(index_codes)]
    '''
    pe_col = next((c for c in spot.columns
                   if '市盈率' in str(c) or str(c).upper() == 'PE'), None)
    if pe_col is None:
        raise RuntimeError("找不到市盈率字段")
    spot = spot[spot[pe_col].notna() & spot[pe_col].between(pe_low, pe_high)]
    '''

    codes = spot['代码'].str.zfill(6).tolist()
    names = spot.set_index('代码')['名称'].to_dict()
    return codes, names

# =============================================================================
# 2. 本地缓存 + 增量更新
# =============================================================================
def _local_path(code: str) -> str:
    return os.path.join(CACHE_DIR, f"{code}.pkl")

import datetime
import pandas as pd
import akshare as ak

def last_trading_day() -> str:
    """返回最近一个交易日（YYYYMMDD），周末/节假日自动跳过"""
    today = datetime.date.today()
    # 向前多找 10 天，确保至少有一条交易日
    start_str = (today - datetime.timedelta(days=10)).strftime("%Y%m%d")
    end_str   = today.strftime("%Y%m%d")

    try:
        # 用上证指数接口拉最近所有日期
        df_idx = ak.stock_zh_index_daily(symbol="sh000001",
                                         start_date=start_str,
                                         end_date=end_str)
        if df_idx.empty:
            raise ValueError("空表")
        df_idx['date'] = pd.to_datetime(df_idx['date'])
        last_day = df_idx['date'].max()
        return last_day.strftime("%Y%m%d")
    except Exception:
        # 兜底：继续往前找，直到拿到一条
        offset = 1
        while True:
            candidate = today - datetime.timedelta(days=offset)
            if candidate.weekday() < 5:           # 周一到周五
                return candidate.strftime("%Y%m%d")
            offset += 1

def load_or_update(code: str, update: bool) -> pd.DataFrame:
    today_str = last_trading_day()
    pkl_path = _local_path(code)

    # 新增：上证指数 000001 的缓存
    if code == "000001":
        pkl_path = _local_path("sh_index")
        if os.path.exists(pkl_path):
            return pd.read_pickle(pkl_path)

        df_idx = ak.stock_zh_index_daily(symbol="sh000001")
        df_idx['日期'] = pd.to_datetime(df_idx['date'])
        df_idx = df_idx.rename(columns={'close': '收盘'})
        # 补齐缺失列
        df_idx['开盘'] = df_idx['收盘']  # 指数没有开高低，用收盘填充
        df_idx['最高'] = df_idx['收盘']
        df_idx['最低'] = df_idx['收盘']
        df_idx = df_idx[['日期', '开盘', '最高', '最低', '收盘']]
        df_idx.to_pickle(pkl_path)
        return df_idx

    # 本地已有则读
    if os.path.exists(pkl_path):
        df_old = pd.read_pickle(pkl_path)
        last_date = df_old['日期'].max() if not df_old.empty else \
                    pd.to_datetime(START_DATE) - pd.Timedelta(days=1)
    else:
        df_old = pd.DataFrame()
        last_date = pd.to_datetime(START_DATE) - pd.Timedelta(days=1)

    # 距离上次更新 ≥ 5 天（含）才更新
    if update and (pd.to_datetime(today_str).date() - last_date.date()).days >= 5:
        start_str = (last_date + pd.Timedelta(days=1)).strftime("%Y%m%d")
        print('{} need update, last:{}, start:{}, end{}'.format(code, last_date.date(), start_str, today_str))
        time.sleep(random.uniform(0.5, 1.5))
        df_new = ak.stock_zh_a_hist(symbol=code,
                                    period="daily",
                                    start_date=start_str,
                                    end_date=today_str,
                                    adjust=ADJUST)
        if not df_new.empty:
            df_new['日期'] = pd.to_datetime(df_new['日期'])
            df_old = pd.concat([df_old, df_new]).drop_duplicates('日期').sort_values('日期')
            df_old.to_pickle(pkl_path)
    return df_old

# =============================================================================
# 3. 策略回测（单只股票）
# =============================================================================
def boll_reverse_backtest(symbol: str,
                          period_s: str = "2023-01-16",
                          period_e: str = None,
                          window: int = 20) -> Tuple[pd.DataFrame, float]:
    if period_e is None:
        period_e = datetime.date.today().strftime("%Y-%m-%d")

    # 1) 取个股日 K（本地缓存）
    df = load_or_update(symbol, False)
    if df.empty:
        return pd.DataFrame(), None
    df = df.sort_values('日期').reset_index(drop=True)

    # 2) 合成 3 日线
    #df['trade_no'] = df.index // 3
    df['trade_no'] = pd.to_datetime(df['日期']).dt.to_period('W').dt.start_time  # 周一

    three_day_df = (
        df.groupby(df['trade_no'])
          .agg(日期=('日期', 'last'),
               开盘=('开盘', 'first'),
               收盘=('收盘', 'last'),
               最高=('最高', 'max'),
               最低=('最低', 'min'))
          .reset_index(drop=True)
    )

    # 3) 布林线
    three_day_df['MA20']  = three_day_df['收盘'].rolling(window).mean()
    three_day_df['STD']   = three_day_df['收盘'].rolling(window).std()
    three_day_df['Upper'] = three_day_df['MA20'] + 2 * three_day_df['STD']
    three_day_df['Lower'] = three_day_df['MA20'] - 2 * three_day_df['STD']

    # 4) 标记突破/跌破
    three_day_df['Break_Upper'] = three_day_df['最高'] >= three_day_df['Upper']
    three_day_df['Break_Lower'] = three_day_df['最低'] <= three_day_df['Lower']

    # 5) 时间过滤
    period_s = pd.to_datetime(period_s)
    period_e = pd.to_datetime(period_e)
    sub = three_day_df[
        (three_day_df['日期'] >= period_s) &
        (three_day_df['日期'] <= period_e)
    ].reset_index(drop=True)

    upper_dates = sub.loc[sub['Break_Upper'], '日期'].tolist()
    lower_dates = sub.loc[sub['Break_Lower'], '日期'].tolist()

    trades = []
    for up_date in reversed(upper_dates):
        lows_after = [d for d in lower_dates if d > up_date]
        if not lows_after:
            continue
        low_date = min(lows_after)

        # 区间干净检查
        mids = sub[(sub['日期'] > up_date) & (sub['日期'] < low_date)]
        if mids['Break_Upper'].any() or mids['Break_Lower'].any():
            continue

        # 买入日
        buy_bar = sub[sub['日期'] == low_date].iloc[0]
        if not _sh_ok(buy_bar['日期']):
            continue  # 上证不在区间，跳过

        # 卖出日
        sell_candidates = sub[sub['日期'] > low_date]
        cond = sell_candidates['最高'] >= sell_candidates['MA20']
        if not cond.any():
            continue
        sell_bar = sell_candidates[cond].iloc[0]
        if not _sh_ok(sell_bar['日期']):
            continue  # 上证不在区间，跳过

        buy_price = buy_bar['Lower']
        sell_price = sell_bar['MA20']
        trades.append({
            '股票代码': symbol,
            '买入日期': buy_bar['日期'].date(),
            '买入价': buy_price,
            '卖出日期': sell_bar['日期'].date(),
            '卖出价': sell_price,
            '收益率': (sell_price - buy_price) / buy_price,
            '持有天数': (sell_bar['日期'] - buy_bar['日期']).days
        })

    df_trades = pd.DataFrame(trades)
    return df_trades, df_trades['收益率'].mean() if not df_trades.empty else None
