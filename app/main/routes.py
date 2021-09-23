from flask import render_template, request, Blueprint, flash, redirect, url_for
from app.main.forms import (AddPasswordForm, GetPasswordForm,
                                  ChangeMasterPasswordForm, ChangePasswordForm,
                                  ChangeEmailForm)
from app.models import Password, User
from flask_login import login_required, current_user
from app import bcrypt, db
main = Blueprint('main', __name__)


@main.route('/', methods=['GET', "POST"])
@login_required
def index():
    add_password_form = AddPasswordForm()
    get_password_form = GetPasswordForm()
    change_password_form = ChangePasswordForm()
    # добавить пароль
    if add_password_form.validate_on_submit():
        password = Password.query.filter_by(
            password_name=add_password_form.password_name.data).first()
        if password:
            flash("Такая запись уже существует!")
            return redirect(url_for('main.index'))
        else:
            password = Password(
                password_name=add_password_form.password_name.data, password_content=add_password_form.password.data, creator=current_user.id)
            db.session.add(password)
            db.session.commit()
            flash("Пароль успешно добавлен!")
            return redirect(url_for('main.index'))
    # получить пароль
    if get_password_form.validate_on_submit():
        password = Password.query.filter_by(
            password_name=get_password_form.password_name.data).first()
        if password is None or not bcrypt.check_password_hash(current_user.password, get_password_form.master_password.data):
            flash("Неправильное имя пароля и/или мастер-пароль!")
            return redirect(url_for('main.index'))
        flash(
            f"Пароль от {add_password_form.password_name.data} - {password.password_content}")
    # изменить пароль
    if change_password_form.validate_on_submit():
        password = Password.query.filter_by(
            password_name=change_password_form.password_name.data).first()
        if password is None or not bcrypt.check_password_hash(
            current_user.password, get_password_form.master_password.data
        ) or change_password_form.old_password.data != password.password_content:
            flash("Проверьте введенные данные!")
            return redirect(url_for('main.index'))
        password.change_password(change_password_form.new_password.data)
        db.session.commit()
        flash("Пароль обновлен!")
        return redirect(url_for('main.index'))
    return render_template('main/index.html',
                           title='Главная',
                           add_password_form=add_password_form,
                           get_password_form=get_password_form,
                           change_password_form=change_password_form
                           )


@main.route('/profile')
@login_required
def profile():
    return render_template('profile/profile.html', user=current_user, title="Профиль")


@main.route('/change_master_password', methods=['GET', 'POST'])
@login_required
def change_master_password():
    form = ChangeMasterPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=current_user.username).first()
        if bcrypt.check_password_hash(user.password, form.current_password.data) and form.current_password.data != form.new_password.data:
            user.password = bcrypt.generate_password_hash(
                form.new_password.data).decode('utf-8')
            db.session.commit()
            flash('Пароль успешно сменен!', "success")
            return redirect(url_for('main.index'))
        else:
            flash('Мастер-пароль введен неверно и/или пароли совпадают')
            return redirect(url_for('main.change_master_password'))
    return render_template('profile/change_master_password.html', form=form, title="Смена пароля")


@main.route("/change_email", methods=["GET", "POST"])
@login_required
def change_email():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        current_user.change_email(form.new_email.data)
        db.session.commit()
        flash("Почта успешно сменена!")
        return redirect(url_for('main.profile'))
    return render_template('profile/change_email.html', form=form, title="Смена почты")
