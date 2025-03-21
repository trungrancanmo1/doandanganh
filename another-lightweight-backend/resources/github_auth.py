from flask_restful import Resource
from flask import request
import jwt
from datetime import datetime, timedelta
from flask import current_app
from flask import jsonify
from http import HTTPStatus

from schema import GithubLoginSchema
from app.services import auth
from app.services import db
from models.User import User


class GithubLogin(Resource):
    def post(self):
        # must have the JWT generated from firebase' Auth2
        # this endpoint will extract that JWT
        # and then verify that JWT with firebase again
        # and then generate a new JWT that include the role of the user
        # this JWT is used with this back-end application later on
        schema = GithubLoginSchema()
        data = schema.load(request.get_json())
        decoded_token = auth.verify_id_token(id_token=data['firebase_jwt'])

        # extract the jwt information
        github_name = decoded_token['name']
        user_id = decoded_token['user_id']
        email = decoded_token['email']
        user_doc = db.collection('users').document(document_id=user_id)

        # check that the user_doc has been created
        if not user_doc.get().exists:
            # create the user
            user_doc_data = User(name=github_name, email=email, role='user').to_dict()
            user_doc.set(user_doc_data)
            user_role = 'user'
        else:
            user_role = user_doc.get().to_dict().get('role')
        
        # create new jwt
        decoded_token['role'] = user_role
        decoded_token['exp'] = (datetime.utcnow() + timedelta(hours=1)).isoformat()
        token = jwt.encode(
            payload=decoded_token,
            key=current_app.config['JWT_SECRET_KEY'],
            algorithm='HS256'
        )

        return {
            'access_token' : token
        }, HTTPStatus.OK