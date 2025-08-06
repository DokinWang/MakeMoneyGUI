import pandas as pd
from typing import List, Tuple

# 假设已有本地缓存工具
from back_best import load_or_update   # 返回完整的个股日 K DataFrame
# -------------------------------------------------
# 公共：把日 K 转周线
# -------------------------------------------------
def _make_weekly(df: pd.DataFrame, window: int = 20) -> pd.DataFrame:
    """
    输入：完整的日 K DataFrame（必须含 ['日期','开盘','收盘','最高','最低']）
    输出：周线 DataFrame，含最新一条布林上下轨
    """
    if df.empty:
        return pd.DataFrame()

    df = df.sort_values('日期').reset_index(drop=True)
    df['week_start'] = pd.to_datetime(df['日期']).dt.to_period('W').dt.start_time
    weekly = (
        df.groupby('week_start')
          .agg(日期=('日期', 'last'),     # 周五
               开盘=('开盘', 'first'),
               收盘=('收盘', 'last'),
               最高=('最高', 'max'),
               最低=('最低', 'min'))
          .reset_index(drop=True)
    )

    weekly['MA']   = weekly['收盘'].rolling(window).mean()
    weekly['STD']  = weekly['收盘'].rolling(window).std()
    weekly['Upper'] = weekly['MA'] + 2 * weekly['STD']
    weekly['Lower'] = weekly['MA'] - 2 * weekly['STD']
    return weekly

# -------------------------------------------------
# 1) 距离下轨 ≤10%
# -------------------------------------------------
def scan_weekly_boll_lower_near(
        symbols: List[str],
        window: int = 20,
        threshold: float = 0.10,
        update: bool = False) -> pd.DataFrame:
    """
    symbols: 要扫描的股票代码列表
    threshold: 距离下轨的百分比上限，默认 0.10（10%）
    返回 DataFrame：code, latest_close, lower, distance
    """
    records = []
    for code in symbols:
        df_day = load_or_update(code, update)
        wk = _make_weekly(df_day, window)
        if wk.empty or wk['Lower'].isna().iloc[-1]:
            continue

        latest_close = wk.iloc[-1]['收盘']
        lower = wk.iloc[-1]['Lower']
        distance = abs(latest_close - lower) / abs(lower)

        if distance <= threshold:
            records.append({
                'code': code,
                'latest_close': latest_close,
                'lower': lower,
                'distance': distance
            })
    df_out = pd.DataFrame(records)
    if df_out.empty:
        return pd.DataFrame(columns=['code', 'latest_close', 'lower', 'distance'])
    return pd.DataFrame(records).sort_values('distance')

# -------------------------------------------------
# 2) 收盘价跌破下轨
# -------------------------------------------------
def scan_weekly_boll_lower_break(
        symbols: List[str],
        window: int = 20,
        update: bool = False) -> pd.DataFrame:
    """
    symbols: 要扫描的股票代码列表
    返回 DataFrame：code, latest_close, lower, distance(负数)
    """
    records = []
    for code in symbols:
        df_day = load_or_update(code, update)
        wk = _make_weekly(df_day, window)
        if wk.empty or wk['Lower'].isna().iloc[-1]:
            continue

        latest_close = wk.iloc[-1]['收盘']
        lower = wk.iloc[-1]['Lower']
        distance = (latest_close - lower) / lower   # 跌破时为负

        if latest_close < lower:                    # 只要跌破的
            records.append({
                'code': code,
                'latest_close': latest_close,
                'lower': lower,
                'distance': distance
            })

    df_out = pd.DataFrame(records)
    if df_out.empty:
        # 空表也带上 distance 列
        return pd.DataFrame(columns=['code', 'latest_close', 'lower', 'distance'])

    return df_out.sort_values('distance').reset_index(drop=True)
