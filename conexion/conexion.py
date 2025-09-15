from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# ===============================
# Configuración de la aplicación
# ===============================
app = Flask(__name__)
app.config['SECRET_KEY'] = 'inventario123'

# Conexión a MySQL (ajusta user/pass según phpMyAdmin)
# Si tu usuario tiene contraseña (ej. "1234"), sería:
# "mysql+pymysql://root:1234@localhost/proyecto"
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:@localhost/proyecto"

# Evitar warnings innecesarios
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Depuración (mostrar errores claros)
app.config['DEBUG'] = True
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['TRAP_HTTP_EXCEPTIONS'] = True
app.config['TRAP_BAD_REQUEST_ERRORS'] = True

# Inicializar SQLAlchemy
db = SQLAlchemy(app)
