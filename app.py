import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="嗖马选品数据中台MVP", layout="wide")

DATA_DIR = "./data"

def get_latest_analysis():
    files = [f for f in os.listdir(DATA_DIR) if f.startswith("analysis_result")]
    if not files:
        return None
    return os.path.join(DATA_DIR, max(files, key=os.path.getctime))

def load_data():
    f = get_latest_analysis()
    if not f:
        return None, None
    df = pd.read_excel(f, sheet_name="all")
    top = pd.read_excel(f, sheet_name="top20")
    return df, top

st.title("📊 嗖马选品 & 竞品分析数据中台（MVP）")
df, top = load_data()

if df is None:
    st.warning("请先运行采集与分析脚本")
    st.stop()

st.subheader("🔥 高潜力商品推荐")
st.dataframe(top[["title", "price", "sales_num", "potential_score", "link"]], use_container_width=True)

st.subheader("📈 全量数据概览")
c1, c2, c3 = st.columns(3)
c1.metric("总商品数", len(df))
c2.metric("均价", round(df["price"].mean(), 2))
c3.metric("高潜力商品", len(top))

st.subheader("📋 完整数据")
st.dataframe(df, use_container_width=True)