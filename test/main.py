
from back_best import *
from weekly_boll import *
import datetime
from pathlib import Path

def bool_reverse_test():
    # 1. 股票列表（含 PE 过滤）

    codes, name_map = get_all_a_codes(PE_LOW, PE_HIGH)

    print(f"共 {len(codes)} 只股票待回测")

    all_res = []
    for code in tqdm(codes, desc="回测中"):
        try:
            trades_df, _ = boll_reverse_backtest(code, period_e="2025-07-25")
            if trades_df.empty:
                continue
            trades_df.insert(1, '股票名称', name_map.get(code, ''))
            all_res.append(trades_df)
        except Exception as e:
            tqdm.write(f"{code} 出错：{e}")

    if not all_res:
        print("没有任何交易记录")
        return

    # 合并结果
    result = pd.concat(all_res, ignore_index=True)

    # 计算整体统计
    avg_ret   = result['收益率'].mean()
    avg_days  = result['持有天数'].mean()
    summary = pd.DataFrame([{
        '股票代码': '汇总',
        '股票名称': '-',
        '买入日期': '-',
        '买入价': '-',
        '卖出日期': '-',
        '卖出价': '-',
        '收益率': avg_ret,
        '持有天数': avg_days
    }])

    # 1) 补零
    result['股票代码'] = result['股票代码'].astype(str).str.zfill(6)
    result['买入日期'] = result['买入日期'].astype(str)
    result['卖出日期'] = result['卖出日期'].astype(str)

    # 2) 收益率百分比
    result['收益率'] = result['收益率'] * 100

    # 追加到文件末尾
    result = pd.concat([result, summary], ignore_index=True)

    # 生成“年-月-日-时-分-秒”格式的工作表名
    sheet_name = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    with pd.ExcelWriter('all_boll_trades.xlsx',
                        engine='openpyxl',
                        mode='a',  # 追加模式
                        if_sheet_exists='new') as writer:  # 同名则新建
        result.to_excel(writer, sheet_name=sheet_name, index=False)
        ws = writer.sheets[sheet_name]

        # 设置列宽
        widths = dict(zip('ABCDEFGH', [10, 15, 16, 10, 16, 10, 12, 12]))
        for col_letter, w in widths.items():
            ws.column_dimensions[col_letter].width = w

    print(f"已保存 all_boll_trades.xlsx（{len(result)-1} 笔交易，平均收益 {avg_ret}%，平均持有 {avg_days:.1f} 天）")

def weekly_boll_test() -> None:
    # 1) 拉数据
    #codes, name_map = get_all_a_codes(PE_LOW, PE_HIGH)
    codes = get_all_a_codes_from_cache(PE_LOW, PE_HIGH)
    near_df = scan_weekly_boll_lower_near(codes, update=False)
    break_df = scan_weekly_boll_lower_break(codes, update=False)

    # 2) 合并 & 排序
    # 如果某一类为空，concat 会自动忽略
    merged = pd.concat([near_df, break_df], ignore_index=True)
    if not merged.empty:
        merged = merged.sort_values('distance', ascending=True).reset_index(drop=True)
    else:
        print("empty")
        return
    # 3) 写 Excel
    sheet_name = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    file_path = Path('weekly_boll.xlsx')

    with pd.ExcelWriter(file_path,
                        mode='a' if file_path.exists() else 'w',
                        engine='openpyxl') as writer:
        if not merged.empty:
            merged.to_excel(writer, sheet_name=sheet_name, index=False)

    print(f'已写入 {file_path.resolve()}，工作表名：{sheet_name}')


if __name__ == "__main__":

    #bool_reverse_test()
    weekly_boll_test()
