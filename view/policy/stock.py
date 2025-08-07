

import os
import akshare as ak
import pandas as pd
import time
import re
import random
import datetime
from typing import List, Dict, Tuple

CACHE_DIR = "./cache"
os.makedirs(CACHE_DIR, exist_ok=True)

# ----------- 全局参数 -----------
START_DATE = "20230103"          # 首次下载起点
ADJUST = "qfq"                   # 前复权
PE_LOW, PE_HIGH = 20, 45         # PE 过滤
BOLL_WINDOW = 20                 # 布林周期（基于 3 日线）
_sh_cache = None  # 保存已加载的 Series

def get_cache_dir() -> str:
    return CACHE_DIR

def get_sh_series() -> pd.Series:
    """延迟加载上证指数日线"""
    global _sh_cache
    if _sh_cache is None:
        df = load_or_update("000001", True)
        _sh_cache = df.set_index('日期')['收盘']
    return _sh_cache


def _local_path(code: str) -> str:
    return os.path.join(CACHE_DIR, f"{code}.pkl")

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

#更新个股信息,update为True才更新
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

def get_all_stock_from_cache() -> List[str]:
    import warnings
    warnings.filterwarnings("ignore", category=FutureWarning)

    codes, names = [], {}
    pe_pattern = re.compile(r"\d{6}")
    dir = get_cache_dir()

    for file in os.listdir(dir):
        # 只处理 6 位数字 .pkl 文件
        m = pe_pattern.fullmatch(file.split(".")[0])
        if not m:
            continue
        code = m.group(0)
        codes.append(code)

    return codes

def get_all_stock(pe_low: float = 20, pe_high: float = 45) -> Tuple[List[str], Dict[str, str]]:
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