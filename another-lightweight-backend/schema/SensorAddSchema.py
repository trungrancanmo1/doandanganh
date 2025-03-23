from marshmallow import Schema, fields, validate, ValidationError
class SensorAddSchema(Schema):
    type = fields.Str(data_key='type', required=True)
    status = fields.Bool(
        truthy=['true', 'on'], 
        falsy=['false', 'off'], 
        required=False, 
        missing=False, 
        validate=validate.OneOf([True, False, 'true', 'on', 'false', 'off'])
    )
    # feed_id = fields.Str(data_key='feed_id', required=True)
    unit = fields.Str(data_key='unit', required=True)
    sensor_id = fields.Str(data_key='sensor_id', required=True)