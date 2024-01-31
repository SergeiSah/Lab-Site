from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectMultipleField, FloatField
from wtforms.validators import DataRequired, NumberRange


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Войти')


class OptConstForm(FlaskForm):
    materials = SelectMultipleField('Материалы')
    energy = FloatField('Энергия (эВ)', default=112)
    submit = SubmitField('Рассчитать')
