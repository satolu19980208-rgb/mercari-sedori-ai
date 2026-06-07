import streamlit as st

from utils.settings_db import (
    init_settings,
    get_settings,
    save_settings
)

init_settings()

settings = get_settings()

st.title("⚙️ 設定")

judge_type = st.selectbox(
    "判定方法",
    [
        "利益額",
        "ROI",
        "利益額＋ROI"
    ],
    index=[
        "利益額",
        "ROI",
        "利益額＋ROI"
    ].index(
        settings["judge_type"]
    )
)

st.subheader("💰 利益額基準")

buy_profit = st.number_input(
    "買い利益額",
    value=settings["buy_profit"]
)

consider_profit = st.number_input(
    "検討利益額",
    value=settings["consider_profit"]
)

st.subheader("📈 ROI基準")

buy_roi = st.number_input(
    "買いROI(%)",
    value=float(
        settings["buy_roi"]
    )
)

consider_roi = st.number_input(
    "検討ROI(%)",
    value=float(
        settings["consider_roi"]
    )
)

if st.button("💾 設定保存"):

    save_settings(
        judge_type,
        buy_profit,
        consider_profit,
        buy_roi,
        consider_roi
    )

    st.success(
        "設定を保存しました"
    )

    st.rerun()