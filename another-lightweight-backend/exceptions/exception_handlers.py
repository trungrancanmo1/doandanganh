'''
    define the global exception handlers
'''
from flask import jsonify
from marshmallow import ValidationError
from http import HTTPStatus
from datetime import datetime
import jwt

from .CustomException import CustomException
from .JwtMissingException import JwtMissingException


class Error:
    def __init__(self, code, message, details, timestamp):
        self.status = 'error'
        self.code = code
        self.message = message
        self.details = details
        self.timestamp = timestamp


    def to_dict(self):
        return {
            "status": self.status,              # Indicates this is an error response
            "error_code": self.code,            # A unique identifier for the error
            "message": self.message,            # A human-readable error message
            "details": self.details,            # Optional additional details about the error
            "timestamp": self.timestamp         # The timestamp of the error occurrence
        }


def register_error_handlers(app):
    
    @app.errorhandler(Exception)
    def global_exception_handler(error):

        return jsonify(
            Error(
                code=HTTPStatus.INTERNAL_SERVER_ERROR, 
                message='An internal server error has occurred', 
                details=str(error), 
                timestamp=datetime.utcnow().isoformat())
                .to_dict()
        ), HTTPStatus.INTERNAL_SERVER_ERROR


    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        return jsonify(
            Error(
                code=HTTPStatus.BAD_REQUEST,
                message="Validation failed",
                details=error.messages,
                timestamp=datetime.utcnow().isoformat()
            ).to_dict()
        ), HTTPStatus.BAD_REQUEST
    

    @app.errorhandler(CustomException)
    def handle_customer_error(error):
        return jsonify({"message": error.message}), HTTPStatus.NOT_FOUND
    

    @app.errorhandler(JwtMissingException)
    def handle_jwt_missing_error(error):
        return jsonify(
            Error(
                code=HTTPStatus.UNAUTHORIZED,
                message="JWT token is missing",
                details=str(error),
                timestamp=datetime.utcnow().isoformat()
            ).to_dict()
        ), HTTPStatus.UNAUTHORIZED
    

    @app.errorhandler(jwt.ExpiredSignatureError)
    def handle_expired_signature_error(error):
        return jsonify(
            Error(
                code=HTTPStatus.UNAUTHORIZED,
                message="JWT token has expired",
                details=str(error),
                timestamp=datetime.utcnow().isoformat()
            ).to_dict()
        ), HTTPStatus.UNAUTHORIZED