# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo


# ------------------------------
# Formulario para productos
# ------------------------------
class ProductoForm(FlaskForm):
    nombre = StringField("Nombre", validators=[DataRequired(), Length(min=2, max=100)])
    cantidad = IntegerField("Cantidad", validators=[DataRequired()])
    precio = FloatField("Precio", validators=[DataRequired()])
    submit = SubmitField("Guardar")


# ------------------------------
# Formulario de login
# ------------------------------
class LoginForm(FlaskForm):
    username = StringField("Usuario", validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField("Contraseña", validators=[DataRequired()])
    submit = SubmitField("Iniciar Sesión")


# ------------------------------
# Formulario de registro
# ------------------------------
class RegisterForm(FlaskForm):
    username = StringField("Usuario", validators=[DataRequired(), Length(min=3, max=50)])
    email = StringField("Correo", validators=[DataRequired(), Email()])
    password = PasswordField("Contraseña", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField("Confirmar Contraseña", 
                                     validators=[DataRequired(), EqualTo("password", message="Las contraseñas deben coincidir")])
    submit = SubmitField("Registrarse")
