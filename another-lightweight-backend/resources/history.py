from flask_restful import Resource
from flask import request
from http import HTTPStatus

from middlewares import jwt_required
from middlewares import role_required


class History(Resource):
    @jwt_required
    @role_required(['user', 'admin'])
    def get(self):
        user_id = request.args.get('user_id')
        sensor_id = request.args.get('sensor_id')
        start = request.args.get('start')
        end = request.args.get('end')

        # TODO
        # Real-time access requires a dedicated database, which has not been implemented yet.
        # For now, placeholder data is being used as a temporary solution.

        dump_data = {
            'metric': 'temperature',
            'unit': 'C',
            'start': '2023-03-15T12:34:56Z',
            'end': '2023-03-15T12:34:56Z',
            'sum': 10000,
            'location': 'HCMUT.H6.812',
            'status': 'on',
            'feed_id': 'trungdunglebui17112004@gmail.com_sensor101',
            'records': [
                {
                    'timestamp': '2023-03-15T12:00:00Z',
                    'value': 25.3
                },
                {
                    'timestamp': '2023-03-15T12:05:00Z',
                    'value': 25.5
                },
                {
                    'timestamp': '2023-03-15T12:10:00Z',
                    'value': 25.7
                }
            ]
        }

        return dump_data, HTTPStatus.OK