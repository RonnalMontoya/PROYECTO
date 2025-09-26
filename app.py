# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from conexion.conexion import db   # ✅ solo importamos db
from forms import ProductoForm, LoginForm, RegisterForm
from models import Usuario, Producto
from datetime import datetime
import os, csv, json

# ======================================================
# Inicializar Flask
# ======================================================
app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost/proyecto'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar extensiones
db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"  # redirige si no estás logueado

# ======================================================
# Flask-Login: Cargar usuario
# ======================================================
@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# ======================================================
# Inyectar fecha en templates
# ======================================================
@app.context_processor
def inject_now():
    return {'now': datetime.utcnow}

# ======================================================
# Persistencia en archivos
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
# Rutas de Autenticación
# ======================================================
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Aquí va la lógica para autenticar usuario
        flash("Inicio de sesión exitoso.", "success")
        return redirect(url_for('index'))
    return render_template('auth/login.html', title="Iniciar Sesión", form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # Aquí va la lógica para guardar usuario en la BD
        flash("Usuario registrado correctamente.", "success")
        return redirect(url_for('login'))
    return render_template('auth/register.html', title="Registro", form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Has cerrado sesión", "info")
    return redirect(url_for('index'))

# ======================================================
# Rutas de Productos
# ======================================================
@app.route('/productos')
@login_required
def listar_productos():
    q = request.args.get('q', '').strip()
    if q:
        productos = Producto.query.filter(Producto.nombre.like(f"%{q}%")).all()
    else:
        productos = Producto.query.all()
    return render_template('products/list.html', title='Productos', productos=productos, q=q)

@app.route('/productos/nuevo', methods=['GET', 'POST'])
@login_required
def crear_producto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        cantidad = int(request.form['cantidad'])
        precio = float(request.form['precio'])

        nuevo = Producto(nombre=nombre, cantidad=cantidad, precio=precio)
        db.session.add(nuevo)
        db.session.commit()

        guardar_en_txt({"nombre": nombre, "cantidad": cantidad, "precio": precio})
        guardar_en_json({"nombre": nombre, "cantidad": cantidad, "precio": precio})
        guardar_en_csv({"nombre": nombre, "cantidad": cantidad, "precio": precio})

        flash("Producto agregado correctamente.", "success")
        return redirect(url_for('listar_productos'))

    return render_template('products/form.html', title='Nuevo producto', modo='crear')

@app.route('/productos/<int:pid>/editar', methods=['GET', 'POST'])
@login_required
def editar_producto(pid):
    prod = Producto.query.get(pid)
    if not prod:
        return "Producto no encontrado", 404

    if request.method == 'POST':
        prod.nombre = request.form['nombre']
        prod.cantidad = int(request.form['cantidad'])
        prod.precio = float(request.form['precio'])
        db.session.commit()
        flash("Producto actualizado correctamente.", "success")
        return redirect(url_for('listar_productos'))

    return render_template('products/form.html', title="Editar producto", modo="editar", pid=pid, form=prod)

@app.route('/productos/<int:pid>/eliminar', methods=['POST'])
@login_required
def eliminar_producto(pid):
    prod = Producto.query.get(pid)
    if prod:
        db.session.delete(prod)
        db.session.commit()
        flash("Producto eliminado correctamente.", "success")
    else:
        flash("Producto no encontrado.", "warning")
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

# ======================================================
# Probar conexión con la base de datos
# ======================================================
@app.route('/test_db')
def test_db():
    try:
        result = db.session.execute("SELECT 1").scalar()
        return {"conexion": "exitosa", "resultado": result}
    except Exception as e:
        return {"error": str(e)}

# ======================================================
# Inicializar BD
# ======================================================
with app.app_context():
    db.create_all()

# ======================================================
if __name__ == '__main__':
    app.run(debug=True)
