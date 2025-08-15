
import pandas as pd
import datetime

from typing import List, Dict, Tuple
from view.policy.stock import get_cache_dir, get_sh_series, stock_name

def _sh_ok(dt, sh_min=3180, sh_max=3600) -> bool:
    val = get_sh_series().get(dt)
    return val is not None and sh_min <= val <= sh_max

def boll_reverse_backtest(code: str,
                          df: pd.DataFrame,
                          period_s: str = "2023-01-16",
                          period_e: str = None,
                          sh_min: int = 3100,
                          sh_max: int = 3600,
                          window: int = 20) -> pd.DataFrame:
    if period_e is None:
        period_e = datetime.date.today().strftime("%Y-%m-%d")

    if df.empty:
        return pd.DataFrame(), None
    df = df.sort_values('日期').reset_index(drop=True)

    # 2) 合成 3 日线
    df['trade_no'] = df.index // 3
    #df['trade_no'] = pd.to_datetime(df['日期']).dt.to_period('W').dt.start_time  # 周一

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
        if not _sh_ok(buy_bar['日期'], sh_min, sh_max):
            continue  # 上证不在区间，跳过

        # 卖出日
        sell_candidates = sub[sub['日期'] > low_date]
        cond = sell_candidates['最高'] >= sell_candidates['MA20']
        if not cond.any():
            continue
        sell_bar = sell_candidates[cond].iloc[0]
        #if not _sh_ok(sell_bar['日期']):
        #    continue  # 上证不在区间，跳过

        # 保留两位小数
        buy_price = round(buy_bar['Lower'], 2)
        sell_price = round(sell_bar['MA20'], 2)

        name = stock_name(code)
        trades.append({
            '代码': code,
            '名称': name,
            '买入价': buy_price,
            '卖出价': sell_price,
            '买入日期': buy_bar['日期'].strftime("%Y-%m-%d"),
            '卖出日期': sell_bar['日期'].strftime("%Y-%m-%d"),
            '收益率': (sell_price - buy_price) / buy_price,
            '持有天数': (sell_bar['日期'] - buy_bar['日期']).days
        })

    df_trades = pd.DataFrame(trades)
    return df_trades
