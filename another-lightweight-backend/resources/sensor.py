from flask_restful import Resource
from flask import request
from http import HTTPStatus
from werkzeug.exceptions import NotFound
from firebase_admin.firestore import firestore

from app.services.firebase_firestore import db
from schema.SensorAddSchema import SensorAddSchema
from middlewares.jwt_middleware import jwt_required
from middlewares.role_based_access_control import role_required


class SensorListResource(Resource):

    @jwt_required
    @role_required(['admin', 'user'])
    def post(self, user_id, env_id):
        schema = SensorAddSchema()
        body = schema.load(request.get_json())

        ORG = 'hcmut-smart-farm'
        USERS = 'users'
        ENVS = 'envs'
        SENSORS = 'sensors'
        TYPE = body.get('type')
        DATA = 'data'

        feed_id = '-'.join([ORG, USERS, user_id.lower(), ENVS, env_id.lower(), TYPE.lower(), SENSORS, body['sensor_id'].lower(), DATA])

        data = {
            'user_id' : user_id,
            'env_id' : env_id,
            'sensor_id' : body['sensor_id'],
            'type' : body['type'],
            'status' : body['status'],
            'unit' : body['unit'],
            'feed_id' : feed_id
        }

        # TODO check for dupplication in sensors

        update_time, sensor_ref = db.collection('sensors').add(document_data=data)

        env_ref = db.document('users', user_id, 'environments', env_id)
        env_ref.update(
            {
                'sensor_references' : firestore.ArrayUnion([sensor_ref])
            }
        )

        response = {
            'user_id' : user_id,
            'env_id' : env_id,
            'sensor_id' : body['sensor_id'],
            'type' : body['type'],
            'status' : body['status'],
            'unit' : body['unit'],
            'feed_id' : feed_id
        }

        return response, HTTPStatus.CREATED
    

    @jwt_required
    @role_required(['admin', 'user'])
    def get(self, user_id, env_id):
        sensors_query = db.collection('sensors').where('user_id', '==', user_id).where('env_id', '==', env_id).stream()

        sensors = []
        for sensor in sensors_query:
            sensor_data = sensor.to_dict()
            sensor_data['id'] = sensor.id
            sensors.append(sensor_data)

        response = {
            'user_id': user_id,
            'env_id': env_id,
            'sensors': sensors
        }

        return response, HTTPStatus.OK


class SensorResource(Resource):

    @jwt_required
    @role_required(['admin', 'user'])
    def delete(self, user_id, env_id, sensor_id):

        sensors_query = db.collection('sensors').where('user_id', '==', user_id).where('env_id', '==', env_id).where('sensor_id', '==', sensor_id).stream()
        
        sensor_refs = list(sensors_query)
        if not sensor_refs:
            raise NotFound(f"Sensor with ID {sensor_id} not found within user {user_id} and environment {env_id}.")
        
        for sensor_ref in sensor_refs:
            sensor_ref.reference.delete()

        env_ref = db.document('users', user_id, 'environments', env_id)
        env_ref.update(
            {
                'sensor_references': firestore.ArrayRemove([sensor_ref.reference for sensor_ref in sensor_refs])
            }
        )

        return '', HTTPStatus.NO_CONTENT