from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange


class QuizQuestionForm(FlaskForm):
    question_text = TextAreaField('Question', validators=[DataRequired()])
    option_a = StringField('Option A', validators=[DataRequired(), Length(max=200)])
    option_b = StringField('Option B', validators=[DataRequired(), Length(max=200)])
    option_c = StringField('Option C', validators=[DataRequired(), Length(max=200)])
    correct_answer = SelectField('Correct Answer', choices=[('a', 'A'), ('b', 'B'), ('c', 'C')], validators=[DataRequired()])
    order = IntegerField('Order', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Save Question')
