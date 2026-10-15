from controller.database_connection import Database_connection

class Usuario:
    def __init__(self, username, password, nombre=""):
        self.username = username
        self.password = password
        self.nombre = nombre
        self.db = Database_connection()

    def autenticar(self):
        """Valida las credenciales del usuario en PostgreSQL."""
        query = "SELECT * FROM login_system_db.users WHERE username = %s AND pass = %s;"
        result = self.db.ejecutar_consulta(query, (self.username, self.password))
        if result:
            return result[0]  # Retorna el diccionario con la información del usuario
        return None

    def registrar(self):
        """Inserta un nuevo usuario en la base de datos PostgreSQL."""
        query = """
            INSERT INTO login_system_db.users (username, pass, nombre) 
            VALUES (%s, %s, %s) 
            RETURNING id;
        """
        conexion = self.db.get_connection()
        if not conexion:
            return False
            
        try:
            with conexion.cursor() as cursor:
                cursor.execute(query, (self.username, self.password, self.nombre))
                nuevo_id = cursor.fetchone()[0]
                conexion.commit()  # Confirma los cambios en la base de datos
                print(f"Usuario registrado exitosamente con ID: {nuevo_id}")
                return True
        except Exception as e:
            print(f"Error al registrar usuario: {e}")
            conexion.rollback()
            return False
        finally:
            conexion.close()