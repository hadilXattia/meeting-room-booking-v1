import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:Najet2013@localhost:5432/reservation_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'my-secret-key')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key')
