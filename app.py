from flask import Flask
from src.routes import user, tours, bookings
from src.database.db import db
from config import DATABASE_CONNECTION_URI, secret_key
from flask_migrate import Migrate
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app, origins='http://localhost:4200') #CORS peticiones 
    app.secret_key = secret_key
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_CONNECTION_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = secret_key  # Reemplaza con tu clave secreta
    app.config['JWT_TOKEN_LOCATION'] = ['headers']
    app.config['TESTING'] = True
    db.init_app(app)
    migrate = Migrate(app,db)

    # Registrar blueprints
    app.register_blueprint(user.main, url_prefix ='/')
    app.register_blueprint(tours.main, url_prefix ='/tours')
    app.register_blueprint(bookings.main, url_prefix ='/bookings')

    return app



