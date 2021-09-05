from flask_mail import Message
from flask_app import mail
from flask import render_template, current_app as app


def send_email(subject, sender, recipient, html_body):
    msg = Message(subject, sender=sender, recipient=recipient)
    msg.html_body = html_body
    mail.send(msg)


def send_reset_password_email(user):
    token = user.get_reset_password_token()
    send_email(
        "[PassMan] Восстановление пароля",
        sender=app.config["ADMIN"][0],
        recipient=[user.email],
        html_body=render_template(
            "email_reset_password.html",
            user=user,
            token=token
        )
    )
