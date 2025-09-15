from flask import Flask, render_template, request, redirect, url_for, jsonify
from conexion.conexion import app, db
import os, json, csv

# ===============================
# Configuración de la aplicación
# ===============================
app.config['DEBUG'] = True
app.config['PROPAGATE_EXCEPTIONS'] = True

# ===============================
# Modelo de datos en MySQL
# ===============================
class Producto(db.Model):
    __tablename__ = "producto"   # importante: coincidir con la tabla en MySQL

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<Producto {self.nombre}>"

# ===============================
# Funciones de persistencia en archivos
# ===============================
def guardar_en_txt(producto):
    ruta = "datos/datos.txt"
    with open(ruta, "a") as f:
        f.write(f"{producto['nombre']},{producto['cantidad']},{producto['precio']}\n")

def leer_de_txt():
    productos = []
    ruta = "datos/datos.txt"
    if os.path.exists(ruta):
        with open(ruta, "r") as f:
            for linea in f:
                nombre, cantidad, precio = linea.strip().split(",")
                productos.append({"nombre": nombre, "cantidad": int(cantidad), "precio": float(precio)})
    return productos

def guardar_en_json(producto):
    ruta = "datos/datos.json"
    productos = []
    if os.path.exists(ruta):
        with open(ruta, "r") as f:
            try:
                productos = json.load(f)
            except:
                productos = []
    productos.append(producto)
    with open(ruta, "w") as f:
        json.dump(productos, f, indent=4)

def leer_de_json():
    ruta = "datos/datos.json"
    if os.path.exists(ruta):
        with open(ruta, "r") as f:
            return json.load(f)
    return []

def guardar_en_csv(producto):
    ruta = "datos/datos.csv"
    existe = os.path.exists(ruta)
    with open(ruta, "a", newline="") as f:
        writer = csv.writer(f)
        if not existe:
            writer.writerow(["nombre", "cantidad", "precio"])
        writer.writerow([producto['nombre'], producto['cantidad'], producto['precio']])

def leer_de_csv():
    productos = []
    ruta = "datos/datos.csv"
    if os.path.exists(ruta):
        with open(ruta, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                productos.append({
                    "nombre": row["nombre"],
                    "cantidad": int(row["cantidad"]),
                    "precio": float(row["precio"])
                })
    return productos

# ===============================
# Rutas principales
# ===============================
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/formulario", methods=["GET", "POST"])
def formulario():
    try:
        if request.method == "POST":
            nombre = request.form["nombre"]
            cantidad = int(request.form["cantidad"])
            precio = float(request.form["precio"])

            nuevo_producto = {"nombre": nombre, "cantidad": cantidad, "precio": precio}

            # Guardar en archivos
            guardar_en_txt(nuevo_producto)
            guardar_en_json(nuevo_producto)
            guardar_en_csv(nuevo_producto)

            # Guardar en MySQL
            producto_db = Producto(nombre=nombre, cantidad=cantidad, precio=precio)
            db.session.add(producto_db)
            db.session.commit()

            return redirect(url_for("listar_todos"))

        return render_template("formulario.html")

    except Exception as e:
        # Mostramos el error en consola y en navegador
        import traceback
        print("❌ ERROR EN /formulario:")
        traceback.print_exc()
        return jsonify({"error": str(e)})

@app.route("/listar_todos")
def listar_todos():
    productos_db = Producto.query.all()
    productos_txt = leer_de_txt()
    productos_json = leer_de_json()
    productos_csv = leer_de_csv()
    return render_template("resultado.html",
                           productos_db=productos_db,
                           productos_txt=productos_txt,
                           productos_json=productos_json,
                           productos_csv=productos_csv)

# ===============================
# Rutas API
# ===============================
@app.route("/api/txt")
def api_txt():
    return jsonify(leer_de_txt())

@app.route("/api/json")
def api_json():
    return jsonify(leer_de_json())

@app.route("/api/csv")
def api_csv():
    return jsonify(leer_de_csv())

# ===============================
# Ruta para probar conexión con MySQL
# ===============================
@app.route("/test_db")
def test_db():
    try:
        result = db.session.execute("SELECT 1").scalar()
        return jsonify({"conexion": "exitosa", "resultado": result})
    except Exception as e:
        return jsonify({"error": str(e)})

# ===============================
# Inicializar la BD
# ===============================
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # crea tablas si no existen
    app.run(debug=True)


