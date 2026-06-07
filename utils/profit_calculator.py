def calculate_profit(
    sell_price,
    buy_price,
    shipping
):

    fee = sell_price * 0.10

    profit = (
        sell_price
        - fee
        - shipping
        - buy_price
    )

    roi = 0

    if buy_price > 0:

        roi = (
            profit
            / buy_price
            * 100
        )

    return {
        "fee": fee,
        "profit": profit,
        "roi": roi
    }