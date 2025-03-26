from marshmallow import Schema, fields, validate, ValidationError
class EnvironmentCreateSchema(Schema):
    env_id = fields.Str(required=True, data_key='env_id')
    location = fields.Str(required=True, data_key='location')
    type = fields.Str(required=True, data_key='type')
    desc = fields.Str(required=False, data_key='desc')