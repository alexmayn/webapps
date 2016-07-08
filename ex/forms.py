from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, EqualTo

# Login form
class LoginForm(Form):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


# Registraton form. It's not used
class RegistrationForm(LoginForm):
    password_repeat = PasswordField('Check your password', validators=[DataRequired(), EqualTo('password')])