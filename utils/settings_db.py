import sqlite3

DB_NAME = "settings.db"


def init_settings():

    conn = sqlite3.connect(DB_NAME)

    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS settings (
        id INTEGER PRIMARY KEY,
        judge_type TEXT,
        buy_profit INTEGER,
        consider_profit INTEGER,
        buy_roi REAL,
        consider_roi REAL
    )
    """)

    cur.execute("""
    INSERT OR IGNORE INTO settings (
        id,
        judge_type,
        buy_profit,
        consider_profit,
        buy_roi,
        consider_roi
    )
    VALUES (
        1,
        '利益額＋ROI',
        3000,
        1000,
        30,
        15
    )
    """)

    conn.commit()
    conn.close()


def get_settings():

    conn = sqlite3.connect(DB_NAME)

    cur = conn.cursor()

    cur.execute("""
    SELECT
        judge_type,
        buy_profit,
        consider_profit,
        buy_roi,
        consider_roi
    FROM settings
    WHERE id=1
    """)

    row = cur.fetchone()

    conn.close()

    if row is None:

        init_settings()

        return {
            "judge_type": "利益額＋ROI",
            "buy_profit": 3000,
            "consider_profit": 1000,
            "buy_roi": 30,
            "consider_roi": 15
        }

    return {
        "judge_type": row[0],
        "buy_profit": row[1],
        "consider_profit": row[2],
        "buy_roi": row[3],
        "consider_roi": row[4]
    }

def save_settings(
    judge_type,
    buy_profit,
    consider_profit,
    buy_roi,
    consider_roi
):

    conn = sqlite3.connect(DB_NAME)

    cur = conn.cursor()

    cur.execute("""
    UPDATE settings
    SET
        judge_type=?,
        buy_profit=?,
        consider_profit=?,
        buy_roi=?,
        consider_roi=?
    WHERE id=1
    """, (
        judge_type,
        buy_profit,
        consider_profit,
        buy_roi,
        consider_roi
    ))

    conn.commit()
    conn.close()