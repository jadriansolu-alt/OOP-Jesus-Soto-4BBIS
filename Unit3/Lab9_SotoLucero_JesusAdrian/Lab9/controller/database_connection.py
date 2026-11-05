import psycopg
from psycopg.rows import dict_row
from controller.config import db_config

class Database_connection:
    def __init__(self):
        self.config = db_config

    def get_connection(self):
        try:
            return psycopg.connect(
                host=self.config.get('host', 'localhost'),
                user=self.config.get('user', 'postgres'),
                password=str(self.config.get('password', '')),
                dbname=self.config.get('database', 'login_system_db'),
                port=self.config.get('port', 5432)
            )
        except Exception as e:
            print(f"Error de conexión: {e}")
            return None

    def ejecutar_consulta(self, query, params=()):
        conexion = self.get_connection()
        if not conexion:
            return None
        try:
            with conexion.cursor(row_factory=dict_row) as cursor:
                cursor.execute(query, params)
                return cursor.fetchall()
        except Exception as e:
            print(f"Error SQL: {e}")
            return None
        finally:
            if conexion:
                conexion.close()
