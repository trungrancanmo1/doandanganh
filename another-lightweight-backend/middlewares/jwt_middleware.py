from functools import wraps
from flask import request
import jwt
from flask import current_app, g
import datetime

from exceptions import JwtMissingException


def jwt_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        # decorate with jwt authentication logic
        header = request.headers.get('Authorization')

        if not header:
            raise JwtMissingException()
        
        # Bearer <token>
        token = header.split(' ')[1]
        decoded_token = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
        exp = decoded_token['exp']
        
        if exp < datetime.datetime.utcnow().timestamp():
            raise jwt.ExpiredSignatureError("Token has expired")
        
        g.user_id = decoded_token.get('user_id')
        g.role = decoded_token.get('role')
        g.email = decoded_token.get('email')

        # excute original function
        return func(*args, **kwargs)

    return decorated