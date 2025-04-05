from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Salle
from flask import current_app as app

routes = Blueprint('routes', __name__)

# Route to get list of all salles
@routes.route('/salles', methods=['GET'])
def get_salles():
    salles = Salle.query.all()
    return jsonify([{'id': salle.id, 'nom': salle.nom, 'numero': salle.numero, 
                     'etage': salle.etage, 'status': salle.status, 'taille': salle.taille} 
                    for salle in salles])

# Route to create a salle (Admin only)
@routes.route('/salle', methods=['POST'])
@jwt_required()
def create_salle():
    # a verifier le admin token function here 
    current_user = get_jwt_identity()
    
    # Only admin can create
    if current_user['role'] != 'admin':
        return jsonify({"message": "Unauthorized"}), 403

    data = request.get_json()
     
     # Check if the necessary fields are present in the request body
    if not all(field in data for field in ['nom', 'numero', 'etage', 'status', 'taille']):
        return jsonify({'message': 'Missing required fields'}), 400
    new_salle = Salle(
        nom=data['nom'],
        numero=data['numero'],
        etage=data['etage'],
        status=data['status'],
        taille=data['taille']
    )

    db.session.add(new_salle)
    db.session.commit()
    return jsonify({"message": "Salle created successfully!"}), 201

# Route to update a salle (Admin only)
@routes.route('/salle/<int:id>', methods=['PUT'])
@jwt_required()
def update_salle(id):
    current_user = get_jwt_identity()

    if current_user['role'] != 'admin':
        return jsonify({"message": "Unauthorized"}), 403

    salle = Salle.query.get(id)
    if not salle:
        return jsonify({"message": "Salle not found!"}), 404

    data = request.get_json()
    salle.nom = data.get('nom', salle.nom)
    salle.numero = data.get('numero', salle.numero)
    salle.etage = data.get('etage', salle.etage)
    salle.status = data.get('status', salle.status)
    salle.taille = data.get('taille', salle.taille)

    db.session.commit()
    return jsonify({"message": "Salle updated successfully!"})

# Route to delete a salle (Admin only)
@routes.route('/salle/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_salle(id):
    current_user = get_jwt_identity()

    if current_user['role'] != 'admin':
        return jsonify({"message": "Unauthorized"}), 403

    salle = Salle.query.get(id)
    if not salle:
        return jsonify({"message": "Salle not found!"}), 404

    db.session.delete(salle)
    db.session.commit()
    return jsonify({"message": "Salle deleted successfully!"})
