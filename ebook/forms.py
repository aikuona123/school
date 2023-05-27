from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, EmailField
from wtforms.validators import InputRequired, Email, EqualTo
from wtforms.widgets import TextArea
from .models import User


class LoginForm(FlaskForm):
    username = StringField("Логин", validators=[InputRequired("Введите логин")])
    password = PasswordField("Пароль", validators=[InputRequired("Введите пароль")])


class SignupForm(FlaskForm):
	fio = StringField("Логин", validators=[InputRequired("Введите ФИО")])
	username = StringField("Логин", validators=[InputRequired("Введите логин")])
	password = PasswordField("Пароль", validators=[InputRequired("Введите пароль")])
	confirmation = PasswordField("Повторите пароль", validators=[InputRequired("Введите подтаверждение"), EqualTo('password', 'Пароли не совпадают!')])
	email = EmailField("Email", validators=[InputRequired("Введите e-mail"), Email("Неправильный e-mail")])

	