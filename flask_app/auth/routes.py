from flask import render_template, url_for, flash, redirect, Blueprint, request
from flask_app.models import User
from flask_app.auth.forms import LoginForm, RegistrationForm, ResetPasswordForm
from flask_login import login_user, logout_user, current_user, login_required
from flask_app import db, bcrypt
auth = Blueprint("auth", __name__)


@auth.route('/sign in', methods=['GET', 'POST'])
def sign_in():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not bcrypt.check_password_hash(user.password, form.password.data):
            flash("Неправильное имя пользователя и/или пароль!")
            return redirect(url_for("auth.sign_in"))
        login_user(user)
        next_page = request.args.get('next')
        return redirect(next_page) if next_page else redirect(url_for("main.index"))
    return render_template('login.html', form=form, title="Авторизация")


@auth.route('/sign up', methods=['GET', 'POST'])
def sign_up():
    form = RegistrationForm()
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    if form.validate_on_submit():
        u_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data, password=u_password)
        db.session.add(user)
        db.session.commit()
        flash("Приветствуем нового пользователя!", "success")
        return redirect(url_for("auth.sign_in"))
    return render_template('register.html', form=form, title='Авторизация')


@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.index"))


@auth.route("/reset_password", methods=['GET', 'POST'])
def reset_password():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        pass
    return render_template('reset_password.html', form=form)
