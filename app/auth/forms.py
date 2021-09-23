from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Length, EqualTo, Email
from app.models import User


class RegistrationForm(FlaskForm):
    username = StringField("Имя пользователя", validators=[
                           DataRequired(), Length(min=2, max=20, message="Длина имени от 2 до 20 символов")])
    email = StringField("Почта", validators=[DataRequired(), Email()])
    password = PasswordField("Пароль", validators=[
                             DataRequired()])
    confirm_password = PasswordField("Подтвердите пароль", validators=[
                                     DataRequired(), EqualTo("password", message="Пароли должны совпадать")])
    submit = SubmitField("Создать аккаунт")

    def validate_username(self, username):
        excluded_chars = " *?!'^+%&amp;/()=}][{$#"
        for char in username.data:
            if char in excluded_chars:
                raise ValidationError(
                    f"Символ {char} нельзя использовать в имени пользователя!")

        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                "Пользователь с таким именем уже существует!")

    def validate_password(self, password):
        if len(password.data) < 7:
            raise ValidationError("Длина пароля должна быть от 8 символов")
        import re
        p = r"^(?=.*[A-Z])(?=.*[0-9])(?=.*[a-z]).{8,}$"
        if not re.match(p, password.data):
            raise ValidationError(
                "Пароль должен состоять из строчных, прописных букв и цифр")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                "Пользователь с такой почтой уже существует!")


class LoginForm(FlaskForm):
    username = StringField(
        "Имя пользователя", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    submit = SubmitField("Войти")


class SendResetPasswordForm(FlaskForm):
    email = StringField("Почта", validators=[DataRequired(), Email()])
    submit = SubmitField("Отправить письмо")


class ResetPasswordForm(FlaskForm):
    new_password = PasswordField("Новый пароль", validators=[DataRequired()])
    submit = SubmitField("Обновить пароль")
