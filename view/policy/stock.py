

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

_curr_all_stock = None
_all_stock_file_path = "cache/all_stock.pkl"
def get_cache_dir() -> str:
    return CACHE_DIR

def get_sh_series() -> pd.Series:
    """延迟加载上证指数日线"""
    global _sh_cache
    if _sh_cache is None:
        df = load_or_update("000001", False, '')
        _sh_cache = df.set_index('日期')['收盘']
    return _sh_cache

def update_sh():
    global _sh_cache
    df = load_or_update("000001", True, last_trading_day())
    _sh_cache = df.set_index('日期')['收盘']

def get_current_stock_info(update: bool = False):
    global _curr_all_stock

    if _curr_all_stock is not None:
        return _curr_all_stock

    # 检查缓存文件是否存在
    if os.path.exists(_all_stock_file_path):
        # 加载缓存文件
        _curr_all_stock = pd.read_pickle(_all_stock_file_path)
        # 检查数据是否为当天的
        if not update and _is_today_data(_curr_all_stock):
            return _curr_all_stock

    # 如果缓存文件不存在或数据不是当天的，更新数据
    _curr_all_stock = ak.stock_zh_a_spot_em()
    # 添加日期列
    _curr_all_stock['日期'] = datetime.datetime.now().strftime('%Y-%m-%d')  # 使用 datetime.now()
    # 保存到缓存文件
    os.makedirs(os.path.dirname(_all_stock_file_path), exist_ok=True)
    _curr_all_stock.to_pickle(_all_stock_file_path)
    print("数据已更新并保存到缓存文件")
    return _curr_all_stock

def _is_today_data(data: pd.DataFrame) -> bool:
    # 获取数据中的最新日期
    if '日期' not in data.columns:
        return False  # 如果没有日期列，返回 False
    latest_date = data['日期'].max()
    # 检查是否为当天日期
    return latest_date == datetime.datetime.now().strftime('%Y-%m-%d')

def _local_path(code: str) -> str:
    return os.path.join(CACHE_DIR, f"{code}.pkl")

def last_trading_day(date: str = None) -> str:
    # 如果没有传入日期，则使用当前日期
    if date is None:
        dt = pd.Timestamp.today()
    else:
        dt = pd.to_datetime(date, format="%Y%m%d")

    # 如果当前时间是下午3点之前，回退到上一个交易日
    if dt.hour < 15 and date is None:  # 只有使用当前日期时才考虑小时
        dt -= pd.Timedelta(days=1)

    # 如果日期是周末，回退到上一个周五
    while dt.weekday() >= 5:  # 周六或周日
        dt -= pd.Timedelta(days=1)

    return dt.strftime("%Y%m%d")

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
def load_or_update(code: str, update: bool, update_day: str) -> pd.DataFrame:
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

    if update :
        update_day_dt = pd.to_datetime(last_trading_day(update_day))  # 确保使用最近的交易日
        if update_day_dt.date() > last_date.date():
            start_str = (last_date + pd.Timedelta(days=1)).strftime("%Y%m%d")
            end_str = update_day_dt.strftime("%Y%m%d")  # 使用调整后的交易日日期
            print('{} need update, last:{}, start:{}, end{}'.format(code, last_date.date(), start_str, end_str))
            #time.sleep(random.uniform(0.2, 0.3))
            time.sleep(0.2)
            df_new = ak.stock_zh_a_hist(symbol=code,
                                        period="daily",
                                        start_date=start_str,
                                        end_date=end_str,
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
    spot = get_current_stock_info()

    sh_delist = ak.stock_info_sh_delist()
    delist_codes = set(sh_delist['公司代码'].astype(str).str.zfill(6))

    spot = spot[~spot['代码'].isin(delist_codes)]


    # 增强退市股票过滤条件
    delisting_keywords = ['退市', '退', 'DELIST', '终止上市']
    delisting_pattern = '|'.join(delisting_keywords)

    spot = spot[~spot['名称'].str.contains(delisting_pattern, na=False, case=False)]

    if '退市整理' in spot.columns or 'delisting_status' in spot.columns:
        status_col = '退市整理' if '退市整理' in spot.columns else 'delisting_status'
        spot = spot[spot[status_col] != 1]  # 假设1表示退市状态

    #spot = spot[~spot['名称'].str.startswith('退市', na=False)]

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

    load_or_update_stock_code_name_dict(update=True, ak_spot=spot)

    codes = spot['代码'].str.zfill(6).tolist()
    names = spot.set_index('代码')['名称'].to_dict()
    return codes, names

def get_stock_data() -> Dict[str, pd.DataFrame]:
    global _global_stock_data_dict
    if _global_stock_data_dict is None:
        _global_stock_data_dict = {}
        codes, _ = get_all_stock_from_cache()
        for code in codes:
            _global_stock_data_dict[code] = load_or_update(code, False, '')
    return _global_stock_data_dict
