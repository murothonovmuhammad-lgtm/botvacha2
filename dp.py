import sqlite3

DB_NAME = "database.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tg_id INTEGER UNIQUE,
        username TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tg_id INTEGER,
        product_name TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()

def add_order(tg_id: int, product_name: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO orders (tg_id, product_name) VALUES (?, ?)", (tg_id, product_name))    
    conn.commit()
    conn.close()

def get_user_order_count(tg_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT product_name, COUNT(*) 
        FROM orders 
        WHERE tg_id = ? 
        GROUP BY product_name
    """, (tg_id,))
    orders = cursor.fetchall()
    conn.close()
    return orders

def clear_orders(tg_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM orders WHERE tg_id = ?", (tg_id,))
    conn.commit()
    conn.close()

def delete_one_order(tg_id: int, product: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM orders 
        WHERE id = (
            SELECT id FROM orders 
            WHERE tg_id = ? AND product_name = ? 
            LIMIT 1
        )
    """, (tg_id, product))
    conn.commit() 
    conn.close()  