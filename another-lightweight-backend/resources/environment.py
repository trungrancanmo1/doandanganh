from flask_restful import Resource
from flask import request
from http import HTTPStatus
from werkzeug.exceptions import NotFound

from app.services.firebase_firestore import db
from schema.EnvironmentCreateSchema import EnvironmentCreateSchema
from middlewares.jwt_middleware import jwt_required
from middlewares.role_based_access_control import role_required


class EnvironmentListResource(Resource):

    @jwt_required
    @role_required(['admin', 'user'])
    def post(self, user_id):
        schema = EnvironmentCreateSchema()
        body = schema.load(request.get_json())

        data = {
            'location' : body.get('location'),
            'type' : body.get('type'),
            'desc' : body.get('desc', 'My green environment')
        }

        update_time, env_ref = db.collection('users', user_id, 'environments').add(document_id=body.get('env_id'), document_data=data)

        response = {
            'env_id' : body.get('env_id'),
            'location' : data['location'],
            'type' : data['type']
        }

        return response, HTTPStatus.CREATED
    

    @jwt_required
    @role_required(['admin', 'user'])
    def get(self, user_id):
        documents = db.collection('users', user_id, 'environments').get()

        env_list = [{
            'env_id' : d.id,
            'location' : d.get('location'),
            'type' : d.get('type')
        } for d in documents]

        return env_list, HTTPStatus.OK


class EnvironmentResource(Resource):

    @jwt_required
    @role_required(['user', 'admin'])
    def get(self, user_id, env_id):
        '''
        - get environment resource of a user
        '''
        document = db.document('users', user_id, 'environments', env_id).get()

        response = {
            'env_id' : document.id,
            'location' : document.get('location'),
            'type' : document.get('type')
        }

        return response, HTTPStatus.OK


    @jwt_required
    @role_required(['admin', 'user'])
    def delete(self, user_id, env_id):
        '''
        - delete an environment of a user
        '''
        document_ref = db.document('users', user_id, 'environments', env_id)
        document = document_ref.get()

        if not document.exists:
            raise NotFound(env_id)

        document_ref.delete()

        return '', HTTPStatus.NO_CONTENT