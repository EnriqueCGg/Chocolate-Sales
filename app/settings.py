import os
from dotenv import load_dotenv

load_dotenv()

def required(name: str) -> str:
    v = os.getenv(name)
    if v is None or v.strip() == "":
        raise RuntimeError(f"Missing environment variable: {name}")
    return v.strip()

def optional(name: str, default: str = "") -> str:
    v = os.getenv(name)
    return default if v is None else v.strip()

# Configuración General
APP_NAME = "Chocolate-Factory-API"

# Configuración de Base de Datos (Fijado a Postgres)
DB_HOST = required("DB_HOST")
DB_PORT = int(required("DB_PORT"))
DB_NAME = required("DB_NAME")
DB_USER = required("DB_USER")
DB_PASSWORD = optional("DB_PASSWORD", "")

# DSN optimizado para psycopg3
# Usamos el formato de URI que es más estándar y compatible
PSYCOPG_DSN = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# Flags de utilidad
IS_POSTGRES = True