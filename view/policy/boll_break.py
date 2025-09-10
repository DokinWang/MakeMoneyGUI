
import pandas as pd
import datetime

from typing import List, Dict, Tuple
from view.policy.stock import get_cache_dir, get_sh_series, stock_name, update_sh, get_current_stock_info

def get_sh(dt) -> int:
    val = get_sh_series().get(dt)
    if val is None:
        update_sh()
    val = get_sh_series().get(dt)
    return val
#推荐值:
#3250 - 3450:3日线
#3450以上:周线
#月线常开
def boll_reverse_backtest(code: str,
                          df: pd.DataFrame,
                          
                          policySelect: int,
                          sellPos: int,
                          upperBreak: bool,
                          period_s: str = "2023-01-16",
                          period_e: str = None,
                          sh_min: int = 3100,
                          sh_max: int = 3600,
                          marketValMin: int = 50,
                          marketValMax: int = 20000,
                          peRatioMin: int = 20,
                          peRatioMax: int = 80,
                          window: int = 20) -> pd.DataFrame:
    if period_e is None:
        period_e = datetime.date.today().strftime("%Y-%m-%d")

    if df.empty:
        return pd.DataFrame(), None
    df = df.sort_values('日期').reset_index(drop=True)

    # 2) 合成 3 日线
    if policySelect == 0:
        df['trade_no'] = df.index // 3
        period_delta = pd.Timedelta(days=5)
    elif policySelect == 1:
        df['trade_no'] = pd.to_datetime(df['日期']).dt.to_period('W').dt.start_time
        period_delta = pd.Timedelta(days=7)
    elif policySelect == 2:
        df['trade_no'] = pd.to_datetime(df['日期']).dt.to_period('M').dt.start_time
        period_delta = pd.Timedelta(days=31)

    policy_df = (
        df.groupby(df['trade_no'])
          .agg(日期=('日期', 'last'),
               开盘=('开盘', 'first'),
               收盘=('收盘', 'last'),
               最高=('最高', 'max'),
               最低=('最低', 'min'))
          .reset_index(drop=True)
    )

    # 3) 布林线
    policy_df['MA20']  = policy_df['收盘'].rolling(window).mean()
    policy_df['STD']   = policy_df['收盘'].rolling(window).std()
    policy_df['Upper'] = policy_df['MA20'] + 2 * policy_df['STD']
    policy_df['Lower'] = policy_df['MA20'] - 2 * policy_df['STD']

    # 4) 标记突破/跌破
    policy_df['Break_Upper'] = policy_df['最高'] >= policy_df['Upper']
    policy_df['Break_Lower'] = policy_df['最低'] <= policy_df['Lower']

    # 5) 时间过滤
    period_s = pd.to_datetime(period_s)
    period_e = pd.to_datetime(period_e)
    sub = policy_df[
        (policy_df['日期'] >= period_s) &
        (policy_df['日期'] <= period_e)
    ].reset_index(drop=True)

    upper_dates = sub.loc[sub['Break_Upper'], '日期'].tolist()
    lower_dates = sub.loc[sub['Break_Lower'], '日期'].tolist()
    sh = 0
    trades = []
    curr_stock_info = get_current_stock_info()
    stock_info = curr_stock_info[curr_stock_info['代码'] == code]
    marketVal = stock_info['总市值'].values[0] / 100000000
    if marketVal < marketValMin or marketVal > marketValMax:
        return pd.DataFrame(trades)
    peRatio = stock_info['市盈率-动态'].values[0]
    if peRatio < peRatioMin or peRatio > peRatioMax:
        return pd.DataFrame(trades)

    if upperBreak:
        for up_date in reversed(upper_dates):
            lows_after = [d for d in lower_dates if d > up_date]
            if not lows_after:
                continue
            low_date = min(lows_after)

            # 区间干净检查
            mids = sub[(sub['日期'] > up_date) & (sub['日期'] < low_date)]
            if mids['Break_Upper'].any() or mids['Break_Lower'].any():
                continue

            # 在原始日线数据中找到该周期内首次达到买入价的具体日期
            buy_day_candidates = df[(df['日期'] >= up_date) & (df['日期'] <= low_date)]
            buy_price = policy_df[policy_df['日期'] == low_date]['Lower'].values[0]
            buy_day_candidates = buy_day_candidates[buy_day_candidates['最低'] <= buy_price]
            if buy_day_candidates.empty:
                continue
            buy_bar = buy_day_candidates.iloc[0]

            # 检查上证指数是否在指定范围内
            sh = get_sh(buy_bar['日期'])
            if sh < sh_min or sh > sh_max:
                continue  # 上证不在区间，跳过

            # 卖出日
            sell_candidates = sub[sub['日期'] > low_date]
            if sellPos == 0:
                cond = sell_candidates['最高'] >= sell_candidates['MA20']
            else:
                cond = sell_candidates['最高'] >= sell_candidates['Upper']
            if not cond.any():
                continue
            sell_policy_bar = sell_candidates[cond].iloc[0]

            # 在原始日线数据中找到该周期内首次达到卖出价的具体日期
            sell_date = sell_policy_bar['日期']
            sell_day_candidates = df[(df['日期'] > buy_bar['日期']) & (df['日期'] >= (sell_date - period_delta)) & (df['日期'] <= sell_date)]
            if sellPos == 0:
                sell_price = sell_policy_bar['MA20']
            else:
                sell_price = sell_policy_bar['Upper']
            sell_day_candidates = sell_day_candidates[sell_day_candidates['最高'] >= sell_price]
            if sell_day_candidates.empty:
                continue
            sell_bar = sell_day_candidates.iloc[0]

            # 保留两位小数
            buy_price = round(buy_price, 2)
            sell_price = round(sell_price, 2)
            marketVal = round(marketVal, 2)
            peRatio = round(peRatio, 2)

            name = stock_name(code)
            trades.append({
                '代码': code,
                '名称': name,
                '买入价': buy_price,
                '卖出价': sell_price,
                '买入日期': buy_bar['日期'].strftime("%Y-%m-%d"),
                '卖出日期': sell_bar['日期'].strftime("%Y-%m-%d"),
                '收益率': (sell_price - buy_price) / buy_price,
                '持有天数': (sell_bar['日期'] - buy_bar['日期']).days,
                '上证指数': sh,
                '市值': marketVal,
                '市盈率': peRatio
            })
    else:
        # 标记是否已经发生过买入操作
        has_bought = False
        for low_date in lower_dates:
            if has_bought:
                break  # 如果已经买入，不再处理后续的突破

            # 在原始日线数据中找到该周期内首次达到买入价的具体日期
            buy_day_candidates = df[(df['日期'] <= low_date)]
            buy_price = policy_df[policy_df['日期'] == low_date]['Lower'].values[0]
            buy_day_candidates = buy_day_candidates[buy_day_candidates['最低'] <= buy_price]
            if buy_day_candidates.empty:
                continue
            buy_bar = buy_day_candidates.iloc[-1]

            # 检查上证指数是否在指定范围内
            sh = get_sh(buy_bar['日期'])
            if sh < sh_min or sh > sh_max:
                continue  # 上证不在区间，跳过

            # 卖出日
            sell_candidates = sub[sub['日期'] > low_date]
            if sellPos == 0:
                cond = sell_candidates['最高'] >= sell_candidates['MA20']
            else:
                cond = sell_candidates['最高'] >= sell_candidates['Upper']
            if not cond.any():
                continue
            sell_policy_bar = sell_candidates[cond].iloc[0]

            # 在原始日线数据中找到该周期内首次达到卖出价的具体日期
            sell_date = sell_policy_bar['日期']
            sell_day_candidates = df[(df['日期'] > buy_bar['日期']) & (df['日期'] >= (sell_date - period_delta)) & (df['日期'] <= sell_date)]
            if sellPos == 0:
                sell_price = sell_policy_bar['MA20']
            else:
                sell_price = sell_policy_bar['Upper']
            sell_day_candidates = sell_day_candidates[sell_day_candidates['最高'] >= sell_price]
            if sell_day_candidates.empty:
                continue
            sell_bar = sell_day_candidates.iloc[0]


            # 逐天遍历，检查是否跌破买入价的90%
            sell_candidates = df[(df['日期'] > buy_bar['日期']) & (df['日期'] <= sell_bar['日期'])]
            threshold_price = buy_price * 0.9  # 买入价的90%
            for _, row in sell_candidates.iterrows():
                if row['最低'] <= threshold_price and (row['日期'] - buy_bar['日期']).days > 80:
                    # 如果某一天的最低价跌破了买入价的90%，则在这一天卖出
                    sell_date = row['日期']
                    sell_price = threshold_price
                    break
                if row['收盘'] > buy_price and (row['日期'] - buy_bar['日期']).days > 80:
                    sell_date = row['日期']
                    sell_price = row['收盘']
                    break

            # 保留两位小数
            buy_price = round(buy_price, 2)
            sell_price = round(sell_price, 2)
            marketVal = round(marketVal, 2)
            peRatio = round(peRatio, 2)

            name = stock_name(code)
            trades.append({
                '代码': code,
                '名称': name,
                '买入价': buy_price,
                '卖出价': sell_price,
                '买入日期': buy_bar['日期'].strftime("%Y-%m-%d"),
                '卖出日期': sell_bar['日期'].strftime("%Y-%m-%d"),
                '收益率': (sell_price - buy_price) / buy_price,
                '持有天数': (sell_bar['日期'] - buy_bar['日期']).days,
                '上证指数': sh,
                '市值': marketVal,
                '市盈率': peRatio
            })

            # 标记已经发生过买入操作
            has_bought = True
    df_trades = pd.DataFrame(trades)
    return df_trades

def boll_find(
    code: str,
    df: pd.DataFrame,
    curr_all_stock: pd.DataFrame,
    policySelect: int,
    upperBreak: bool,
    marketValMin: int = 50,
    marketValMax: int = 20000,
    peRatioMin: int = 20,
    peRatioMax: int = 80,
    window: int = 20,
) -> pd.DataFrame:
    """扫描：最近一次“突破上轨后又跌破下轨”是否已完成"""
    # 1. 基础过滤
    info = curr_all_stock[curr_all_stock['代码'] == code]
    if info.empty:
        return pd.DataFrame()
    marketVal = info['总市值'].values[0] / 1e8
    peRatio = info['市盈率-动态'].values[0]
    if not (marketValMin <= marketVal <= marketValMax and peRatioMin <= peRatio <= peRatioMax):
        return pd.DataFrame()

    # 2. 数据检查
    if df.empty or len(df) < window + 5:
        return pd.DataFrame()
    df = df.sort_values('日期').reset_index(drop=True)

    # 3. 合成周期
    if policySelect == 0:
        df['trade_no'] = df.index // 3
    elif policySelect == 1:
        df['trade_no'] = pd.to_datetime(df['日期']).dt.to_period('W').dt.start_time
    else:
        df['trade_no'] = pd.to_datetime(df['日期']).dt.to_period('M').dt.start_time

    policy_df = (
        df.groupby(df['trade_no'])
          .agg(日期=('日期', 'last'),
               开盘=('开盘', 'first'),
               收盘=('收盘', 'last'),
               最高=('最高', 'max'),
               最低=('最低', 'min'))
          .reset_index(drop=True)
    )

    # 3) 布林线
    policy_df['MA20']  = policy_df['收盘'].rolling(window).mean()
    policy_df['STD']   = policy_df['收盘'].rolling(window).std()
    policy_df['Upper'] = policy_df['MA20'] + 2 * policy_df['STD']
    policy_df['Lower'] = policy_df['MA20'] - 2 * policy_df['STD']

    policy_df['Break_Upper'] = policy_df['最高'] >= policy_df['Upper']
    policy_df['Break_Lower'] = policy_df['最低'] <= policy_df['Lower']

    # 5. 只看今天之前已完结的周期
    hist = policy_df.iloc[:-1]

    last_break_upper_date = (
        policy_df.loc[policy_df['Break_Upper'], '日期']
            .iloc[-1]          # 最后一个 True
            if policy_df['Break_Upper'].any()
            else None
    )
    
    if last_break_upper_date is None:
        return pd.DataFrame()

    curr_price = info['最新价'].values[0]
    lower_now = policy_df['Lower'].iloc[-1]
    if lower_now is None:
        print('lower_now is none')
        return pd.DataFrame()

    if curr_price > lower_now:
        return pd.DataFrame()

    # 8. 信号判断
    signal = False
    if upperBreak:
        up_rows = policy_df[policy_df['Break_Upper']]
        if up_rows.empty:
            return pd.DataFrame()                       # 从未突破过上轨
        idx_last_up = up_rows.index[-1]                 # 行号

        # 3. 截取「上次突破上轨 → 当前」这段区间
        seg = policy_df.loc[idx_last_up:, ]             # 包含 idx_last_up 行

        # 4. 检查是否出现过「跌破下轨」且「之后最高≥中轨」
        #    只要有一次完整的 down→up 往返，就视为「到过中轨」
        broken_lower = seg['Break_Lower']               # bool Series
        above_ma20   = seg['最高'] >= seg['MA20']

        # 向下穿越标志
        down_cross = broken_lower & ~broken_lower.shift(1).fillna(False)
        # 向上穿越标志
        up_cross   = above_ma20 & ~above_ma20.shift(1).fillna(False)

        # 找最近一次 down_cross 之后有没有 up_cross
        down_idx = seg.index[down_cross]
        if len(down_idx) == 0:
            # 期间从未跌破下轨 → 符合要求
            signal = True
        else:
            last_down = down_idx[-1]
            # 看 last_down 之后有没有 up_cross
            signal = up_cross.loc[last_down:].sum() == 0

        buy_price = round(lower_now, 2) if signal else None
    else:
        signal = True
        buy_price = round(lower_now, 2) if signal else None

    if not signal:
        return pd.DataFrame()

    # 8. 组装结果
    return pd.DataFrame([{
        '代码': code,
        '名称': stock_name(code),
        '市值': round(marketVal, 2),
        '市盈率': round(peRatio, 2),
        '日期': datetime.date.today().strftime("%Y-%m-%d"),
        '价格': buy_price,
    }])
