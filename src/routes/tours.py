from flask import Blueprint, request,jsonify
import jwt
from src.models.tours import Tours
from src.database.db import db
from src.utils.security import Security
from datetime import datetime

main =Blueprint('tours',__name__)

#Crear Tour
@main.route('/newtour', methods=['POST'])
def add_tour():
    authorization_header = request.headers.get('Authorization')
    #bearer token
    if not authorization_header:
        response = jsonify({'message': 'Unauthorized - Missing Authorization header'})
        return response, 401

    try:
        authorization = authorization_header.split(" ")
        if len(authorization) != 2 or authorization[0].lower() != 'bearer':
            raise jwt.InvalidTokenError("Invalid Authorization header")

        encoded_token = authorization[1]
        decoded_token = jwt.decode(encoded_token, Security.secret, algorithms=["HS256"])
        
        roles = decoded_token.get('roles', [])
        
        if any(role == 'User' for role in roles):
            # Obtener el ID del usuario desde el token decodificado
            user_id = decoded_token['id']
            data = request.json
            # Validación de datos
            nameTour = data['nameTour']
            descriptionTour = data['descriptionTour']
            date_str = data['date_str']
            price = data['price']
            
            date_str = datetime.strptime(date_str, '%d/%m/%Y').date()

            new_tour = Tours(
                nameTour=nameTour,
                descriptionTour=descriptionTour,
                date=date_str,
                price=price,
                user_id=user_id
            )

            db.session.add(new_tour)
            db.session.commit()
            #Respuesta JSON
            return jsonify({
                'message': 'Tour creado con éxito',
                'nameTour': nameTour,
                'descriptionTour': descriptionTour,
                'date': new_tour.date.strftime('%d/%m/%Y'),
                'user_id': user_id,
                'price': price
            }),200
    #Manejo de errores
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError) as e:
        print(f"Error de decodificación del token: {e}")
        return "Token inválido o expirado", 401

    response = jsonify({'message': 'Unauthorized'})
    return response, 401


#Actualizar datos del tour
@main.route('/update/<int:id>', methods=['PUT'])
def update_tour(id):
    try:
        tour = db.session.get(Tours,id)

        if not tour:
            return jsonify({'error': 'Tour no encontrado'}), 404

        data = request.json

        tour.nameTour = data.get('nameTour', tour.nameTour)
        tour.descriptionTour = data.get('descriptionTour', tour.descriptionTour)

        # Manejo de formato de fecha
        date_str = data.get('date', None)
        if date_str:
            tour.date = datetime.strptime(date_str, '%d/%m/%Y').date()

        tour.price = data.get('price', tour.price)

        db.session.commit()

        #Respuesta JSON
        return jsonify({
            'message': 'Tour actualizado con éxito',
            'nameTour': tour.nameTour,
            'descriptionTour': tour.descriptionTour,
            'date': tour.date.strftime('%d/%m/%Y') if tour.date else None,
            'price': tour.price
        }), 200
    #Manejo de Errores
    except ValueError as e:
        return jsonify({'error': f'Error de formato en la fecha: {str(e)}'}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 500


#GET Tours
@main.route('/toursdetails', methods=['GET'])
def get_tour():
    try:
        #Busqueda de tours
        tours = Tours.query.all()
        #Datos a mostrar
        tours_data = [{'id': tour.id, 'nameTour': tour.nameTour ,
            'descriptionTour': tour.descriptionTour, 
            'date': tour.date, 
            'price': tour.price} for tour in tours]

        return jsonify({'tours': tours_data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


#Delete Tour
@main.route('/delete/<id>', methods = ["DELETE", "GET"])
def delete_tour(id):
    try:
        #Busqueda del Tour poe ID
        tour = db.session.get(Tours,id)
        #Eliminar Tour
        db.session.delete(tour)
        db.session.commit()

        return jsonify({'tours': "delete Tour"}), 200 #Respuesta JSON
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/tourfor/<int:tour_id>', methods=['GET'])
def get_tour_by_id(tour_id):
    try:
        tour = db.session.get(Tours, tour_id)
        if tour:
            tour_data = {
                'id': tour.id,
                'nameTour': tour.nameTour,
                'descriptionTour': tour.descriptionTour,
                'date': tour.date,
                'price': tour.price
            }
            return jsonify({'tour': tour_data}), 200
        else:
            # Si no se encuentra el tour, devuelve un mensaje de error
            return jsonify({'error': 'Tour no encontrado'}), 404

    except Exception as e:
        # Manejar otros errores
        return jsonify({'error': str(e)}), 500