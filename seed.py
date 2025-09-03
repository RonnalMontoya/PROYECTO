from models import Inventario, Producto

# Crear inventario
inventario = Inventario()

# Borrar productos previos (vaciar tabla)
inventario.cursor.execute("DELETE FROM productos")
inventario.conn.commit()

# Lista de productos iniciales
productos = [
    Producto(None, "Pan Tradicional", 50, 0.25),
    Producto(None, "Torta de Chocolate", 10, 15.00),
    Producto(None, "Galletas de Vainilla", 100, 0.50),
    Producto(None, "Pan Integral", 40, 0.35),
    Producto(None, "Croissant", 25, 0.80),
    Producto(None, "Donas Glaseadas", 30, 0.60),
    Producto(None, "Bizcocho de Naranja", 12, 8.00),
    Producto(None, "Pan de Queso", 35, 0.50),
    Producto(None, "Brownies", 20, 1.20),
    Producto(None, "Empanadas de Pollo", 18, 1.50),
    Producto(None, "Pastel de Zanahoria", 8, 12.00),
    Producto(None, "Pan de Ajo", 22, 0.70),
    Producto(None, "Muffins de Arándanos", 15, 1.80),
    Producto(None, "Tarta de Manzana", 7, 10.00),
    Producto(None, "Baguette", 25, 1.00),
    Producto(None, "Pan de Leche", 40, 0.40),
    Producto(None, "Alfajores", 50, 0.75),
    Producto(None, "Tarta de Fresas", 6, 14.00),
    Producto(None, "Pan de Centeno", 20, 0.90),
    Producto(None, "Eclairs", 15, 1.50),
]

# Insertar productos en la base de datos
for p in productos:
    inventario.añadir_producto(p)

print("✅ Base de datos reseteada y 20 productos añadidos.")
