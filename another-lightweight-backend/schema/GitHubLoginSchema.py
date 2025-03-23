from marshmallow import Schema, fields, validate, ValidationError
class GithubLoginSchema(Schema):
    firebase_jwt = fields.Str(required=True, data_key='firebase_jwt')