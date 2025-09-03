import sqlite3

class Producto:
    def __init__(self, id_producto, nombre, cantidad, precio):
        self.id_producto = id_producto
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio

class Inventario:
    def __init__(self):
        self.conn = sqlite3.connect("inventario.db", check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.crear_tabla()

    def crear_tabla(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS productos (
                id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                cantidad INTEGER NOT NULL,
                precio REAL NOT NULL
            )
        ''')
        self.conn.commit()

    def añadir_producto(self, producto):
        self.cursor.execute(
            "INSERT INTO productos (nombre, cantidad, precio) VALUES (?, ?, ?)",
            (producto.nombre, producto.cantidad, producto.precio)
        )
        self.conn.commit()

    def eliminar_producto(self, id_producto):
        self.cursor.execute("DELETE FROM productos WHERE id_producto = ?", (id_producto,))
        self.conn.commit()

    def actualizar_producto(self, id_producto, nombre, cantidad, precio):
        self.cursor.execute(
            "UPDATE productos SET nombre = ?, cantidad = ?, precio = ? WHERE id_producto = ?",
            (nombre, cantidad, precio, id_producto)
        )
        self.conn.commit()

    def buscar_producto(self, nombre):
        self.cursor.execute("SELECT * FROM productos WHERE nombre LIKE ?", ('%' + nombre + '%',))
        filas = self.cursor.fetchall()
        return [Producto(*fila) for fila in filas]

    def obtener_productos(self):
        self.cursor.execute("SELECT * FROM productos")
        filas = self.cursor.fetchall()
        return [Producto(*fila) for fila in filas]
