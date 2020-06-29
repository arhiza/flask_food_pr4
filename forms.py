from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError

from app import db
from models import User


class OrderForm(FlaskForm):
    name = StringField("Ваше имя", [DataRequired()])
    mail = StringField("Электропочта", [DataRequired(), Email(message="Не похоже на почту")])
    phone = StringField("Телефон", [DataRequired()])
    address = StringField("Адрес", [DataRequired()])


def unique_mail_check(form, field):
    if db.session.query(User).filter_by(mail=field.data).first():
        raise ValidationError('Пользователь с таким емейлом уже существует')

    
class LoginForm(FlaskForm):
    mail = StringField("Электропочта", [DataRequired()])
    password = PasswordField("Пароль", [DataRequired()])

    
class RegistrationForm(FlaskForm):
    mail = StringField("Электропочта", [DataRequired(), Email(message="Не похоже на почту"), unique_mail_check])
    password = PasswordField("Пароль", [DataRequired(), Length(min=5, message="Слишком короткий пароль")])

