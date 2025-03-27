from rest_framework import serializers


class ControlPumperSerializer(serializers.Serializer):
    value = serializers.IntegerField()
    timestamp = serializers.DateTimeField(required=False)


    def validate_value(self, value):
        """Ensure value is only 0 or 100."""
        if not (0 <= value <= 100):
            raise serializers.ValidationError('Signal must be between 0 and 100')
        return value