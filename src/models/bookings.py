from src.database.db import db
from datetime import datetime

class Bookings(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    nameUser = db.Column(db.String(30))
    surName = db.Column(db.String(30))
    dateBooking = db.Column(db.DateTime, default=datetime.utcnow,nullable=True)
    numPerson = db.Column(db.Integer)
    tours_id = db.Column(db.Integer, db.ForeignKey("tours.id"), nullable = False)
    
    def __init__(self, nameUser, dateBooking, numPerson, surName, tours_id):
        self.nameUser = nameUser
        self.surName = surName
        self.dateBooking = dateBooking
        self.numPerson = numPerson
        self.tours_id = tours_id