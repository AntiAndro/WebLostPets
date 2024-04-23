from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class AddsForm(FlaskForm):
    type_cat = BooleanField('Кошка')
    type_dog = BooleanField('Собака')
    type_other = BooleanField('Другое')
    gender_male = BooleanField('Мужской')
    gender_female = BooleanField('Женский')
    place = StringField('Место:')
    time = StringField('Дата:')
    description = TextAreaField("Описание:")
    name = StringField('Ваше имя:')
    number = StringField('Ваш номер телефона:')
    submit = SubmitField('Применить')
