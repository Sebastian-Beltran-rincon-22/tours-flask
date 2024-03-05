from flask import Blueprint, request,jsonify
from sqlalchemy.exc import IntegrityError
from src.models.bookings import Bookings
from src.database.db import db 
from datetime import datetime

main = Blueprint('booking',__name__)

#Metodo para crear nuevas reservas
@main.route('/newbooking', methods=['POST'])
def add_booking():
    try:
        data = request.json
        
        # Validación de datos
        required_fields = ['nameUser', 'surName', 'dateBooking_str', 'numPerson', 'tours_id']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        dateBooking_str = datetime.strptime(data['dateBooking_str'], '%d/%m/%Y').date()
        # Crear nueva reserva
        new_booking = Bookings(
            nameUser=data['nameUser'],
            surName=data['surName'],
            dateBooking = dateBooking_str,
            numPerson=data['numPerson'],
            tours_id=data['tours_id']
        )

        db.session.add(new_booking)
        db.session.commit()

        return jsonify({
            'message': 'Reserva realizada con éxito',
            'nameUser': new_booking.nameUser,
            'surName': new_booking.surName,
            'dateBooking': new_booking.dateBooking.strftime('%d/%m/%Y'), 
            'numPerson': new_booking.numPerson,
            'tours_id': new_booking.tours_id
        }), 201

    except IntegrityError as e:
        db.session.rollback() 
        return jsonify({'error': 'Error de integridad en la base de datos'}), 500

    except ValueError as e:
        return jsonify({'error': f'Error de formato en la fecha: {str(e)}'}), 400
    
    except KeyError as e:
        return jsonify({'error': f'Missing required field: {str(e)}'}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 500


#Buscar reserva por nombre
@main.route('/listbookings/<string:nameUser>', methods=['GET'])
def get_booking(nameUser):
    try:
        # Filtrar las reservas por nameUser
        bookings = Bookings.query.filter_by(nameUser=nameUser).all()

        # Crear una lista con los datos de las reservas
        booking_data = [
            {
                'id': booking.id, 
                'nameUser': booking.nameUser, 
                'surName': booking.surName, 
                'dateBooking': booking.dateBooking.strftime('%d/%m/%Y'),  # Formatear la fecha a cadena
                'numPerson': booking.numPerson, 
                'tours_id': booking.tours_id
            } 
            for booking in bookings
        ]

        return jsonify({'bookings': booking_data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


#Eliminar Reserva
@main.route('/deletebooking/<id>', methods=["DELETE"])
def delete_booking(id):
    try:
        booking = db.session.get(Bookings, id)

        if booking is None:
            return jsonify({'error': 'Booking not found'}), 404

        db.session.delete(booking)
        db.session.commit()

        return jsonify({'message': 'Booking deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


#lista completa de reservas
@main.route('/completebooking', methods=['GET'])
def list_booking():
    try:
        bookings = Bookings.query.all()

        #Datos que traera para la respuesta JSON
        booking_data = [{'id': booking.id, 
            'nameUser': booking.nameUser, 
            'surName': booking.surName, 
            'dateBooking': booking.dateBooking,
            'numPerson': booking.numPerson, 
            'tours_id': booking.tours_id } for booking in bookings]

        return jsonify({'booking': booking_data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500