from flask import Blueprint, jsonify, request
from adafruitio_client import add_feed
from flask import current_app


feed_bp = Blueprint("feeds", __name__)


@feed_bp.route('/<feed_id>', methods=['POST'])
def create_feed(feed_id):
    '''
    - Require a group to be previously created in Ada Fruit (weird)

    - Endpoint to create a new feed in IO ada fruit
    - This is equal to set up the topic and create data storage for that topic (no need to persist database)
    - After this operation, the sensor can be set up to public data to this topic/feed_id -> data is collected in IO data fruit
    - If you want the data to be persisted in firestore, then add_sensor endpoint must be executed (to subscribe to the topic) -> data stored in FireStore
    - feed_id in the format group_id.feed_id
    '''
    try:
        group_name, feed_name = feed_id.split('.', 1)
        add_feed(group_name, feed_name)

        return jsonify({}), 201
    except Exception as e:
        current_app.logger.error(f'Fail to create new feed in {feed_id} with: {str(e)}')
        return jsonify({"error": "Internal server error"}), 500