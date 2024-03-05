from src.database.db import db


class Tours(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nameTour = db.Column(db.String(40), nullable = False)
    descriptionTour = db.Column(db.String(300))
    date = db.Column(db.DateTime())
    price = db.Column(db.Float, nullable = True)
    bookings = db.relationship('Bookings', backref='tours', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable = False)

    def __init__(self, nameTour,descriptionTour, date, price, user_id):
        self.nameTour = nameTour
        self.descriptionTour = descriptionTour
        self.date = date
        self.price = price
        self.user_id = user_id