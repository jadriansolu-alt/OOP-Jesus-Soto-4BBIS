from controller.database_connection import Database_connection

class Usuario:
    def __init__(self, username, password, nombre=""):
        self.username = username
        self.password = password
        self.nombre = nombre
        self.db = Database_connection()

    def autenticar(self):
        query = "SELECT * FROM users WHERE username = %s AND pass = %s;"
        result = self.db.ejecutar_consulta(query, (self.username, self.password))
        return result[0] if result else None

    def registrar(self):
        query = """
            INSERT INTO users (username, pass, nombre) 
            VALUES (%s, %s, %s) 
            RETURNING id;
        """
        conexion = self.db.get_connection()
        if not conexion:
            return False
        try:
            with conexion.cursor() as cursor:
                cursor.execute(query, (self.username, self.password, self.nombre))
                conexion.commit()
                return True
        except Exception as e:
            print(f"Error registro: {e}")
            conexion.rollback()
            return False
        finally:
            conexion.close()
