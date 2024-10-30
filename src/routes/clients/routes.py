from flask import Blueprint, request, jsonify
from src.models import db, Client
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
    doc = data.get('doc')

    if not nom or not prenom or not birthdate:
        return jsonify({"message": "Les champs nom, prenom et birthdate sont obligatoires"}), 400

    new_client = Client(nom=nom, prenom=prenom, birthdate=birthdate, email=email, telephone=telephone, doc=doc)

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

@client_bp.route('/<int:id>', methods=['PUT'])
def update_client(id):
    data = request.get_json()
    if not data:
        return jsonify({"message": "Aucune donnée fournie"}), 400

    client_to_update = Client.query.get(id)
    if client_to_update is None:
        return jsonify({"message": "Client non trouvé"}), 404

    nom = data.get('nom')
    prenom = data.get('prenom')
    birthdate = data.get('birthdate')
    email = data.get('email')
    telephone = data.get('telephone')
    doc = data.get('doc')


    if nom:
        client_to_update.nom = nom
    if prenom:
        client_to_update.prenom = prenom
    if birthdate:
        client_to_update.birthdate = birthdate
    if email:
        client_to_update.email = email
    if telephone:
        client_to_update.telephone = telephone
    if doc:
        client_to_update.doc = doc

    db.session.commit()

    return jsonify({"message": "Client mis à jour avec succès"}), 200
