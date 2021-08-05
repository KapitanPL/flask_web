from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.fields.simple import PasswordField
from flask_wtf.file import FileField, FileRequired
from wtforms.validators import DataRequired

class CommentForm(FlaskForm):
    text = TextAreaField('Comment', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Tak to řekni!')
    recaptcha = RecaptchaField()

class LoginForm(FlaskForm):
    password = PasswordField('Heslo', validators=[DataRequired()])
    submit = SubmitField('Jdeme na to...')

class NewPostForm(FlaskForm):
    name = StringField('Title',validators=[DataRequired()])
    tags = StringField('Tags',validators=[DataRequired()])
    abstract = TextAreaField('Abstract',validators=[DataRequired()])
    file = FileField(validators=[FileRequired()])
    submit = SubmitField('Odpal to...')
