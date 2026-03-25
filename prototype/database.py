import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG

class Database:
    def __init__(self):
        self.connection = None
        self.cursor = None
    
    def connect(self):
        """Establece conexión con MySQL"""
        try:
            self.connection = mysql.connector.connect(**DB_CONFIG)
            self.cursor = self.connection.cursor(dictionary=True)
            print("✓ Conexión a MySQL exitosa")
            return True
        except Error as err:
            print(f"✗ Error conectando a MySQL: {err}")
            return False
    
    def disconnect(self):
        """Cierra la conexión con MySQL"""
        if self.connection:
            self.cursor.close()
            self.connection.close()
            print("✓ Conexión cerrada")
    
    def execute_query(self, query, params=None):
        """Ejecuta una consulta SELECT"""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchall()
        except Error as err:
            print(f"✗ Error en consulta: {err}")
            return None
    
    def execute_insert(self, query, params=None):
        """Ejecuta INSERT y retorna el ID del último registro"""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.connection.commit()
            return self.cursor.lastrowid
        except Error as err:
            self.connection.rollback()
            print(f"✗ Error en INSERT: {err}")
            return None
    
    def execute_update(self, query, params=None):
        """Ejecuta UPDATE o DELETE"""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.connection.commit()
            return self.cursor.rowcount
        except Error as err:
            self.connection.rollback()
            print(f"✗ Error en UPDATE/DELETE: {err}")
            return None

# Instancia global de base de datos
db = Database()
