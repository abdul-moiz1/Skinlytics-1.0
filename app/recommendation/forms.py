from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length


class ProductForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired(), Length(max=150)])
    description = TextAreaField('Description')
    skin_type_id = SelectField('Skin Type', coerce=int, validators=[DataRequired()])
    image = FileField('Product Image', validators=[
        FileAllowed(['jpg', 'jpeg', 'png'], 'Only JPG and PNG images are allowed.')
    ])
    submit = SubmitField('Save Product')
