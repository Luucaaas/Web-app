from flask import Blueprint, request, jsonify
from src.models.models import db, Client
from src.routes.clients import client_bp


@client_bp.route("/", methods=['POST'])
def create_client():
    data = request.get_json()
    if not data:
        return jsonify({"message": "Aucune donnée fournie"}), 400

    nom = data.get('nom')
    prenom = data.get('prenom')
    birthdate = data.get('birthdate')
    email = data.get('email')
    telephone = data.get('telephone')

    if not nom or not prenom or not birthdate:
        return jsonify({"message": "Les champs nom, prenom et birthdate sont obligatoires"}), 400

    new_client = Client(nom=nom, prenom=prenom, birthdate=birthdate, email=email, telephone=telephone)

    db.session.add(new_client)
    db.session.commit()

    return jsonify({"message": "Client créé avec succès"}), 201


@client_bp.route('/<int:id>', methods=['DELETE'])
def delete_client(id):
    client_to_delete = Client.query.get(id)
    if client_to_delete is None:
        return jsonify({"message": "Client non trouvé"}), 404

    db.session.delete(client_to_delete)
    db.session.commit()

    return jsonify({"message": "Client supprimé avec succès"}), 204