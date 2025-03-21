from flask import Flask
from flask_restful import Api
from flask_swagger_ui import get_swaggerui_blueprint

from resources.test import Test


app = Flask(__name__)
api = Api(app)


# api.add_resource(UserList, "/users")
api.add_resource(Test, '/api/v1/tests')


# Swagger UI
SWAGGER_URL = "/api/docs"
API_URL = "/static/swagger.yaml"

swagger_ui = get_swaggerui_blueprint(SWAGGER_URL, API_URL)
app.register_blueprint(swagger_ui, url_prefix=SWAGGER_URL)

if __name__ == "__main__":
    app.run(debug=True)