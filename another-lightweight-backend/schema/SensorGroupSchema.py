from marshmallow import Schema, fields


class SensorSchema(Schema):
    value = fields.Raw()
    status = fields.String()


class CameraSchema(SensorSchema):
    sensor_schema = fields.Nested(SensorSchema)
    image_processed = fields.Boolean()
    insect_attack_detected = fields.Boolean()


class InferencesSchema(Schema):
    temperature = fields.Nested(SensorSchema)
    light = fields.Nested(SensorSchema)
    humidity = fields.Nested(SensorSchema)
    camera = fields.Nested(CameraSchema)


class SensorGroupSchema(Schema):
    sensor_group = fields.String()
    time_stamp = fields.DateTime(format="iso")
    inferences = fields.Nested(InferencesSchema)