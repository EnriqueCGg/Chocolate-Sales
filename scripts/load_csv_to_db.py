import os
import csv
import psycopg
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

def create_tables():
    DDL_SQL = """
    CREATE TABLE IF NOT EXISTS customers(
        customer_id TEXT PRIMARY KEY,
        age INT,
        gender TEXT,
        loyalty_member BOOLEAN,
        join_date DATE
    );
    CREATE TABLE IF NOT EXISTS products (
        product_id TEXT PRIMARY KEY,
        product_name TEXT,
        brand TEXT,
        category TEXT,
        cocoa_percent INT,
        weight_g INT
    );
    CREATE TABLE IF NOT EXISTS stores (
        store_id TEXT PRIMARY KEY,
        store_name TEXT,
        city TEXT,
        country TEXT,
        store_type TEXT
    );
    CREATE TABLE IF NOT EXISTS calendar (
        date DATE PRIMARY KEY,
        year INT,
        month INT,
        day INT,
        week INT,
        day_of_week INT
    );
    CREATE TABLE IF NOT EXISTS sales (
        order_id TEXT PRIMARY KEY,
        order_date DATE,
        product_id TEXT REFERENCES products(product_id),
        store_id TEXT REFERENCES stores(store_id),
        customer_id TEXT REFERENCES customers(customer_id),
        quantity INT,
        unit_price NUMERIC(10,2),
        discount NUMERIC(10,2),
        revenue NUMERIC(10,2),
        cost NUMERIC(10,2),
        profit NUMERIC(10,2)
    );
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(DDL_SQL)
            conn.commit()
    print("✅ Tables created or already exist.")

def load_csv(file_name, query):
    path = os.path.join('data', file_name)
    if not os.path.exists(path):
        print(f"⚠️ Warning: {file_name} not found in /data folder.")
        return
    
    with get_connection() as conn:
        with conn.cursor() as cur:
            with open(path, encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader) # Skip header
                for row in reader:
                    cur.execute(query, row)
            conn.commit()
    print(f"✅ Data from {file_name} loaded.")

if __name__ == "__main__":
    create_tables()
    
    # Load independent tables first
    load_csv('customers.csv', "INSERT INTO customers VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING")
    load_csv('products.csv', "INSERT INTO products VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING")
    load_csv('calendar.csv', "INSERT INTO calendar VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING")
    
    # Check if you have stores.csv, if not this will just skip
    load_csv('stores.csv', "INSERT INTO stores VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING")
    
    # Load sales last (depends on others)
    load_csv('sales.csv', """
        INSERT INTO sales (order_id, order_date, product_id, store_id, customer_id, quantity, unit_price, discount, revenue, cost, profit)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING
    """)