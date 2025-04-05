from flask_mail import Message, Mail

mail = Mail()

def send_password_email(email, password):
    msg = Message("Votre mot de passe",
                  sender="miniprojetdevops@gmail.com",
                  recipients=[email])
    msg.body = f"Voici votre mot de passe temporaire : {password}"
    mail.send(msg)
