from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class CommentForm(FlaskForm):
    text = TextAreaField('Comment', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Tak to řekni!')
    recaptcha = RecaptchaField()