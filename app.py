# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
from conexion.conexion import conexion, cerrar_conexion
from forms import ProductoForm
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

@app.context_processor
def inject_now():
    return {'now': datetime.utcnow}

# -----------------------------
# Página principal
# -----------------------------
@app.route('/')
def index():
    return render_template('index.html', title='Inicio')

# -----------------------------
# Listar productos
# -----------------------------
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

# -----------------------------
# Crear producto
# -----------------------------
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
            flash("Producto agregado correctamente.", "success")
            return redirect(url_for('listar_productos'))
        except Exception as e:
            conn.rollback()
            flash(f"Error al guardar: {e}", "danger")
        finally:
            cerrar_conexion(conn)
    return render_template('products/form.html', title='Nuevo producto', form=form, modo='crear')

# -----------------------------
# Editar producto
# -----------------------------
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

# -----------------------------
# Eliminar producto
# -----------------------------
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

# -----------------------------
if __name__ == '__main__':
    app.run(debug=True)
