import pytest
from app import create_app
from src.database.db import db
from src.routes.tours import main

@pytest.fixture
def app():
    app = create_app()

    with app.app_context():
        db.create_all()

    app.register_blueprint(main, name='tour_blueprint')  

    yield app

@pytest.fixture()
def client(app):
    return app.test_client()

def test_create_tour(app, client):
    with app.app_context():
        # Define los datos que se enviarán en la solicitud
        new_tour_data = {
            "nameTour": "tour desde testing",
            "descriptionTour": "testing desde testing",
            "date_str": '25/07/2024',
            "price": 12000,
        }
        
        #Agregar token a la peticion
        headers = {'Authorization': 'Bearer token_valido'}

        print(new_tour_data)
        response = client.post('/newtour', json=new_tour_data, headers=headers)
        print(response.json)
        assert response.status_code == 200

        assert 'nameTour' in response.json
        assert 'descriptionTour' in response.json
        assert 'date' in response.json
        assert 'price' in response.json
        assert 'user_id' in response.json


def test_update_tour(app, client):
    with app.app_context():
        tour_id = 1

        # Define los datos que se enviarán en la solicitud PUT
        updated_tour_data = {
            "nameTour": "Tour por argentina",
        }

        response = client.put(f'/update/{tour_id}', json=updated_tour_data)

        assert response.status_code == 200
        assert 'nameTour' in response.json
        assert response.json['nameTour'] == updated_tour_data['nameTour']
        

def test_delete_tour(app, client):
    with app.app_context():

        tour_id = 5

        response = client.delete(f'/delete/{tour_id}')

        assert response.status_code == 200
        assert 'tours' in response.json
        assert response.json['tours'] == 'delete Tour'

