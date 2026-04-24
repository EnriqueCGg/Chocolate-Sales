
# 🍫 Chocolate Factory - Data Engineering & API

This project implements a full Data Engineering workflow: from raw CSV data to a containerized PostgreSQL database, culminating in a **FastAPI** RestAPI to monitor business KPIs. It was developed as part of the Data Science and AI program at **UPY**.



## 🚀 Features
* **Automated ETL**: Python scripts to clean and load 50,000+ sales records.
* **Relational Integrity**: Fully mapped database with Foreign Key constraints (viewable in DBeaver).
* **Data Cleaning**: Automatic handling of orphan records (e.g., missing product IDs like `P0000`).
* **KPI Endpoints**: Real-time business metrics (Revenue, Profit, Top Products).
* **Dockerized**: Isolated PostgreSQL environment for easy deployment and consistency.

---

## 🛠️ Tech Stack
* **Language**: Python 3.14
* **Database**: PostgreSQL 15 (Docker)
* **API Framework**: FastAPI + Uvicorn
* **Database Driver**: Psycopg 3 (with `dict_row` support for JSON responses)

---

## 📋 Prerequisites
* **Docker Desktop** (must be running)
* **Python 3.10+**
* **Git**

---

## ⚙️ Installation & Setup

### 1. Clone the repository
```bash
git clone [https://github.com/EnriqueCGg/Chocolate-Sales.git](https://github.com/EnriqueCGg/Chocolate-Sales.git)
cd Chocolate-Sales
```

### 2. Configure Environment Variables
Create a `.env` file in the root directory (use `.env.example` as a template):
```bash
cp .env.example .env
```
> **Note**: Ensure the credentials in `.env` match the environment variables defined in your `docker-compose.yml`.

### 3. Spin up the Database
```bash
docker compose up -d
```

### 4. Install Dependencies
```bash
python3 -m venv .venv
source .venv/bin/activate  # Mac/Linux
pip install -r requirements.txt
```

### 5. Run the ETL Pipeline
This script recreates the tables with proper constraints, handles missing data, and loads the CSV data into Postgres:
```bash
python3 scripts/load_csv_to_db.py
```

---

## 🖥️ Running the API
Start the FastAPI server using Uvicorn:
```bash
uvicorn app.main:app --reload
```

### Interactive Documentation
Once the server is running, explore the API and test the endpoints directly from your browser:
* **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* **Redoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)



---

## 📊 Available KPIs
| Endpoint | Description |
| :--- | :--- |
| `/kpi/total-revenue` | Returns the sum of all sales revenue. |
| `/kpi/top-profitable-products` | Lists the top 5 products by profit margin. |
| `/kpi/performance-by-city` | Ranks cities based on order volume and revenue. |
| `/kpi/category-sales` | Breakdown of units sold per chocolate category. |

---

## 🤝 Collaborators
* **Enrique Arturo Emmanuel Chi Góngora** - *Data Science & AI (UPY)*
* **Saul Ruiz Peña**
* **Kevin Daniel Castellanos Chan**

---

### 💡 Pro Tip for DBeaver
To visualize the "lines" (relationships) we established: 
1. Connect DBeaver to `localhost:5432`.
2. Open the `chocolate_db` database.
3. Select the `sales` table and click on the **ER Diagram** tab.
```

How does this look for your repo?