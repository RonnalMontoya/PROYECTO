from conexion.conexion import db

class Producto(db.Model):
    __tablename__ = "producto"   # Nombre de la tabla en MySQL

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<Producto {self.nombre}>"

from flask_login import UserMixin
from conexion.conexion import db

class Usuario(UserMixin, db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"<Usuario {self.username}>"
