"""
Módulo de base de datos para Happy Burger.

Administra la conexión a SQLite y la creación de las tablas necesarias
(con integridad referencial mediante el uso de foreign keys).

Proyecto Happy Burguer para la clase de Python Avanzado del curso de Fullstack developer de TecMilenio.
Autor: Jose Bernardo Moya Jimenez
Fecha: 2024-12-4
email: bmjimenez@hotmail.com

"""
#Importaciones
import os
import sqlite3

# Nombre del archivo de base de datos de SQLite para el Proyecto Happy Burger
DB_NAME = "dbSqlite.db"

# Obtiene la ruta absoluta al archivo de base de datos.
def get_db_path():
    # Carpeta raíz del proyecto (un nivel arriba de /db)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, DB_NAME)

"""
Esta funcion obtiene una conexión a la base de datos SQLite.
    - Usa ruta absoluta al archivo dbSqlite.db
    - Aumenta timeout a 10 segundos para evitar el error de 'database is locked' que me daba en el frontend
    - Desactiva la restricción de thread de SQLite para usarla con Flask y sus threads
    - Usa Row factory para acceder a columnas por nombre
    - Activa foreign_keys y WAL para mejor integridad y concurrencia
"""
def get_connection():
    
    db_path = get_db_path()
    conn = sqlite3.connect(
        db_path,
        timeout=10,             # espera hasta 10s si la DB está ocupada
        check_same_thread=False # permite uso en distintos threads de Flask
    )
    conn.row_factory = sqlite3.Row # utilizamos esta linea para acceder a columnas por nombre

    # Activar foreign_keys
    conn.execute("PRAGMA foreign_keys = ON;")
    # (Opcional, pero ayuda con concurrencia)
    conn.execute("PRAGMA journal_mode = WAL;")

    return conn

# Crea las tablas Clientes, Menu y Pedido si no existen.
def init_db():
    with get_connection() as conn:
        cur = conn.cursor()

        # Crea Tabla Clientes
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS Clientes (
                IdCliente INTEGER PRIMARY KEY,
                nombre TEXT NOT NULL,
                direccion TEXT NOT NULL,
                correo_electronico TEXT NOT NULL,
                telefono TEXT NOT NULL
            );
            """
        )

        # Crea Tabla Menu
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS Menu (
                IdMenu INTEGER PRIMARY KEY,
                nombre TEXT NOT NULL,
                precio REAL NOT NULL
            );
            """
        )

        # Crea Tabla Pedido con foreign keys hacia Clientes y Menu
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS Pedido (
                IdPedido   INTEGER PRIMARY KEY,
                IdCliente  INTEGER NOT NULL,
                IdMenu     INTEGER NOT NULL,
                cliente    TEXT NOT NULL,
                producto   TEXT NOT NULL,
                precio     REAL NOT NULL,
                FOREIGN KEY (IdCliente) REFERENCES Clientes(IdCliente),
                FOREIGN KEY (IdMenu)   REFERENCES Menu(IdMenu)
            );
            """
        )

        conn.commit()
        cur.close()
