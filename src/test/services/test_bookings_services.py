import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime
from src.services.bookings_services import BookingsService
from src.models.bookings import Bookings

@pytest.fixture
def mock_db_session():
    return MagicMock()

def test_get_all_bookings(mock_db_session):
    with patch('src.services.bookings_services.db.session', mock_db_session):
        mock_db_session.query.return_value.all.return_value = [
            Bookings(nameUser="User1", dateBooking=datetime.now(), numPerson=2, surName="Surname1", tours_id=1),
            Bookings(nameUser="User2", dateBooking=datetime.now(), numPerson=1, surName="Surname2",tours_id=2),
        ]

        # Llamamos al método
        bookings = BookingsService.get_all_bookings()

    # Afirmaciones
    assert isinstance(bookings, list)
    assert len(bookings) == 2  # instancias simuladas
    assert bookings[0].nameUser == "User1"
    assert bookings[1].nameUser == "User2"
    assert all(isinstance(booking.tours_id, int) and booking.tours_id is not None for booking in bookings)  # tours_id válidos

