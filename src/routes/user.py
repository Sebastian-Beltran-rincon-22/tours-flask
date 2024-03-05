import bcrypt
import traceback
from flask import Blueprint,request,jsonify
from src.models.user import User
from src.database.db import db
from src.utils.security import Security
from src.utils.logger import Logger
from typing import List


main =Blueprint('user',__name__)

@main.route('/new', methods=['POST'])
def register():
    try:
        # Accede a los datos JSON
        data = request.json
        userName = data['userName']
        email = data['email']
        password = data['password']
        roles: List[str] = data.get('roles', ['User'])
        
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        new_user = User(userName, email, hashed_password, roles=roles)

        db.session.add(new_user)
        db.session.commit()
        
        token = Security.generate_token(new_user, roles=new_user.roles)

        # Devuelve una respuesta JSON con un mensaje
        return jsonify({'message': 'Usuario creado correctamente', 'user_id': new_user.id , 'email':email, 'password':hashed_password, 'token':token}), 201
    except KeyError as e:
        # Captura excepciones específicas relacionadas con datos faltantes
        return jsonify({'error': f'Missing required field: {str(e)}'}), 400
    except Exception as e:
        # Captura otras excepciones y devuelve un mensaje de error general
        return jsonify({'error': str(e)}), 500

#loginUser
@main.route('/login', methods=['POST'])
def login():
    try:
        email = request.json['email']
        password = request.json['password']

        # Obtén el usuario de la base de datos por email
        user = User.query.filter_by(email=email).first()

        # Verifica si el usuario existe y si la contraseña coincide
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            # Usuario autenticado, generación del token
            encoded_token = Security.generate_token(user)
            return jsonify({'success': True, 'token': encoded_token}),200
        else:
            # Usuario no autenticado
            response = jsonify({'message': 'Unauthorized'})
            return response, 401
    except Exception as ex:
        Logger.add_to_log("error", str(ex))
        Logger.add_to_log("error", traceback.format_exc())

        return jsonify({'message': "ERROR", 'success': False})


#GET USERS
@main.route('/users', methods=['GET'])
def get_users():
    try:
        # Obtén la lista de todos los usuarios desde la base de datos
        users = User.query.all()

        # Formatea los detalles de cada usuario en un diccionario
        users_data = [{'id': user.id, 'userName': user.userName, 'email': user.email, 'roles': user.roles} for user in users]

        # Devuelve una respuesta JSON con la lista de usuarios
        return jsonify({'users': users_data}), 200
    except Exception as e:
        # Maneja excepciones y devuelve un mensaje de error
        return jsonify({'error': str(e)}), 500

#DELETE USER
@main.route('/deleteuser/<id>', methods = ["DELETE", "GET"])
def delete_user(id):
    try:
        user = db.session.get(User,id)
        db.session.delete(user)
        db.session.commit()
    
            # Devuelve una respuesta JSON con la lista de usuarios
        return jsonify({'users': "delete User"}), 200
    except Exception as e:
        # Maneja excepciones y devuelve un mensaje de error
        return jsonify({'error': str(e)}), 500