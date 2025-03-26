from marshmallow import Schema, fields, validate, ValidationError


class ActuatorAddSchema(Schema):
    type = fields.Str(data_key='type', required=True)
    status = fields.Bool(
        truthy=['true', 'on'], 
        falsy=['false', 'off'], 
        required=False, 
        missing=False, 
        validate=validate.OneOf([True, False, 'true', 'on', 'false', 'off'])
    )
    actuator_id = fields.Str(data_key='actuator_id', required=True)