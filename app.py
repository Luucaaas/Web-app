from flask import Flask
from flask_jwt_extended import JWTManager
from config import Config
from src.models import db
from src.routes.clients import client_bp
from src.routes.meetings.routes import meeting_bp


app = Flask(__name__)
app.config.from_object(Config)

# Initialiser les extensions
db.init_app(app)
jwt = JWTManager(app)

# Enregistrer les blueprints

app.register_blueprint(client_bp,url_prefix="/clients")
app.register_blueprint(meeting_bp, url_prefix="/api")



@app.route('/')
def home():
    return "L'application Flask est en cours d'exécution !"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)


