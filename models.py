import sqlite3

# ===============================
# Clase Producto
# ===============================
class Producto:
    def __init__(self, id_producto, nombre, cantidad, precio):
        self.id_producto = id_producto
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio


# ===============================
# Clase Inventario
# ===============================
class Inventario:
    def __init__(self, db_path="inventario.db"):
        self.db_path = db_path
        self._crear_tabla()

    # Crear tabla si no existe
    def _crear_tabla(self):
        conexion = sqlite3.connect(self.db_path)
        cursor = conexion.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS productos (
                            id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
                            nombre TEXT NOT NULL,
                            cantidad INTEGER NOT NULL,
                            precio REAL NOT NULL
                        )''')
        conexion.commit()
        conexion.close()

    # ===============================
    # CRUD - Operaciones
    # ===============================

    # Obtener todos los productos
    def obtener_productos(self):
        conexion = sqlite3.connect(self.db_path)
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM productos")
        filas = cursor.fetchall()
        conexion.close()
        return [Producto(*fila) for fila in filas]

    # Obtener producto por ID
    def obtener_producto_por_id(self, id_producto):
        conexion = sqlite3.connect(self.db_path)
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM productos WHERE id_producto = ?", (id_producto,))
        fila = cursor.fetchone()
        conexion.close()
        if fila:
            return Producto(*fila)
        return None

    # Añadir producto
    def añadir_producto(self, producto):
        conexion = sqlite3.connect(self.db_path)
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO productos (nombre, cantidad, precio) VALUES (?, ?, ?)",
                       (producto.nombre, producto.cantidad, producto.precio))
        conexion.commit()
        conexion.close()

    # Actualizar producto
    def actualizar_producto(self, id_producto, nombre, cantidad, precio):
        conexion = sqlite3.connect(self.db_path)
        cursor = conexion.cursor()
        cursor.execute('''UPDATE productos 
                          SET nombre = ?, cantidad = ?, precio = ? 
                          WHERE id_producto = ?''',
                       (nombre, cantidad, precio, id_producto))
        conexion.commit()
        conexion.close()

    # Eliminar producto
    def eliminar_producto(self, id_producto):
        conexion = sqlite3.connect(self.db_path)
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM productos WHERE id_producto = ?", (id_producto,))
        conexion.commit()
        conexion.close()
