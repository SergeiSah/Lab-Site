from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectMultipleField, FloatField


class OptConstForm(FlaskForm):
    materials = SelectMultipleField('Материалы')
    energy = FloatField('Энергия (эВ)', default=100)
    density = FloatField('Плотность (г/cм3)')
    submit = SubmitField('Рассчитать')