from flask_restful import Resource
from flask import request
import jwt
from datetime import datetime, timedelta, timezone
from flask import current_app
from http import HTTPStatus

from schema import GithubLoginSchema
from app.services import auth
from app.services import db
from models.User import User


# TODO handle IDOR
class GithubLogin(Resource):
    def post(self):
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
        decoded_token['exp'] = int((datetime.fromtimestamp(decoded_token['iat'], tz=timezone.utc) + timedelta(days=3)).timestamp())
        token = jwt.encode(
            payload=decoded_token,
            key=current_app.config['JWT_SECRET_KEY'],
            algorithm='HS256',
        )

        return {
            'access_token' : token,
            'user_id' : user_id,
            'email' : email,
            'role' : user_role
        }, HTTPStatus.OK