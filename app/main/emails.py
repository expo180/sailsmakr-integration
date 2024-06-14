# emails.py

from flask_mail import Message
from flask_babelex import gettext as _
from ... import mail


def send_reseller_email(email, password):
    subject = _("Welcome to the Reseller Portal")
    body = _("""
    Bonjour,

    Félicitations ! Vous avez été approuvé en tant que revendeur. Veuillez trouver ci-dessous vos identifiants de connexion :

    Email: {email}
    Mot de passe: {password}

    Veuillez copier votre mot de passe quelque part en sécurité. Vous en aurez besoin pour vous connecter à votre portail de revendeur.

    Cordialement,
    Votre nom de l'entreprise
    """).format(email=email, password=password)

    msg = Message(subject, recipients=[email], body=body)
    try:
        mail.send(msg)
        print(f"Email sent successfully to {email}")
    except Exception as e:
        print(f"Failed to send email to {email}: {str(e)}")
