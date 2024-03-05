import traceback
from src.database.db import db
from src.utils.logger import Logger
from src.models.bookings import Bookings

class BookingsService():
    
    @classmethod
    def get_all_bookings(cls):
        try:
            bookings = db.session.query(Bookings).all()
            
            return bookings
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
        finally:
            db.session.close()