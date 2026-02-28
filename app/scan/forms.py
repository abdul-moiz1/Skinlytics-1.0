from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import SubmitField


class UploadForm(FlaskForm):
    image = FileField('Skin Image', validators=[
        FileRequired('Please select an image.'),
        FileAllowed(['jpg', 'jpeg', 'png'], 'Only JPG and PNG images are allowed.')
    ])
    submit = SubmitField('Start Analyzing')
