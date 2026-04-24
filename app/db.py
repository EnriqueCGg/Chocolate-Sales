from collections.abc import Generator
from app import settings

def get_conn() -> Generator[object, None, None]:
    """
    Gestiona la conexión a PostgreSQL utilizando la configuración de settings.py.
    Usa dict_row para que FastAPI reciba diccionarios y genere JSON automáticamente.
    """
    import psycopg
    from psycopg.rows import dict_row

    # Se conecta usando el PSYCOPG_DSN que ya construimos en settings.py
    conn = psycopg.connect(
        settings.PSYCOPG_DSN, 
        row_factory=dict_row
    )
    
    # Autocommit True para que los cambios se guarden sin necesidad de conn.commit()
    conn.autocommit = True
    
    try:
        yield conn
    finally:
        # Cerramos la conexión al finalizar la petición HTTP
        conn.close()