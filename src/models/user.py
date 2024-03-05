from src.database.db import db

class User(db.Model):
    
    id = db.Column(db.Integer, primary_key = True)
    userName = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(250), nullable=False)
    tours = db.relationship('Tours', backref='user', lazy=True)
    roles = db.Column(db.JSON) 
    
    def __init__(self, userName, email,password, roles= None):
        self.userName = userName
        self.email = email
        self.password = password
        self.roles = roles if roles else []