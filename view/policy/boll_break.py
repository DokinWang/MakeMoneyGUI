
import pandas as pd
import datetime

from typing import List, Dict, Tuple
from stock import get_cache_dir, get_sh_series, load_or_update

def _sh_ok(dt, min_val=3180, max_val=3600) -> bool:
    val = get_sh_series().get(dt)
    return val is not None and min_val <= val <= max_val

def boll_reverse_backtest(code: str,
                          period_s: str = "2023-01-16",
                          period_e: str = None,
                          window: int = 20) -> Tuple[pd.DataFrame, float]:
    if period_e is None:
        period_e = datetime.date.today().strftime("%Y-%m-%d")

    # 1) 取个股日 K（本地缓存）
    df = load_or_update(code, False)
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
            '股票代码': code,
            '买入日期': buy_bar['日期'].date(),
            '买入价': buy_price,
            '卖出日期': sell_bar['日期'].date(),
            '卖出价': sell_price,
            '收益率': (sell_price - buy_price) / buy_price,
            '持有天数': (sell_bar['日期'] - buy_bar['日期']).days
        })

    df_trades = pd.DataFrame(trades)
    return df_trades, df_trades['收益率'].mean() if not df_trades.empty else None
