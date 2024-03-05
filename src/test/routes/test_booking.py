from datetime import datetime, timezone
from dateutil import parser
from flask import Flask
from src.models.bookings import Bookings
from src.routes.bookings import main
from app import create_app
from src.database.db import db
import pytest

@pytest.fixture
def app():
    app = create_app()

    with app.app_context():
        db.create_all()

    app.register_blueprint(main, name='bookings_blueprint')  

    yield app

@pytest.fixture()
def client(app):
    return app.test_client()

#Prueba para crear reservas
def test_create_booking(app, client):
    with app.app_context():
        # Define los datos que se enviarán en la solicitud POST
        new_booking_data = {
            "nameUser": "johan",
            "surName": "beltran",
            "numPerson": 12,
            "tours_id": 1,
            "dateBooking_str": '25/07/2024'
        }

        print(new_booking_data)
        response = client.post('/newbooking', json=new_booking_data)
        print(response.json)
        assert response.status_code == 201

        assert 'nameUser' in response.json
        assert 'surName' in response.json
        assert 'dateBooking' in response.json
        assert 'numPerson' in response.json
        assert 'tours_id' in response.json


# Prueba para obtener datos existentes
def test_list_booking_route(app, client):
    with app.app_context():

        existing_booking_data = [
            Bookings(
                nameUser="juan",
                surName="sanchez",
                numPerson=12,
                tours_id=1,
                dateBooking=datetime(2024, 7, 25, 0, 0, 0, tzinfo=timezone.utc)
            ),
        ]
        
        response = client.get('/completebooking')

        assert response.status_code == 200
        assert 'booking' in response.json

        id = 2

        formatted_response = {
            'booking': [
                {
                    'id': id,
                    'nameUser': booking['nameUser'],
                    'surName': booking['surName'],
                    'dateBooking': existing_booking_data[0].dateBooking.strftime('%a, %d %b %Y %H:%M:%S GMT'),
                    'numPerson': booking['numPerson'],
                    'tours_id': booking['tours_id']
                }
                for booking in response.json['booking']
            ]
        }
        
        formatted_response['booking'] = sorted(formatted_response['booking'], key=lambda x: x['id'])

        fields_to_compare = ['id','nameUser', 'surName', 'dateBooking', 'numPerson', 'tours_id']
        formatted_response['booking'] = [{field: booking[field] for field in fields_to_compare} for booking in formatted_response['booking']]

        assert formatted_response
        
#Prueba de eliminar reserva
def test_delete_booking(app, client):
    with app.app_context():

        booking_id = 3

        response = client.delete(f'/deletebooking/{booking_id}')

        assert response.status_code == 200
        assert 'message' in response.json
        assert response.json['message'] == 'Booking deleted successfully'
