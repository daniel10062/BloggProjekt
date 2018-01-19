from wtforms import SubmitField, TextField, TextAreaField, StringField, PasswordField
from wtforms.validators import DataRequired, Required, Email, EqualTo
from flask_wtf import FlaskForm
from .. models import User


class AddItemForm(FlaskForm):
    title = TextField('Titel...', validators=[Required()])
    description = TextAreaField('Att göra...', validators=[Required()])
    submit = SubmitField('Lägg till')


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
    submit = SubmitField('Login')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
