from flask import Flask
from flask_jwt_extended import JWTManager
from models import db
from config import Config
from routes import routes

app = Flask(__name__)
app.config.from_object(Config)

# Initialize Flask extensions
db.init_app(app)
jwt = JWTManager(app)

# Register the routes blueprint
app.register_blueprint(routes)

# Create the tables if they don't exist
with app.app_context():
    db.create_all()

if __name__ == '__main__':
      app.run(debug=True, host='0.0.0.0', port=5001)
