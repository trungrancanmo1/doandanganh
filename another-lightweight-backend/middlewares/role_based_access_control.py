from functools import wraps
from flask import g
from werkzeug import exceptions

from utils.logger import logger


# curried function
def role_required(roles):
    def decorator(func):
        @wraps(func)
        def decorated(*args, **kargs):
            if not hasattr(g, 'role'):
                raise exceptions.Unauthorized()
            
            role = g.get('role')

            if role not in roles:
                raise exceptions.Forbidden()
            
            logger.info(f'Authorize successfully: {role}')
            return func(*args, **kargs)
        return decorated
    return decorator