from functools import wraps
from flask import request
import jwt
from flask import current_app, g
import datetime

from exceptions import JwtMissingException
from utils.logger import logger


def jwt_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        # decorate with jwt authentication logic
        header = request.headers.get('Authorization')

        if not header:
            raise JwtMissingException()
        
        # Bearer <token>
        token = header.split(' ')[1]
        decoded_token = jwt.decode(
            token, 
            current_app.config['JWT_SECRET_KEY'], 
            algorithms=['HS256'],
            audience='user-smart-farm',
            issuer='https://securetoken.google.com/user-smart-farm')
        exp = decoded_token['exp']
        
        if int(exp) < int(datetime.datetime.now(datetime.timezone.utc).timestamp()):
            raise jwt.ExpiredSignatureError()
        
        g.user_id = decoded_token.get('user_id')
        g.role = decoded_token.get('role')
        g.email = decoded_token.get('email')

        # excute original function
        logger.info(f'Authenticate successfully: {g.email}')
        return func(*args, **kwargs)

    return decorated