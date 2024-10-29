from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

app = Flask(__name__)

# Configuration de la base de données
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clients.db'  # Utilise SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Clé secrète pour JWT
app.config['JWT_SECRET_KEY'] = 'ma_cle_secrete'

# Initialisation des extensions
db = SQLAlchemy(app)
jwt = JWTManager(app)

# Définition du modèle de la table Client
class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    birthdate = db.Column(db.String(100), nullable=False)  
    email = db.Column(db.String(120))
    telephone = db.Column(db.String(20))

# Définition du modèle de la table Patho
class Patho(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doc = db.Column(db.Text)  

# Définition du modèle de la table kpi
class Kpi(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    cab = db.Column(db.String(100), nullable=False)

# Route POST pour ajouter un client
@app.route('/clients', methods=['POST'])
def create_client():
    # Récupère les données JSON envoyées dans la requête
    data = request.get_json()
    if not data:
        return jsonify({"message": "Aucune donnée fournie"}), 400

    # Récupère les informations du client depuis les données JSON
    nom = data.get('nom')
    prenom = data.get('prenom')
    birthdate = data.get('birthdate')
    email = data.get('email')
    telephone = data.get('telephone')

    # Vérifie que les informations obligatoires sont présentes
    if not nom or not prenom or not birthdate:
        return jsonify({"message": "Les champs nom, prenom et birthdate sont obligatoires"}), 400

    # Crée un nouveau client
    new_client = Client(nom=nom, prenom=prenom, birthdate=birthdate, email=email, telephone=telephone)

    # Ajoute le client à la base de données
    db.session.add(new_client)
    db.session.commit()

    # Retourne une réponse de succès
    return jsonify({"message": "Client cree avec succes"}), 201

# Route de test
@app.route('/')
def home():
    return "L'application Flask est en cours d'exécution !"

if __name__ == '__main__':
    # Créer les tables dans la base de données
    with app.app_context():
        db.create_all()
    app.run(debug=True)
