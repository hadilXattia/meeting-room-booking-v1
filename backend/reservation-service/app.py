from flask import Flask
from flask_jwt_extended import JWTManager
from models import db
from routes import reservation_routes
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Initialize the database and JWT manager
db.init_app(app)
jwt = JWTManager(app)

# Register the routes from routes.py
app.register_blueprint(reservation_routes)

if __name__ == '__main__':
    app.run(debug=True)
