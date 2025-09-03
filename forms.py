from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DecimalField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class ProductoForm(FlaskForm):
    id_producto = IntegerField("ID del Producto", validators=[DataRequired()])
    nombre = StringField("Nombre", validators=[DataRequired()])
    cantidad = IntegerField("Cantidad", validators=[DataRequired(), NumberRange(min=0)])
    precio = DecimalField("Precio", validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField("Guardar")
