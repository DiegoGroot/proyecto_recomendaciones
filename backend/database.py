import mysql.connector
from mysql.connector import pooling
import os
from dotenv import load_dotenv

load_dotenv()

db_config = {
    "host":     os.getenv("DB_HOST", "localhost"),
    "user":     os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "sira"),
    "port":     int(os.getenv("DB_PORT", 3306)),
}

connection_pool = pooling.MySQLConnectionPool(
    pool_name="sira_pool",
    pool_size=5,
    **db_config
)

def get_db():
    conn = connection_pool.get_connection()
    try:
        yield conn
    finally:
        conn.close()
