from flask import Flask
from flask_restful import Api
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS

from resources.test import Test
from resources.github_auth import GithubLogin
from exceptions import register_error_handlers
from config.config import SERVICE_ACCOUNT_KEY
from config.config import JWT_SECRET_KEY


# init rest_api flask application
app = Flask(__name__)
# enable CORS
CORS(app)
# app configuration
app.config['SERVICE_ACCOUNT_KEY'] = SERVICE_ACCOUNT_KEY
app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY

api = Api(app)


# resources
api.add_resource(GithubLogin, '/api/v1/auth/github')
api.add_resource(Test, '/api/v1/tests')

# exceptions handler registration
register_error_handlers(app)


# Swagger UI configuration
SWAGGER_URL = "/api/docs"
API_URL = "/static/swagger.yaml"
swagger_ui = get_swaggerui_blueprint(SWAGGER_URL, API_URL)
app.register_blueprint(swagger_ui, url_prefix=SWAGGER_URL)


if __name__ == "__main__":
    app.run(debug=True)