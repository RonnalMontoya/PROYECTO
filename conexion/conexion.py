from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# ===============================
# Configuración de la aplicación
# ===============================
app = Flask(__name__)
app.config['SECRET_KEY'] = 'inventario123'

# 🔹 Conexión a MySQL (ajusta user/password/base según tu phpMyAdmin)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:@localhost/proyecto"
# Si tu usuario tiene contraseña, por ejemplo "1234", sería:
# "mysql+pymysql://root:1234@localhost/proyecto"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar SQLAlchemy
db = SQLAlchemy(app)
