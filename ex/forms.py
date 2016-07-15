from flask_wtf import Form
from wtforms import StringField, PasswordField, TextAreaField,  BooleanField
from wtforms.validators import DataRequired, EqualTo, Length, Required
from ex import app


# Login form
class LoginForm(Form):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

# Registraton form. It's not used
class RegistrationForm(LoginForm):
    password_repeat = PasswordField('Check your password', validators=[DataRequired(), EqualTo('password')])

#ser, only=('address', 'firstname', 'secondname', 'email'))
class EditForm(Form):
    oldpassword = StringField('Old Password')
    newpassword1 = StringField('New Password')
    newpassword2 = StringField('Retype New Password')
    isadmin = BooleanField('Is admin')
    address = StringField('Address')
    firstname = StringField('First Name')
    secondname = StringField('Second Name')
    email = StringField('e-mail', validators=[DataRequired()])
    about = TextAreaField('About me', validators = [Length(min = 0, max = 140)])

class EditFormAdmin(Form):
    login = StringField('Login', validators=[DataRequired()])
    newpassword1 = StringField('Password')
    newpassword2 = StringField('Retype Password')
    isadmin = BooleanField('Is admin')
    address = StringField('Address')
    firstname = StringField('First Name')
    secondname = StringField('Second Name')
    email = StringField('e-mail', validators=[DataRequired()])
    about = TextAreaField('About me', validators = [Length(min = 0, max = 140)])


