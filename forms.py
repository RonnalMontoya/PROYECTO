from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DecimalField, SubmitField
from wtforms.validators import DataRequired, NumberRange

# ===============================
# Formulario Producto
# ===============================
class ProductoForm(FlaskForm):
    nombre = StringField("Nombre del producto", validators=[DataRequired()])
    cantidad = IntegerField("Cantidad", validators=[DataRequired(), NumberRange(min=1, message="Debe ser mayor a 0")])
    precio = DecimalField("Precio", validators=[DataRequired(), NumberRange(min=0, message="Debe ser mayor o igual a 0")])
    
    submit = SubmitField("Guardar")
