from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    poste = db.Column(db.String(100), nullable=True)
    telephone = db.Column(db.String(20), nullable=True)

    def __init__(self, email, nom, prenom, password, role, poste, telephone):
        self.email = email
        self.nom = nom
        self.prenom = prenom
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
        self.role = role
        self.poste = poste
        self.telephone = telephone
