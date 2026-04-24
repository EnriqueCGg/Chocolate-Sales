# RestAPI - Proyecto Integrador

Proyecto de REST API para gestionar clientes, productos y ventas usando Python y FastAPI.

Soporta dos opciones de bases de datos:
- **MySQL** (recomendado para comenzar)
- **PostgreSQL** (alternativa avanzada)

## Requisitos previos

- Python 3.8+
- pip (gestor de paquetes de Python)
- **Una de estas opciones:**
  - **MySQL Server** instalado y en funcionamiento (puedes usar MySQL Workbench como interfaz gráfica)
  - **PostgreSQL** instalado y en funcionamiento

## Pasos de instalación

### 1. Clonar o descargar el proyecto

```bash
cd /ruta/del/proyecto
```

### 2. Crear y activar el ambiente virtual

```bash
# Crear el ambiente virtual
python -m venv .venv

# Activar el ambiente (macOS/Linux)
source .venv/bin/activate

# Activar el ambiente (Windows)
# .venv\Scripts\activate
```

### 3. Instalar las dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar las variables de entorno

Copia el archivo `.env.example` a `.env`:

```bash
cp .env.example .env
```

#### Opción A: MySQL (recomendado)

Edita el archivo `.env` con tus credenciales de MySQL:

```dotenv
DB_HOST=localhost          # Host de tu base de datos (generalmente localhost)
DB_PORT=3306              # Puerto (por defecto 3306 para MySQL)
DB_NAME=store_db          # Nombre de la base de datos
DB_USER=root              # Usuario de MySQL (por defecto root)
DB_PASSWORD=tu_contraseña # Tu contraseña de MySQL
```

**Importante:** Asegúrate de que:
- MySQL está corriendo (verifica en MySQL Workbench que el servidor local esté activo)
- La base de datos `store_db` existe o será creada automáticamente por el seed script
- Las credenciales sean correctas (usuario y contraseña que configuraste en MySQL)

#### Opción B: PostgreSQL

Edita el archivo `.env` con tus credenciales de PostgreSQL:

```dotenv
DB_HOST=localhost          # Host de tu base de datos (generalmente localhost)
DB_PORT=5432              # Puerto (por defecto 5432 para PostgreSQL)
DB_NAME=store_db          # Nombre de la base de datos
DB_USER=postgres          # Usuario de PostgreSQL (por defecto postgres)
DB_PASSWORD=tu_contraseña # Tu contraseña de PostgreSQL
```

**Importante:** Asegúrate de que:
- PostgreSQL está corriendo (`brew services start postgresql` en macOS)
- La base de datos `store_db` existe o será creada automáticamente por el seed script
- Las credenciales sean correctas

### 5. Ejecutar el seed (pobla la base de datos)

#### Para MySQL:

```bash
# Primera ejecución (crea tablas e inserta datos)
python scripts/seed_db_mysql.py

# Para reiniciar y recrear las tablas:
python scripts/seed_db_mysql.py --reset
```

#### Para PostgreSQL:

```bash
# Primera ejecución (crea tablas e inserta datos)
python scripts/seed_db_postgres.py

# Para reiniciar y recrear las tablas:
python scripts/seed_db_postgres.py --reset
```

Esto creará 3 tablas:
- **clients**: 5 clientes de ejemplo
- **products**: 6 productos de ejemplo
- **sales**: 12 transacciones de ejemplo

## 6. Levantar el servidor

Una vez que has completado los pasos anteriores y la base de datos está poblada con datos, puedes iniciar el servidor FastAPI:

```bash
# Asegúrate de que tu ambiente virtual está activado
source .venv/bin/activate  # en macOS/Linux

# Ejecuta el servidor
uvicorn app.main:app --reload
```

Deberías ver algo como:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started server process [XXXXX]
```

El servidor estará disponible en: **http://localhost:8000**

## 7. Probar la API

### Opción A: Con FastAPI Swagger UI (Recomendado)

FastAPI incluye una interfaz interactiva automáticamente:

```
http://localhost:8000/docs
```

Ahí puedes ver todos los endpoints disponibles y probarlos directamente desde el navegador.

### Opción B: Con cURL

```bash
# Obtener lista de clientes
curl http://localhost:8000/clients

# Ejemplo de salida:
[
  {"client_id": 1, "full_name": "Ana García", "email": "ana@example.com", "created_at": "2026-02-20T10:00:00"},
  {"client_id": 2, "full_name": "Luis Pérez", "email": "luis@example.com", "created_at": "2026-02-20T10:01:00"},
  ...
]
```

### Opción C: Con Postman

1. Abre Postman (descárgalo desde https://www.postman.com/downloads/)
2. Crea una nueva request:
   - **Método:** GET
   - **URL:** http://localhost:8000/clients
   - **Headers:** (vacío por defecto está bien)
3. Haz clic en "Send"
4. Verás la respuesta JSON con la lista de clientes

**Ejemplo de request en Postman:**
```
GET http://localhost:8000/clients
Accept: application/json
```

## Estructura del proyecto

```
RestAPI/
├── app/
│   ├── __init__.py            # Inicializador del paquete app
│   ├── main.py                # Definición de la aplicación FastAPI y endpoints
│   ├── db.py                  # Funciones de conexión a la base de datos
│   ├── settings.py            # Configuración y variables de entorno
│   └── __pycache__/           # Caché de Python (no commitear)
├── scripts/
│   ├── seed_db_mysql.py       # Script para poblar la base de datos MySQL
│   └── seed_db_postgres.py    # Script para poblar la base de datos PostgreSQL
├── .env.example               # Plantilla de variables de entorno
├── .env                       # Variables de entorno (no commitear a Git)
├── .venv/                     # Ambiente virtual (no commitear a Git)
├── requirements.txt           # Dependencias del proyecto
└── README.md                  # Este archivo
```

### Descripción de archivos en `app/`:

- **main.py**: Contiene la instancia de la aplicación FastAPI y define todos los endpoints (rutas) de la API
- **db.py**: Gestiona la conexión a la base de datos, incluye la función `get_conn()` que establece conexiones según el tipo de base de datos configurado
- **settings.py**: Carga las variables de entorno del archivo `.env` y define constantes como `APP_NAME` e `IS_MYSQL`

## Solución de problemas

### Error: "Missing environment variable"
- Verifica que existe el archivo `.env`
- Comprueba que todas las variables requeridas están configuradas correctamente

### Error: "No puedo conectar a la base de datos"

**Para MySQL:**
- Asegúrate que MySQL está corriendo:
  - En macOS: abre MySQL Workbench o ejecuta `brew services start mysql-community-server`
  - En Windows: verifica que el servicio MySQL está iniciado en Services
- Verifica el host y puerto en `.env` (por defecto localhost:3306)

**Para PostgreSQL:**
- Asegúrate que PostgreSQL está corriendo:
  - En macOS: ejecuta `brew services start postgresql`
  - En Windows: verifica que el servicio PostgreSQL está iniciado en Services
- Verifica el host y puerto en `.env` (por defecto localhost:5432)

### Error: "Access denied for user" o "FATAL: password authentication failed"
- Verifica que el usuario y contraseña en `.env` son correctos
- Asegúrate de que el usuario tiene permisos para crear bases de datos

### Error: "Seed skipped: data already exists"
- Usa `python scripts/seed_db_mysql.py --reset` (para MySQL) o `python scripts/seed_db_postgres.py --reset` (para PostgreSQL) para recrear desde cero


## Datos de ejemplo

Después de ejecutar el seed, tendrás:

**Clientes:**
- Ana García
- Luis Pérez
- María López
- Carlos Sánchez
- Sofía Ramírez

**Productos:**
- Teclado Mecánico ($899)
- Mouse Inalámbrico ($399)
- Termo Acero ($249)
- Playera Deportiva ($299)
- Cuaderno A4 ($79)
- Chocolate 70% ($59)

**Ventas:** 12 transacciones de ejemplo con diferentes estados (PAID, PENDING, CANCELLED)

---

**Autor:** Diplomado en Java y Python - Universidad Anáhuac Mayab  
**Fecha:** 2026
