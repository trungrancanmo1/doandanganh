from flask_restful import Resource
from flask import request
from http import HTTPStatus
from werkzeug.exceptions import NotFound
from firebase_admin.firestore import firestore

from app.services.firebase_firestore import db
from schema.ActuatorAddSchema import ActuatorAddSchema
from middlewares.jwt_middleware import jwt_required
from middlewares.role_based_access_control import role_required


class ActuatorListResource(Resource):

    @jwt_required
    @role_required(['admin', 'user'])
    def post(self, user_id, env_id):
        schema = ActuatorAddSchema()
        body = schema.load(request.get_json())

        ORG = 'hcmut-smart-farm'
        USERS = 'users'
        ENVS = 'envs'
        ACTUATORS = 'actuators'
        TYPE = body.get('type')
        COMMAND = 'command'
        STATUS = 'status'

        command_feed_id = '-'.join([ORG, USERS, user_id.lower(), ENVS, env_id.lower(), TYPE.lower(), ACTUATORS, body['actuator_id'].lower(), COMMAND])
        status_feed_id = '-'.join([ORG, USERS, user_id.lower(), ENVS, env_id.lower(), TYPE.lower(), ACTUATORS, body['actuator_id'].lower(), STATUS])

        data = {
            'user_id': user_id,
            'env_id': env_id,
            'actuator_id': body['actuator_id'],
            'type': body['type'],
            'status': body['status'],
            'command_feed_id': command_feed_id,
            'status_feed_id': status_feed_id,
            'last_command': '',
            'auto_mode' : False,
            'min' : 0,
            'max' : 0,
        }

        # TODO check for duplication in actuators

        update_time, actuator_ref = db.collection('actuators').add(document_data=data)

        env_ref = db.document('users', user_id, 'environments', env_id)
        env_ref.update(
            {
                'actuator_references': firestore.ArrayUnion([actuator_ref])
            }
        )

        response = {
            'user_id': user_id,
            'env_id': env_id,
            'actuator_id': body['actuator_id'],
            'type': body['type'],
            'status': body['status'],
            'command_feed_id' : command_feed_id,
            'status_feed_id' : status_feed_id,
            'last_command' : '',
            'auto_mode' : False,
            'min' : 0,
            'max' : 0,
        }

        return response, HTTPStatus.CREATED


    @jwt_required
    @role_required(['admin', 'user'])
    def get(self, user_id, env_id):
        actuators_query = db.collection('actuators').where('user_id', '==', user_id).where('env_id', '==', env_id).stream()

        actuators = []
        for actuator in actuators_query:
            actuator_data = actuator.to_dict()
            actuator_data['id'] = actuator.id
            actuators.append(actuator_data)

        response = {
            'user_id': user_id,
            'env_id': env_id,
            'actuators': actuators
        }

        return response, HTTPStatus.OK


class ActuatorResource(Resource):

    @jwt_required
    @role_required(['admin', 'user'])
    def delete(self, user_id, env_id, actuator_id):

        actuators_query = db.collection('actuators').where('user_id', '==', user_id).where('env_id', '==', env_id).where('actuator_id', '==', actuator_id).stream()

        actuator_refs = list(actuators_query)
        if not actuator_refs:
            raise NotFound(f"Actuator with ID {actuator_id} not found within user {user_id} and environment {env_id}.")

        for actuator_ref in actuator_refs:
            actuator_ref.reference.delete()

        env_ref = db.document('users', user_id, 'environments', env_id)
        env_ref.update(
            {
                'actuator_references': firestore.ArrayRemove([actuator_ref.reference for actuator_ref in actuator_refs])
            }
        )

        return '', HTTPStatus.NO_CONTENT