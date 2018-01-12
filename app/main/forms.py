from wtforms import SubmitField, TextField, TextAreaField
from wtforms.validators import Required
from flask_wtf import FlaskForm


class AddItemForm(FlaskForm):
    title = TextField('Titel...', validators=[Required()])
    description = TextAreaField('Att göra...', validators=[Required()])
    submit = SubmitField('Lägg till')
