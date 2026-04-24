from fastapi import FastAPI, Depends, HTTPException
from app.db import get_conn
from app.settings import APP_NAME

app = FastAPI(title=APP_NAME)

@app.get("/")
def root():
    return {"message": f"Bienvenido a {APP_NAME}", "status": "Ready"}

# KPI 1: Ventas Totales (Revenue)
@app.get("/kpi/total-revenue")
def get_total_revenue(conn=Depends(get_conn)):
    with conn.cursor() as cur:
        cur.execute("SELECT SUM(revenue) as total_revenue FROM sales")
        result = cur.fetchone()
        return result

# KPI 2: Top 5 Productos con más Ganancia (Profit)
@app.get("/kpi/top-profitable-products")
def get_top_products(conn=Depends(get_conn)):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT p.product_name, SUM(s.profit) as total_profit
            FROM sales s
            JOIN products p ON s.product_id = p.product_id
            GROUP BY p.product_name
            ORDER BY total_profit DESC
            LIMIT 5
        """)
        return cur.fetchall()

# KPI 3: Desempeño por Ciudad (Tiendas)
@app.get("/kpi/performance-by-city")
def get_city_performance(conn=Depends(get_conn)):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT st.city, COUNT(s.order_id) as total_orders, SUM(s.revenue) as total_revenue
            FROM sales s
            JOIN stores st ON s.store_id = st.store_id
            GROUP BY st.city
            ORDER BY total_revenue DESC
        """)
        return cur.fetchall()

# KPI 4: Ventas por Categoría de Chocolate
@app.get("/kpi/category-sales")
def get_category_sales(conn=Depends(get_conn)):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT p.category, SUM(s.quantity) as total_units_sold
            FROM sales s
            JOIN products p ON s.product_id = p.product_id
            GROUP BY p.category
            ORDER BY total_units_sold DESC
        """)
        return cur.fetchall()