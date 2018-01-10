from wtforms import SubmitField, TextField, TextAreaField, StringField, PasswordField
from wtforms.validators import Required
from flask_wtf import FlaskForm


class NewItemForm(FlaskForm):
    title = TextField('Något att göra?', validators=[Required()])
    description = TextAreaField('Beskriv saken!', validators=[Required()])
    submit = SubmitField('Lägg till')

class EditItemForm(FlaskForm):
    title = TextField('Något att göra?', validators=[Required()])
    description = TextAreaField('Beskriv saken!', validators=[Required()])
    submit = SubmitField('Ändra')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[Required()])
    password = PasswordField('Password', validators=[Required()])
