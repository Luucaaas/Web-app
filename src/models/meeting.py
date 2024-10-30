from . import db

class Meeting(db.Model):  
    __tablename__ = 'meeting'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    heure = db.Column(db.Time, nullable=False)  
    cab = db.Column(db.String(100), nullable=False)