from flask_restful import Resource
from flask import request
from http import HTTPStatus

from middlewares.jwt_middleware import jwt_required
from middlewares.role_based_access_control import role_required


class Statistics(Resource):
    @jwt_required
    @role_required(['admin', 'user'])
    def get(self):
        user_id = request.args.get('user_id')
        sensor_group = request.args.get('sensor_group')
        # TODO
        # This functionality is currently implemented as a REST API.
        # Future versions should transition to using WebSockets for improved efficiency.

        # Real-time access requires a dedicated database, which has not been implemented yet.
        # For now, placeholder data is being used as a temporary solution.
        dump_data = {
            'temperature': {
                'value': 30,
                'time_stamp': '2023-03-15T12:34:56Z',
                'sensor_id': 'sensor101',
                'location': 'HCMUT.H6.812',
                'metric': 'temperature',
                'unit': 'C',
                },
            'humidity': {
                'value': 60,
                'time_stamp': '2023-03-15T12:34:56Z',
                'sensor_id': 'sensor102',
                'location': 'HCMUT.H6.812',
                'metric': 'humidity',
                'unit': '%',
                },
            'light': {
                'value': 300,
                'time_stamp': '2023-03-15T12:34:56Z',
                'sensor_id': 'sensor103',
                'location': 'HCMUT.H6.812',
                'metric': 'light',
                'unit': 'lux',
                },
            'picture' : {
                'url' : 'https://server.com/image.png',
                'time_stamp' : '2023-03-15T12:34:56Z',
                'camera' : 'camera_101',
                'location' : 'HCMUT.H6.812',
            }
        }
        
        return dump_data, HTTPStatus.OK