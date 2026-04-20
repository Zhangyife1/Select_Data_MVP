import pandas as pd
import os
from datetime import datetime

DATA_DIR = "./data"

def get_latest_file(prefix):
    files = [f for f in os.listdir(DATA_DIR) if f.startswith(prefix)]
    if not files:
        return None
    return os.path.join(DATA_DIR, max(files, key=os.path.getctime))

def clean_and_calc():
    raw_file = get_latest_file("智能营销机器人_raw")
    if not raw_file:
        print("未找到采集数据")
        return

    df = pd.read_excel(raw_file)

    # 清洗
    df = df.dropna(subset=["price", "sales"])
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df = df[df["price"] > 0]

    # 销量清洗
    df["sales_num"] = df["sales"].str.extract(r"(\d+)").fillna(0).astype(int)

    # 简单指标
    df["estimate_revenue"] = df["price"] * df["sales_num"]
    df["margin_guess"] = 0.3  # 预估毛利率
    df["potential_score"] = df["sales_num"] * 0.6 + df["price"] * 0.1

    # 输出
    out_path = f"./data/analysis_result_{datetime.now().strftime('%Y%m%d')}.xlsx"
    with pd.ExcelWriter(out_path) as w:
        df.to_excel(w, sheet_name="all", index=False)
        top = df.sort_values("potential_score", ascending=False).head(20)
        top.to_excel(w, sheet_name="top20", index=False)

    print(f"分析完成：{out_path}")

if __name__ == "__main__":
    clean_and_calc()