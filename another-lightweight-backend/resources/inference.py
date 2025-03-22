from flask_restful import Resource
from flask import request
from http import HTTPStatus

from middlewares import jwt_required
from middlewares import role_required


class Inference(Resource):
    @jwt_required
    @role_required(['admin', 'user'])
    def get(self):
        user_id = request.args.get('user_id')
        sensor_group = request.args.get('sensor_group')

        # TODO: Implement logic to query the database for the information of the inference
        # Placeholder for database query logic
        dump_data = {
            "sensor_group": "group1",
            "time_stamp": "2023-03-15T12:34:56Z",
            "inferences": {
                "temperature": {
                    "value": 25.5, 
                    "status": "normal"
                    },
                "light": {
                    "value": 300, 
                    "status": "normal"
                    },
                "humidity": {
                    "value": 60, 
                    "status": "normal"
                    },
                "camera": {
                    "value": "image_data_base64_placeholder",
                    "status": "normal",
                    "image_processed": True,
                    "insect_attack_detected": False
                }
            }
        }

        return dump_data, HTTPStatus.OK