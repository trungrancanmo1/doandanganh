from flask import Flask
import threading
from adafruitio_client import mqtt_listener
from routes import sensor_bp
from routes import feed_bp

app = Flask(__name__)
app.logger.setLevel(level='DEBUG')


# register blueprints
app.register_blueprint(sensor_bp, url_prefix="/api/v1/sensors")
app.register_blueprint(feed_bp, url_prefix='/api/v1/feeds')


# run the mtqq listener service
mttq_listener_service = threading.Thread(target=mqtt_listener, daemon=True)
mttq_listener_service.start()


if __name__ == "__main__":
    app.run(debug=True, port=5000, use_reloader=False)