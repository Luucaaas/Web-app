from . import db

class Client(db.Model):
    __tablename__ = 'client'  
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    birthdate = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120))
    telephone = db.Column(db.String(20))
    doc = db.Column(db.Text)

