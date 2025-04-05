from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from models import db, Reservation, Salle
from kafka import KafkaProducer
import json

# Kafka producer for inter-service communication
producer = KafkaProducer(bootstrap_servers='localhost:9092', 
                          value_serializer=lambda v: json.dumps(v).encode('utf-8'))

# Create a Flask Blueprint for reservation routes
reservation_routes = Blueprint('reservation_routes', __name__)

# Route to create a reservation
@reservation_routes.route('/reservation', methods=['POST'])
@jwt_required()
def create_reservation():
    current_user = get_jwt_identity()

    # Get reservation data
    data = request.get_json()
    if 'salle_id' not in data or 'date_reservation' not in data:
        return jsonify({"message": "Salle ID and date are required."}), 400

    salle = Salle.query.get(data['salle_id'])
    if not salle:
        return jsonify({"message": "Salle not found."}), 404

    # Check if salle is already occupied
    if salle.status == 'occupe':
        return jsonify({"message": "Salle is already reserved."}), 400

    # Create reservation
    reservation = Reservation(
        salle_id=data['salle_id'],
        user_id=current_user['id'],
        date_reservation=datetime.strptime(data['date_reservation'], '%Y-%m-%d %H:%M:%S')
    )

    db.session.add(reservation)
    salle.status = 'occupe'  # Mark salle as occupied
    db.session.commit()

    # Send Kafka message to salle-service for status update
    producer.send('salle-topic', {'salle_id': salle.id, 'status': 'occupe'})

    return jsonify({"message": "Reservation created successfully!"}), 201


# Route to cancel a reservation
@reservation_routes.route('/reservation/<int:id>', methods=['DELETE'])
@jwt_required()
def cancel_reservation(id):
    reservation = Reservation.query.get(id)

    if not reservation:
        return jsonify({"message": "Reservation not found."}), 404

    if reservation.user_id != get_jwt_identity()['id']:
        return jsonify({"message": "Unauthorized to cancel this reservation."}), 403

    salle = Salle.query.get(reservation.salle_id)
    salle.status = 'disponible'  # Mark salle as available again
    db.session.delete(reservation)
    db.session.commit()

    # Send Kafka message to salle-service for status update
    producer.send('salle-topic', {'salle_id': salle.id, 'status': 'disponible'})

    return jsonify({"message": "Reservation cancelled successfully."}), 200


# Route to validate or refuse reservation (Admin only)
@reservation_routes.route('/reservation/<int:id>/validate', methods=['PUT'])
@jwt_required()
def validate_reservation(id):
    current_user = get_jwt_identity()

    if current_user['role'] != 'admin':
        return jsonify({"message": "Unauthorized"}), 403

    reservation = Reservation.query.get(id)
    if not reservation:
        return jsonify({"message": "Reservation not found."}), 404

    data = request.get_json()
    if 'status' not in data or data['status'] not in ['validé', 'refusé']:
        return jsonify({"message": "Invalid status."}), 400

    reservation.status = data['status']
    db.session.commit()

    return jsonify({"message": f"Reservation {data['status']}."}), 200
