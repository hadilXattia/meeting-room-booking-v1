from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Salle(db.Model):
    __tablename__ = 'salles'

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    numero = db.Column(db.String(50), nullable=False)
    etage = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False)  # 'occupe' or 'disponible'
    taille = db.Column(db.Integer, nullable=False)  # Number of seats

    def __repr__(self):
        return f'<Salle {self.nom}, {self.numero}>'
