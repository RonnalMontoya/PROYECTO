from flask import Flask, render_template, redirect, url_for, request
from forms import ProductoForm
from models import Producto, Inventario

app = Flask(__name__)
app.config['SECRET_KEY'] = 'inventario123'

# Instancia del inventario (maneja la conexión con SQLite)
inventario = Inventario()

# Página principal
@app.route('/')
def index():
    return render_template("index.html")

# Listar productos
@app.route('/products')
def listar_productos():
    productos = inventario.obtener_productos()
    return render_template("products/list.html", productos=productos)

# Añadir producto
@app.route('/products/add', methods=["GET", "POST"])
def agregar_producto():
    form = ProductoForm()
    if form.validate_on_submit():
        producto = Producto(
            form.id_producto.data,
            form.nombre.data,
            form.cantidad.data,
            form.precio.data
        )
        inventario.añadir_producto(producto)
        return redirect(url_for('listar_productos'))
    return render_template("products/form.html", form=form)

# Eliminar producto
@app.route('/products/delete/<int:id>')
def eliminar_producto(id):
    inventario.eliminar_producto(id)
    return redirect(url_for('listar_productos'))

# Editar producto
@app.route('/products/edit/<int:id>', methods=["GET", "POST"])
def editar_producto(id):
    form = ProductoForm()
    producto = inventario.obtener_producto_por_id(id)

    if request.method == "GET" and producto:
        form.id_producto.data = producto.id_producto
        form.nombre.data = producto.nombre
        form.cantidad.data = producto.cantidad
        form.precio.data = producto.precio

    if form.validate_on_submit():
        inventario.actualizar_producto(
            form.id_producto.data,
            form.nombre.data,
            form.cantidad.data,
            form.precio.data
        )
        return redirect(url_for('listar_productos'))

    return render_template("products/form.html", form=form)

if __name__ == "__main__":
    app.run(debug=True)
