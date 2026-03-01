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


class SkinTypeForm(FlaskForm):
    name = StringField('Skin Type Name', validators=[DataRequired(), Length(max=50)])
    description = TextAreaField('Description')
    submit = SubmitField('Save Skin Type')


class IngredientForm(FlaskForm):
    name = StringField('Ingredient Name', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description')
    skin_type_id = SelectField('Skin Type', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Save Ingredient')
