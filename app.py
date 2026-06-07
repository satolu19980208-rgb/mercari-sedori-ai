import streamlit as st
import base64

from utils.profit_calculator import calculate_profit
from utils.ai_analyzer import analyze_images

from utils.history_db import (
    init_db,
    save_history
)

from utils.settings_db import (
    init_settings,
    get_settings
)

st.set_page_config(
    page_title="💰せどりAI",
    page_icon="💰",
    layout="wide"
)

init_db()
init_settings()
# --------------------
# session_state
# --------------------
if "buy_price" not in st.session_state:
    st.session_state.buy_price = 0

if "sell_price" not in st.session_state:
    st.session_state.sell_price = 0

if "product_name" not in st.session_state:
    st.session_state.product_name = ""

if "manufacturer" not in st.session_state:
    st.session_state.manufacturer = ""

if "model" not in st.session_state:
    st.session_state.model = ""

if "ai_result" not in st.session_state:
    st.session_state.ai_result = None

if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = 0    

if "memo" not in st.session_state:
    st.session_state.memo = ""
# --------------------
# タイトル
# --------------------

st.title("💰 せどりAI")


# --------------------
# 商品情報
# --------------------

st.header("📸 商品情報")

uploaded_files = st.file_uploader(
    "商品画像をアップロード",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True,
    key=st.session_state.get(
        "uploader_key",
        0
    )
)

if uploaded_files:

    st.subheader("アップロード画像")

    cols = st.columns(
        min(4, len(uploaded_files))
    )

    for i, file in enumerate(uploaded_files):

        with cols[i % len(cols)]:

            st.image(
                file,
                caption=f"画像{i+1}",
                width="stretch"
            )

st.divider()

col1, col2 = st.columns(2)

with col1:

    product_name = st.text_input(
        "商品名",
        value=st.session_state.product_name
    )

    manufacturer = st.text_input(
        "メーカー",
        value=st.session_state.manufacturer
    )

    model = st.text_input(
        "型番",
        value=st.session_state.model
    )

with col2:

    condition = st.selectbox(
        "状態",
        [
            "新品",
            "未使用に近い",
            "目立った傷なし",
            "やや傷あり",
            "傷あり",
            "ジャンク"
        ]
    )

    buy_price = st.number_input(
        "仕入価格",
        min_value=0,
        key="buy_price"
    )

memo = st.text_area(
    "備考",
    height=100,
    key="memo"
)

st.divider()

# --------------------
# AI診断
# --------------------

if st.button("🤖 商品診断"):

    image_base64_list = []

    if uploaded_files:

        for file in uploaded_files:

            file.seek(0)

            image_bytes = file.read()

            image_base64 = base64.b64encode(
                image_bytes
            ).decode("utf-8")

            image_base64_list.append(
                image_base64
            )

    manual_info = f"""
商品名: {product_name}
メーカー: {manufacturer}
型番: {model}
状態: {condition}
備考: {memo}
"""

    with st.spinner(
        "AI診断中..."
    ):

        result = analyze_images(
            image_base64_list,
            manual_info
        )

    if "error" in result:

        st.error(
            result["error"]
        )

    else:

        st.session_state.product_name = result.get(
            "product_name",
            ""
        )

        st.session_state.manufacturer = result.get(
            "manufacturer",
            ""
        )

        st.session_state.model = result.get(
            "model",
            ""
        )

        st.session_state.ai_result = result

        st.rerun()

# --------------------
# AI結果表示
# --------------------

if st.session_state.ai_result:

    result = st.session_state.ai_result

    st.subheader(
        "🤖 AI診断結果"
    )

    st.write(
        "商品名:",
        result.get(
            "product_name",
            ""
        )
    )

    st.write(
        "メーカー:",
        result.get(
            "manufacturer",
            ""
        )
    )

    st.write(
        "型番:",
        result.get(
            "model",
            ""
        )
    )

    st.write(
        "カテゴリ:",
        result.get(
            "category",
            ""
        )
    )

    st.write(
    "推定中古相場:",
    result.get(
        "estimated_used_price",
        ""
        )
    )
    st.write(
    "推定価格帯:",
    result.get(
        "estimated_price_range",
        ""
        )
    )
    st.write(
        "推定梱包サイズ:",
        result.get(
            "estimated_package_size",
            ""
        )
    )
    st.write(
        "推定送料:",
        result.get(
            "estimated_shipping_cost",
            ""
        )
    )
    st.write(
        "需要:",
        result.get(
            "demand",
            ""
        )
    )

    st.write(
        "回転率:",
        result.get(
            "turnover",
            ""
        )
    )

    st.write(
        "注意点:",
        result.get(
            "warning_points",
            ""
        )
    )

    st.write(
        "推奨度:",
        result.get(
            "recommendation",
            ""
        )
    )

    st.write(
        "AI自信度:",
        result.get(
            "confidence",
            ""
        )
    )
st.divider()
    
# --------------------
# 相場検索
# --------------------

st.subheader("🔎 相場検索")

default_search_word = (
    product_name
    or model
)

if st.session_state.ai_result:

    ai_name = (
        st.session_state.ai_result.get(
            "product_name",
            ""
        )
    )

    if ai_name:

        default_search_word = ai_name

search_word = st.text_input(
    "検索キーワード",
    value=default_search_word,
    key="search_word"
)

if search_word:

    mercari_url = (
        f"https://jp.mercari.com/search?keyword={search_word}"
    )

    sold_url = (
        f"https://jp.mercari.com/search?keyword={search_word}&status=sold_out"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.link_button(
            "🛒 メルカリ検索",
            mercari_url
        )

    with col2:

        st.link_button(
            "✅ 売り切れ検索",
            sold_url
        )

st.divider()
# --------------------
# 利益計算
# --------------------

st.header("💰 利益計算")

sell_price = st.number_input(
        "販売想定価格",
        min_value=0,
        key="sell_price"
    )

default_shipping = 750

if st.session_state.ai_result:

    shipping_text = (
        st.session_state.ai_result.get(
            "estimated_shipping_cost",
            "750"
        )
    )

    shipping_text = (
        shipping_text
        .replace("円", "")
        .replace(",", "")
    )

    try:
        default_shipping = int(
            shipping_text
        )
    except:
        pass

shipping = st.number_input(
    "送料",
    min_value=0,
    value=default_shipping,
    step=50
)

if sell_price > 0:

    profit_result = calculate_profit(
        sell_price=sell_price,
        buy_price=buy_price,
        shipping=shipping
    )

    settings = get_settings()

    profit = profit_result["profit"]
    roi = profit_result["roi"]

    judge_type = settings["judge_type"]

    buy_profit = settings["buy_profit"]
    consider_profit = settings["consider_profit"]

    buy_roi = settings["buy_roi"]
    consider_roi = settings["consider_roi"]

    st.subheader("計算結果")

    st.write(
        f"販売手数料: {profit_result['fee']:,.0f}円"
    )

    st.write(
        f"利益: {profit:,.0f}円"
    )

    st.write(
        f"ROI: {roi:.1f}%"
    )

    judge_text = "見送り"

    if judge_type == "利益額":

        if profit >= buy_profit:

            judge_text = "買い"
            st.success("🟢 買い")

        elif profit >= consider_profit:

            judge_text = "検討"
            st.warning("🟡 検討")

        else:

            st.error("🔴 見送り")

    elif judge_type == "ROI":

        if roi >= buy_roi:

            judge_text = "買い"
            st.success("🟢 買い")

        elif roi >= consider_roi:

            judge_text = "検討"
            st.warning("🟡 検討")

        else:

            st.error("🔴 見送り")

    else:

        if (
            profit >= buy_profit
            and
            roi >= buy_roi
        ):

            judge_text = "買い"
            st.success("🟢 買い")

        elif (
            profit >= consider_profit
            and
            roi >= consider_roi
        ):

            judge_text = "検討"
            st.warning("🟡 検討")

        else:

            st.error("🔴 見送り")

    st.caption(
        f"判定方式: {judge_type}"
    )

    if st.button("💾 履歴保存"):

        category = ""

        if st.session_state.ai_result:

            category = (
                st.session_state.ai_result.get(
                    "category",
                    ""
                )
            )

        recommendation = judge_text

        save_history(
            product_name,
            manufacturer,
            model,
            category,
            memo,
            buy_price,
            sell_price,
            int(profit_result["profit"]),
            recommendation
        )

        st.success("保存しました")
   
if st.button("🆕 次の商品"):

    for key in [
        "product_name",
        "manufacturer",
        "model",
        "buy_price",
        "sell_price",
        "memo",
        "ai_result"
    ]:

        if key in st.session_state:
            del st.session_state[key]

    st.session_state.uploader_key += 1

    st.rerun()
