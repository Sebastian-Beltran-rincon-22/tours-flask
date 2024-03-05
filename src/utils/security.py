from decouple import config

import datetime
import jwt
import pytz
import traceback

from src.utils.logger import Logger

class Security():

    secret = config('JWT_KEY')
    tz = pytz.timezone("America/Bogota")

    @classmethod
    def generate_token(cls, authenticated_user, roles=None):
        try:
            payload = {
                'iat': datetime.datetime.now(tz=cls.tz),
                'exp': datetime.datetime.now(tz=cls.tz) + datetime.timedelta(minutes=10),
                'userName': authenticated_user.userName,
                'email': authenticated_user.email,
                'roles': roles or authenticated_user.roles,
                'id': authenticated_user.id
            }
            return jwt.encode(payload, cls.secret, algorithm="HS256")
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())

    @classmethod
    def verify_token(cls, headers):
        if 'Authorization' in headers.keys():
            authorization = headers['Authorization']
            encoded_token = authorization.split(" ")[1]

            if (len(encoded_token) > 0):
                try:
                    payload = jwt.decode(encoded_token, cls.secret, algorithms=["HS256"])
                    roles = list(payload['roles'])

                    if 'User' in roles:
                        return True, payload  # Devuelve un booleano y el token decodificado
                    return False, None  # Devuelve un booleano y None cuando no hay acceso
                except (jwt.ExpiredSignatureError, jwt.InvalidSignatureError):
                    return False, None
        return False, None
    
    