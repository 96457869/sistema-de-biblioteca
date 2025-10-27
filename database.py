import mysql.connector
from mysql.connector import Error
import logging

class DBConector:
    def __init__(self, host='localhost', database='sistema_biblioteca', 
                 user='biblioteca_user', password='password_seguro'):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.connection = None
        self.logger = logging.getLogger(__name__)

    def connect(self):
        """Establece conexión segura con la base de datos"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                charset='utf8mb4',
                collation='utf8mb4_unicode_ci'
            )
            
            if self.connection.is_connected():
                self.logger.info("Conexión exitosa a la base de datos MySQL")
                return True
            else:
                self.logger.error("No se pudo establecer conexión")
                return False
                
        except Error as e:
            self.logger.error(f"Error de conexión: {e}")
            return False

    def execute_query(self, query, params=None):
        """Ejecuta consultas INSERT, UPDATE, DELETE de forma segura"""
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()
            
            cursor = self.connection.cursor()
            cursor.execute(query, params or ())
            self.connection.commit()
            cursor.close()
            return True
            
        except Error as e:
            self.logger.error(f"Error en execute_query: {e}")
            self.connection.rollback()
            return False

    def fetch_one(self, query, params=None):
        """Ejecuta consulta y retorna un solo resultado"""
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()
            
            cursor = self.connection.cursor()
            cursor.execute(query, params or ())
            result = cursor.fetchone()
            cursor.close()
            return result
            
        except Error as e:
            self.logger.error(f"Error en fetch_one: {e}")
            return None

    def fetch_all(self, query, params=None):
        """Ejecuta consulta y retorna todos los resultados"""
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()
            
            cursor = self.connection.cursor()
            cursor.execute(query, params or ())
            results = cursor.fetchall()
            cursor.close()
            return results
            
        except Error as e:
            self.logger.error(f"Error en fetch_all: {e}")
            return []

    def close(self):
        """Cierra la conexión de forma segura"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            self.logger.info("Conexión cerrada")

    def __enter__(self):
        """Para usar con 'with' statement"""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Cierra conexión automáticamente"""
        self.close()