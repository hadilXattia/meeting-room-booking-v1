from flask import Blueprint, request, jsonify
from models import db, User
from utils import send_password_email
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import random
import string
import bcrypt

routes = Blueprint('routes', __name__)

def generate_password():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))

@routes.route('/register', methods=['POST'])
@jwt_required()
def register():
    current_user_email = get_jwt_identity()
    current_user = User.query.filter_by(email=current_user_email).first()
    if current_user.role != 'admin':
        return jsonify({"msg": "Accès interdit"}), 403

    data = request.json
    password = generate_password()
    user = User(email=data['email'], nom=data['nom'], prenom=data['prenom'],
                password=password, role=data['role'], poste=data['poste'],
                telephone=data['telephone'])
    db.session.add(user)
    db.session.commit()
    send_password_email(data['email'], password)
    return jsonify({"msg": "Utilisateur créé et mot de passe envoyé"}), 201

@routes.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()
    if user and bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
        token = create_access_token(identity=user.email)
        return jsonify({"token": token}), 200
    return jsonify({"msg": "Identifiants invalides"}), 401

@routes.route('/profil', methods=['PUT'])
@jwt_required()
def update_my_profile():
    email = get_jwt_identity()
    user = User.query.filter_by(email=email).first()
    data = request.json
    user.nom = data.get('nom', user.nom)
    user.prenom = data.get('prenom', user.prenom)
    user.password = bcrypt.generate_password_hash(data['password']).decode('utf-8') if 'password' in data else user.password
    user.poste = data.get('poste', user.poste)
    user.telephone = data.get('telephone', user.telephone)
    db.session.commit()
    return jsonify({"msg": "Coordonnées mises à jour"}), 200

@routes.route('/users', methods=['GET'])
@jwt_required()
def list_users():
    current_user_email = get_jwt_identity()
    current_user = User.query.filter_by(email=current_user_email).first()
    if current_user.role != 'admin':
        return jsonify({"msg": "Accès interdit"}), 403

    users = User.query.all()
    return jsonify([{
        "email": u.email,
        "nom": u.nom,
        "prenom": u.prenom,
        "role": u.role,
        "poste": u.poste,
        "telephone": u.telephone
    } for u in users])

@routes.route('/user/<int:id>', methods=['DELETE', 'PUT'])
@jwt_required()
def manage_user(id):
    current_user_email = get_jwt_identity()
    current_user = User.query.filter_by(email=current_user_email).first()
    if current_user.role != 'admin':
        return jsonify({"msg": "Accès interdit"}), 403

    user = User.query.get_or_404(id)
    if request.method == 'DELETE':
        db.session.delete(user)
        db.session.commit()
        return jsonify({"msg": "Utilisateur supprimé"}), 200

    if request.method == 'PUT':
        data = request.json
        user.nom = data.get('nom', user.nom)
        user.prenom = data.get('prenom', user.prenom)
        user.password = bcrypt.generate_password_hash(data['password']).decode('utf-8') if 'password' in data else user.password
        user.role = data.get('role', user.role)
        user.poste = data.get('poste', user.poste)
        user.telephone = data.get('telephone', user.telephone)
        db.session.commit()
        return jsonify({"msg": "Utilisateur modifié"}), 200

# New endpoint to create and manage admins
@routes.route('/admin', methods=['POST', 'GET'])
@jwt_required()
def manage_admin():
    current_user_email = get_jwt_identity()
    current_user = User.query.filter_by(email=current_user_email).first()
    
    # Ensure that only admins can access this route
    if current_user.role != 'admin':
        return jsonify({"msg": "Accès interdit"}), 403

    if request.method == 'POST':  # Create a new admin
        data = request.json
        password = generate_password()
        admin = User(email=data['email'], nom=data['nom'], prenom=data['prenom'],
                     password=password, role='admin', poste=data['poste'],
                     telephone=data['telephone'])
        db.session.add(admin)
        db.session.commit()
        send_password_email(data['email'], password)
        return jsonify({"msg": "Admin créé et mot de passe envoyé"}), 201

    if request.method == 'GET':  # List all admins
        admins = User.query.filter_by(role='admin').all()
        return jsonify([{
            "email": u.email,
            "nom": u.nom,
            "prenom": u.prenom,
            "role": u.role,
            "poste": u.poste,
            "telephone": u.telephone
        } for u in admins])
