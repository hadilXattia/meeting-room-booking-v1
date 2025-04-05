from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Reservation(db.Model):
    __tablename__ = 'reservations'

    id = db.Column(db.Integer, primary_key=True)
    salle_id = db.Column(db.Integer, db.ForeignKey('salles.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date_reservation = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(50), default='pending', nullable=False)  # pending, validé, refusé

    salle = db.relationship('Salle', back_populates='reservations')
    user = db.relationship('User', back_populates='reservations')