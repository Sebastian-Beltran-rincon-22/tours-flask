import traceback
from src.database.db import db
from src.utils.logger import Logger
from src.models.user import User

class AuthService():

    @classmethod
    def login_user(cls, user):
        try:
            authenticated_user = db.session.query(User).filter_by(email=user.email, password=user.password).first()

            return authenticated_user
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())


