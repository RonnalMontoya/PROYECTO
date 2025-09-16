# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from conexion.conexion import conexion, cerrar_conexion
from forms import ProductoForm
from datetime import datetime
import os, csv, json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'


# ======================================================
# Inyectar fecha en templates
# ======================================================
@app.context_processor
def inject_now():
    return {'now': datetime.utcnow}


# ======================================================
# Funciones para persistencia en archivos
# ======================================================
def guardar_en_txt(producto):
    ruta = "datos/datos.txt"
    with open(ruta, "a") as f:
        f.write(f"{producto['nombre']},{producto['cantidad']},{producto['precio']}\n")

def leer_de_txt():
    ruta = "datos/datos.txt"
    productos = []
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
    ruta = "datos/datos.csv"
    productos = []
    if os.path.exists(ruta):
        with open(ruta, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Normalizar claves a minúsculas
                row_normalizado = {k.lower(): v for k, v in row.items()}
                try:
                    productos.append({
                        "nombre": row_normalizado.get("nombre", ""),
                        "cantidad": int(row_normalizado.get("cantidad", 0)),
                        "precio": float(row_normalizado.get("precio", 0.0))
                    })
                except Exception as e:
                    print("Error procesando fila CSV:", row, e)
    return productos

# ======================================================
# Página principal
# ======================================================
@app.route('/')
def index():
    return render_template('index.html', title='Inicio')


# ======================================================
# Listar productos
# ======================================================
@app.route('/productos')
def listar_productos():
    q = request.args.get('q', '').strip()
    conn = conexion()
    cur = conn.cursor(dictionary=True)
    if q:
        cur.execute("SELECT id, nombre, cantidad, precio FROM producto WHERE nombre LIKE %s", (f"%{q}%",))
    else:
        cur.execute("SELECT id, nombre, cantidad, precio FROM producto")
    productos = cur.fetchall()
    cerrar_conexion(conn)
    return render_template('products/list.html', title='Productos', productos=productos, q=q)


# ======================================================
# Crear producto
# ======================================================
@app.route('/productos/nuevo', methods=['GET', 'POST'])
def crear_producto():
    form = ProductoForm()
    if form.validate_on_submit():
        conn = conexion()
        try:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO producto (nombre, cantidad, precio) VALUES (%s, %s, %s)",
                (form.nombre.data, form.cantidad.data, float(form.precio.data))
            )
            conn.commit()

            # Guardar también en TXT, JSON y CSV
            nuevo_producto = {
                "nombre": form.nombre.data,
                "cantidad": form.cantidad.data,
                "precio": float(form.precio.data)
            }
            guardar_en_txt(nuevo_producto)
            guardar_en_json(nuevo_producto)
            guardar_en_csv(nuevo_producto)

            flash("Producto agregado correctamente.", "success")
            return redirect(url_for('listar_productos'))
        except Exception as e:
            conn.rollback()
            flash(f"Error al guardar: {e}", "danger")
        finally:
            cerrar_conexion(conn)
    return render_template('products/form.html', title='Nuevo producto', form=form, modo='crear')


# ======================================================
# Editar producto
# ======================================================
@app.route('/productos/<int:pid>/editar', methods=['GET', 'POST'])
def editar_producto(pid):
    conn = conexion()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM producto WHERE id = %s", (pid,))
    prod = cursor.fetchone()
    if not prod:
        cerrar_conexion(conn)
        return "Producto no encontrado", 404

    form = ProductoForm(data=prod)
    if form.validate_on_submit():
        try:
            cursor.execute(
                "UPDATE producto SET nombre=%s, cantidad=%s, precio=%s WHERE id=%s",
                (form.nombre.data, form.cantidad.data, float(form.precio.data), pid)
            )
            conn.commit()
            flash("Producto actualizado correctamente.", "success")
            return redirect(url_for('listar_productos'))
        except Exception as e:
            conn.rollback()
            flash(f"Error al actualizar: {e}", "danger")
        finally:
            cerrar_conexion(conn)
    cerrar_conexion(conn)
    return render_template('products/form.html', title="Editar producto", form=form, modo="editar", pid=pid)


# ======================================================
# Eliminar producto
# ======================================================
@app.route('/productos/<int:pid>/eliminar', methods=['POST'])
def eliminar_producto(pid):
    conn = conexion()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM producto WHERE id = %s", (pid,))
    if cursor.rowcount > 0:
        conn.commit()
        flash("Producto eliminado correctamente.", "success")
    else:
        flash("Producto no encontrado.", "warning")
    cerrar_conexion(conn)
    return redirect(url_for('listar_productos'))


# ======================================================
# APIs para ver archivos
# ======================================================
@app.route("/api/txt")
def api_txt():
    return jsonify(leer_de_txt())

@app.route("/api/json")
def api_json():
    return jsonify(leer_de_json())

@app.route("/api/csv")
def api_csv():
    return jsonify(leer_de_csv())

# -----------------------------
# Probar conexión con la base de datos
# -----------------------------
@app.route('/test_db')
def test_db():
    try:
        conn = conexion()
        cur = conn.cursor()
        cur.execute("SELECT 1")
        result = cur.fetchone()
        cerrar_conexion(conn)
        return {"conexion": "exitosa", "resultado": result[0]}
    except Exception as e:
        return {"error": str(e)}

# ======================================================
if __name__ == '__main__':
    app.run(debug=True)
