import pytest
from app import create_app
from src.database.db import db
from src.routes.user import main

@pytest.fixture
def app():
    app = create_app()

    with app.app_context():
        db.create_all()

    app.register_blueprint(main, name='user_blueprint')  

    yield app

@pytest.fixture()
def client(app):
    return app.test_client()
#Register
def test_register(client):
    data = {'email':'correoejemplo1@gmail.com', 'userName':'pepitoperez', 'password': 'testing123'}
    print("Datos enviados:", data) 
    response = client.post('/new', json=data)
    json_data = response.get_json()

    assert response.status_code == 201
    assert json_data['token'] is not None


#Login
def test_login(client):
    data = {'email': 'correoejemplo1@gmail.com','password': 'testing123'}
    print("Datos enviados:", data) 
    response = client.post('/login', json=data)
    json_data = response.get_json()

    assert response.status_code == 200
    assert json_data['token'] is not None