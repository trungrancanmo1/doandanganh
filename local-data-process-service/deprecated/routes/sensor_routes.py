from flask import Blueprint, jsonify, request
from firebase import firestore_db
from adafruitio_client import mqtt_client
from flask import current_app


sensor_bp = Blueprint("sensors", __name__)


@sensor_bp.route('/<sensor_id>', methods=['POST'])
def add_sensor(sensor_id):
    try:
        # Get JSON data from request
        data = request.get_json()

        # Validate required fields
        required_fields = ["device_id", "location", "status", "topic", "user_id"]
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        # Perst the sensor information into database
        firestore_db.collection('sensors').add(document_data=data, document_id=sensor_id)

        # Tell the MQTT listener service to subscribe the topic of the newly added sensors
        topic = data['topic']
        mqtt_client.subscribe(feed_id=topic)
        current_app.logger.info(f'Subscribe to {topic}')
        
        return jsonify({}), 200
        
    except Exception:
        return jsonify({"error": "Internal server error"}), 500