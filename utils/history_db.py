import sqlite3

DB_NAME = "history.db"


def init_db():

    conn = sqlite3.connect(DB_NAME)

    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        created_at TEXT,
        product_name TEXT,
        manufacturer TEXT,
        model TEXT,
        category TEXT,
        memo TEXT,
        buy_price INTEGER,
        sell_price INTEGER,
        profit INTEGER,
        recommendation TEXT,
        sold INTEGER DEFAULT 0
    )
    """)

    try:
        cur.execute("""
        ALTER TABLE history
        ADD COLUMN sold INTEGER DEFAULT 0
        """)
    except:
        pass

    conn.commit()
    conn.close()


def save_history(
    product_name,
    manufacturer,
    model,
    category,
    memo,
    buy_price,
    sell_price,
    profit,
    recommendation
):

    conn = sqlite3.connect(DB_NAME)

    cur = conn.cursor()

    cur.execute("""
    INSERT INTO history (
        created_at,
        product_name,
        manufacturer,
        model,
        category,
        memo,
        buy_price,
        sell_price,
        profit,
        recommendation,
        sold
    )
    VALUES (
        datetime('now','localtime'),
        ?,?,?,?,?,?,?,?,?,?
    )
    """, (
        product_name,
        manufacturer,
        model,
        category,
        memo,
        buy_price,
        sell_price,
        profit,
        recommendation,
        0
    ))

    conn.commit()
    conn.close()


def get_history():

    conn = sqlite3.connect(DB_NAME)

    cur = conn.cursor()

    cur.execute("""
    SELECT *
    FROM history
    ORDER BY id DESC
    """)

    rows = cur.fetchall()

    conn.close()

    return rows


def delete_history(history_id):

    conn = sqlite3.connect(DB_NAME)

    cur = conn.cursor()

    cur.execute(
        "DELETE FROM history WHERE id=?",
        (history_id,)
    )

    conn.commit()
    conn.close()
def update_history(
    history_id,
    product_name,
    manufacturer,
    model,
    category,
    memo,
    buy_price,
    sell_price,
    profit,
    recommendation,
    sold
):

    conn = sqlite3.connect(DB_NAME)

    cur = conn.cursor()

    cur.execute("""
    UPDATE history
    SET
        product_name=?,
        manufacturer=?,
        model=?,
        category=?,
        memo=?,
        buy_price=?,
        sell_price=?,
        profit=?,
        recommendation=?,
        sold=?
    WHERE id=?
    """, (
    product_name,
    manufacturer,
    model,
    category,
    memo,
    buy_price,
    sell_price,
    profit,
    recommendation,
    sold,
    history_id
))

    conn.commit()
    conn.close()