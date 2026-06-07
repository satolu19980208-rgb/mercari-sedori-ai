import streamlit as st
import pandas as pd
from collections import defaultdict
from utils.history_db import (
    get_history,
    delete_history,
    update_history
)
from utils.settings_db import get_settings
st.title("📚 履歴")

rows = get_history()
total_count = len(rows)

total_profit = 0

for row in rows:

    total_profit += row[9]

average_profit = 0

if total_count > 0:

    average_profit = (
        total_profit
        / total_count
    )
actual_profit = 0

for row in rows:

    sold = row[11]

    if sold == 1:

        actual_profit += row[9]

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "📦 総件数",
        total_count
    )

with col2:

    st.metric(
        "💰 予想利益",
        f"{total_profit:,}円"
    )

with col3:

    st.metric(
        "🏦 実利益",
        f"{actual_profit:,}円"
    )
search_word = st.text_input(
    "🔍 商品検索"
)
month_filter = st.selectbox(
    "📅 月別表示",
    ["すべて"] +
    sorted(
        list(
            set(
                row[1][:7]
                for row in rows
            )
        ),
        reverse=True
    )
)
category_filter = st.selectbox(
    "カテゴリ絞り込み",
    ["すべて"] +
    sorted(
        list(
            set(
                row[5]
                for row in rows
                if row[5]
            )
        )
    )
)

if rows:

    st.subheader("🏆 利益ランキング TOP5")

    ranking_rows = sorted(
        rows,
        key=lambda x: x[9],
        reverse=True
    )

    for i, row in enumerate(
        ranking_rows[:5],
        start=1
    ):

        if row[9] >= 0:

            st.success(
                f"{i}位  {row[2]}  ({row[9]:,}円)"
            )

        else:

            st.error(
                f"{i}位  {row[2]}  ({row[9]:,}円)"
            )
if rows:

    st.subheader(
        "📂 ジャンル別利益"
    )

    category_profit = defaultdict(int)

    for row in rows:

        category = row[5]

        profit = row[9]

        category_profit[category] += profit

    sorted_category = sorted(
        category_profit.items(),
        key=lambda x: x[1],
        reverse=True
    )

    for category, profit in sorted_category:

        st.write(
            f"{category} : {profit:,}円"
        )


filtered_rows = []

for row in rows:

    product_name = str(row[2])

    row_month = row[1][:7]

    if (
        (
            search_word == ""
            or search_word.lower()
            in product_name.lower()
        )
        and
        (
            category_filter == "すべて"
            or row[5] == category_filter
        )
        and
        (
            month_filter == "すべて"
            or row_month == month_filter
        )
    ):

        filtered_rows.append(row)

month_profit = 0

for row in filtered_rows:
    month_profit += row[9]

st.info(
    f"表示中利益合計: {month_profit:,}円"
)

if not rows:

    st.info(
        "履歴はありません"
    )
else:

    settings = get_settings()

    judge_type = settings["judge_type"]
    buy_profit = settings["buy_profit"]
    consider_profit = settings["consider_profit"]
    buy_roi = settings["buy_roi"]
    consider_roi = settings["consider_roi"]

    for row in filtered_rows:

        history_id = row[0]
        created_at = row[1]
        product_name = row[2]
        manufacturer = row[3]
        model = row[4]
        category = row[5]
        memo = row[6]
        buy_price = row[7]
        sell_price = row[8]
        profit = row[9]
        recommendation = row[10]
        sold = row[11]

        roi = 0

        if buy_price > 0:

            roi = (
                profit
                / buy_price
                * 100
            )

        mark = "🔴"

        if judge_type == "利益額":

            if profit >= buy_profit:

                mark = "🔵"

            elif profit >= consider_profit:

                mark = "🟡"

        elif judge_type == "ROI":

            if roi >= buy_roi:

                mark = "🔵"

            elif roi >= consider_roi:

                mark = "🟡"

        else:

            if (
                profit >= buy_profit
                and roi >= buy_roi
            ):

                mark = "🔵"

            elif (
                profit >= consider_profit
                and roi >= consider_roi
            ):

                mark = "🟡"

        with st.expander(
            f"📅 {created_at[:10]} | "
            f"{product_name} | "
            f"💰 {profit:,}円 | "
            f"{mark}",
            expanded=False
        ):
            edit_sold = st.checkbox(
                "売却済み",
                value=bool(sold),
                key=f"sold_{history_id}"
            )       
            st.write(
                f"📅 {created_at}"
            )

            st.write(
                f"📦 {product_name}"
            )
            edit_product_name = st.text_input(
                "商品名",
                value=product_name,
                key=f"name_{history_id}"
            )

            edit_manufacturer = st.text_input(
                "メーカー",
                value=manufacturer,
                key=f"maker_{history_id}"
            )

            edit_model = st.text_input(
                "型番",
                value=model,
                key=f"model_{history_id}"
            )

            edit_category = st.text_input(
                "カテゴリ",
                value=category,
                key=f"cat_{history_id}"
            )
            edit_memo = st.text_area(
                "備考",
                value=memo,
                key=f"memo_{history_id}"
            )
            edit_buy_price = st.number_input(
                "仕入価格",
                value=buy_price,
                key=f"buy_{history_id}"
            )

            edit_sell_price = st.number_input(
                "販売価格",
                value=sell_price,
                key=f"sell_{history_id}"
            )

            edit_shipping = st.number_input(
                "送料",
                value=750,
                key=f"ship_{history_id}"
            )

            edit_profit = int(
                edit_sell_price
                - (edit_sell_price * 0.1)
                - edit_shipping
                - edit_buy_price
            )

            st.write(
                f"利益: {edit_profit:,}円"
            )
            edit_recommendation = st.text_input(
                "判定",
                value=recommendation,
                key=f"rec_{history_id}"
            )

            col1, col2 = st.columns(2)

            with col1:

                if st.button(
                    "💾 更新",
                    key=f"update_{history_id}"
                ):

                    update_history(
                        history_id,
                        edit_product_name,
                        edit_manufacturer,
                        edit_model,
                        edit_category,
                        edit_memo,
                        edit_buy_price,
                        edit_sell_price,
                        edit_profit,
                        edit_recommendation,
                        int(edit_sold)
                    )

                    st.success(
                        "更新しました"
                    )

                    st.rerun()

            with col2:

                if st.button(
                    "🗑 削除",
                    key=f"delete_{history_id}"
                ):

                    delete_history(
                        history_id
                    )

                    st.rerun()

            st.divider()
if filtered_rows:

    df = pd.DataFrame(
        filtered_rows,
        columns=[
            "ID",
            "日時",
            "商品名",
            "メーカー",
            "型番",
            "カテゴリ",
            "メモ",
            "仕入価格",
            "販売価格",
            "利益",
            "判定",
            "売却済み"
        ]
    )

    csv = df.to_csv(
        index=False,
        encoding="utf-8-sig"
    )

    st.download_button(
        label="📥 CSV出力",
        data=csv,
        file_name="sedori_history.csv",
        mime="text/csv"
    )
