from controller.database_connection import Database_connection

class Producto:
    def __init__(self, nombre="", precio=0.0, stock=0):
        self.nombre = nombre
        self.precio = precio
        self.stock = stock
        self.db = Database_connection()

    def obtener_todos(self):
        query = "SELECT id, nombre, precio, stock FROM productos ORDER BY id ASC;"
        return self.db.ejecutar_consulta(query)

    def guardar(self):
        query = """
            INSERT INTO productos (nombre, precio, stock) 
            VALUES (%s, %s, %s) 
            RETURNING id;
        """
        conexion = self.db.get_connection()
        if not conexion:
            return False
        try:
            with conexion.cursor() as cursor:
                cursor.execute(query, (self.nombre, self.precio, self.stock))
                conexion.commit()
                return True
        except Exception as e:
            print(f"Error al guardar: {e}")
            conexion.rollback()
            return False
        finally:
            conexion.close()
