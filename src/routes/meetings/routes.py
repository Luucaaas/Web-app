from flask import Blueprint, request, jsonify
from src.models import db, Meeting, Client
from datetime import datetime, time

meeting_bp = Blueprint('meeting_bp', __name__)

@meeting_bp.route("/meetings", methods=["POST"])
def create_meeting():
    data = request.get_json()
    if not data:
        return jsonify({"message": "Aucune donnée fournie"}), 400

    date_str = data.get("date")
    heure_str = data.get("heure")
    cab = data.get("cab")

    if not date_str or not heure_str or not cab:
        return jsonify({"message": "Les champs date, heure et cab sont obligatoires"}), 400

    try:    
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"message": "Format de date invalide, utilisez YYYY-MM-DD"}), 400

    try:
        heure = datetime.strptime(heure_str, "%H:%M:%S").time()
    except ValueError:
        return jsonify({"message": "Format d'heure invalide, utilisez HH:MM:SS"}), 400

    new_meeting = Meeting(date=date, heure=heure, cab=cab)
    db.session.add(new_meeting)
    db.session.commit()

    return jsonify({"message": "Meeting créé avec succès"}), 201

@meeting_bp.route("/meetings", methods=["GET"])
def get_meetings():
    meetings = Meeting.query.all()
    meetings_data = [{"id": meeting.id, "date": meeting.date, "heure": str(meeting.heure), "cab": meeting.cab} for meeting in meetings]
    return jsonify(meetings_data)

@meeting_bp.route("/meetings/<int:meeting_id>", methods=["GET"])
def get_meeting(meeting_id):
    meeting = Meeting.query.get_or_404(meeting_id)
    meeting_data = {"id": meeting.id, "date": meeting.date, "heure": str(meeting.heure), "cab": meeting.cab}
    return jsonify(meeting_data)

@meeting_bp.route("/meetings/<int:id>", methods=["PUT"])
def update_meeting(id):
    meeting = Meeting.query.get(id)
    if meeting is None:
        return jsonify({"message": "Meeting non trouvé"}), 404

    data = request.get_json()
    if "date" in data:
        meeting.date = data["date"]
    if "heure" in data:
        meeting.heure = data["heure"]
    if "cab" in data:
        meeting.cab = data["cab"]

    db.session.commit()
    return jsonify({"message": "Meeting mis à jour avec succès"}), 200

@meeting_bp.route("/meetings/<int:id>", methods=["DELETE"])
def delete_meeting(id):
    meeting = Meeting.query.get(id)
    if meeting is None:
        return jsonify({"message": "Meeting non trouvé"}), 404

    db.session.delete(meeting)
    db.session.commit()
    return jsonify({"message": "Meeting supprimé avec succès"}), 204


@meeting_bp.route('/meetings/create_with_client', methods=['POST'])
def create_meeting_with_client():
    data = request.get_json()
    if not data:
        return jsonify({"message": "Aucune donnée fournie"}), 400

    # Récupération des informations du meeting
    date_str = data.get('date')
    heure_str = data.get('heure')
    cab = data.get('cab')
    
    # Informations du client
    nom = data.get('nom')
    prenom = data.get('prenom')

    # Vérification que les champs nécessaires sont présents
    if not date_str or not heure_str or not cab or not nom or not prenom:
        return jsonify({"message": "Les champs date, heure, cab, nom, et prenom sont obligatoires"}), 400
    
    try:    
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"message": "Format de date invalide, utilisez YYYY-MM-DD"}), 400

    try:
        heure = datetime.strptime(heure_str, "%H:%M:%S").time()
    except ValueError:
        return jsonify({"message": "Format d'heure invalide, utilisez HH:MM:SS"}), 400

    # Rechercher le client par nom et prénom
    client = Client.query.filter_by(nom=nom, prenom=prenom).first()
    if not client:
        return jsonify({"message": "Client non trouvé"}), 404

    # Création du meeting avec l'ID du client trouvé
    new_meeting = Meeting(date=date, heure=heure, cab=cab, id_client=client.id)
    db.session.add(new_meeting)
    db.session.commit()

    return jsonify({"message": "Meeting créé avec succès pour le client"}), 201
