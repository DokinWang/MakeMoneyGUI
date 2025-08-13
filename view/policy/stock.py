

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
_stock_code_name_dict = None    # 全局变量，存储股票代码与名称的字典
STOCK_CODE_NAME_DICT_FILE = os.path.join(CACHE_DIR, "stock_code_name_dict.pkl")

# 全局变量，存储股票代码到 DataFrame 的映射
_global_stock_data_dict: Dict[str, pd.DataFrame] = None

def get_cache_dir() -> str:
    return CACHE_DIR

def get_sh_series() -> pd.Series:
    """延迟加载上证指数日线"""
    global _sh_cache
    if _sh_cache is None:
        df = load_or_update("000001", False)
        _sh_cache = df.set_index('日期')['收盘']
    return _sh_cache

def _local_path(code: str) -> str:
    return os.path.join(CACHE_DIR, f"{code}.pkl")

def last_trading_day() -> str:
    """获取上一个交易日的日期"""
    today = pd.Timestamp.today()
    # 如果当前时间是下午3点之前，回退到上一个交易日
    if today.hour < 15:
        today -= pd.Timedelta(days=1)
    # 如果今天是周末，回退到上一个周五
    while today.weekday() >= 5:  # 周六或周日
        today -= pd.Timedelta(days=1)
    return today.strftime("%Y%m%d")
    '''
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
    '''

def load_or_update_stock_code_name_dict(update: bool = False, ak_spot = None):
    global _stock_code_name_dict
    if update is False and os.path.exists(STOCK_CODE_NAME_DICT_FILE):
        # 如果文件存在，直接加载
        print("加载本地股票代码与名称字典库文件...")
        _stock_code_name_dict = pd.read_pickle(STOCK_CODE_NAME_DICT_FILE)
    else:
        # 如果文件不存在，通过 ak.stock_zh_a_spot_em() 获取数据并保存
        print("本地股票代码与名称字典库文件不存在，正在获取最新数据...")
        if ak_spot is None:
            spot = ak.stock_zh_a_spot_em()
        else:
            spot = ak_spot
        spot = spot[spot['代码'].str.fullmatch(r'\d{6}')]  # 确保代码是6位数字

        # 提取股票代码和名称
        codes = spot['代码'].str.zfill(6).tolist()
        names = spot.set_index('代码')['名称'].to_dict()

        # 保存到全局变量和文件
        _stock_code_name_dict = pd.Series(names, name="股票名称")
        _stock_code_name_dict.to_pickle(STOCK_CODE_NAME_DICT_FILE)
        print("股票代码与名称字典库文件已保存到本地。")

#更新个股信息,update为True才更新
def load_or_update(code: str, update: bool) -> pd.DataFrame:
    today_str = last_trading_day()
    pkl_path = _local_path(code)

    # 加载或更新股票代码与名称字典库文件
    if _stock_code_name_dict is None:
        load_or_update_stock_code_name_dict()

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

    if update and (pd.to_datetime(today_str).date() - last_date.date()).days >= 1:
        start_str = (last_date + pd.Timedelta(days=1)).strftime("%Y%m%d")
        print('{} need update, last:{}, start:{}, end{}'.format(code, last_date.date(), start_str, today_str))
        time.sleep(random.uniform(0.8, 1.6))
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

def stock_name(code: str) -> str:
    if _stock_code_name_dict is None:
        load_or_update_stock_code_name_dict()
    if _stock_code_name_dict is None:
        return None
    return _stock_code_name_dict[code]

def get_all_stock_from_cache() -> Tuple[List[str], Dict[str, str]]:
    import warnings
    warnings.filterwarnings("ignore", category=FutureWarning)

    codes, names = [], {}
    pe_pattern = re.compile(r"\d{6}")
    dir = get_cache_dir()

    if _stock_code_name_dict is None:
        load_or_update_stock_code_name_dict()

    for file in os.listdir(dir):
        # 只处理 6 位数字 .pkl 文件
        m = pe_pattern.fullmatch(file.split(".")[0])
        if not m:
            continue
        code = m.group(0)
        codes.append(code)
        if code in _stock_code_name_dict.index:
            names[code] = _stock_code_name_dict[code]
    return codes, names

def get_all_stock() -> Tuple[List[str], Dict[str, str]]:
    spot = ak.stock_zh_a_spot_em()

    load_or_update_stock_code_name_dict(update=True, ak_spot=spot)

    spot = spot[spot['代码'].str.fullmatch(r'\d{6}')]
    spot = spot[~spot['名称'].str.contains('ST', na=False)]
    spot = spot[~spot['代码'].str.startswith(('30', '83', '87', '43', '688', '689', '9'))]
    #spot = spot[~spot['名称'].str.contains('指数', na=False)]
    # 只排除名称含“指数”且代码不是 000001 的行
    spot = spot[~(spot['名称'].str.contains('指数', na=False) & (spot['代码'] != '000001'))]

    # 剔除常见指数代码
    index_codes = {
        '000300', '000905', '399001',
        '399006', '399101', '399102',
        '399106', '399300', '399905'
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

def get_stock_data(update: bool = False) -> Dict[str, pd.DataFrame]:
    global _global_stock_data_dict
    if _global_stock_data_dict is None:
        _global_stock_data_dict = {}
        codes, _ = get_all_stock_from_cache()
        for code in codes:
            _global_stock_data_dict[code] = load_or_update(code, update)
    return _global_stock_data_dict