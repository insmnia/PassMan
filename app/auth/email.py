from flask_mail import Message
from app import mail
from flask import render_template, current_app as app


def send_email(subject, sender, recipient, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipient)
    msg.html_body = html_body
    msg.body = text_body
    mail.send(msg)


def reset_email(user):
    token = user.get_reset_password_token()
    send_email(
        subject="[PassMan] Восстановление пароля",
        sender=app.config["ADMIN"][0],
        recipient=[user.email],
        text_body=render_template(
            "email/reset_password.txt", user=user, token=token),
        html_body=render_template(
            "email/email_reset_password.html", user=user, token=token)
    )
