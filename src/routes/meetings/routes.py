from flask import Blueprint, request, jsonify
from src.models.meeting import Meeting  
from src.models import db
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
    meetings_list = [{"id": m.id, "date": m.date, "heure": m.heure, "cab": m.cab} for m in meetings]
    return jsonify(meetings_list), 200

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
