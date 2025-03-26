from rest_framework import serializers
from .models import IlluminatorControl


class IlluminatorControlSerializer(serializers.ModelSerializer):
    class Meta:
        model = IlluminatorControl
        fields = ['value', 'timestamp']
        extra_kwargs = {
            'timestamp': { 'required': False },
        }
    
    def validate_value(self, value):
        if value not in [0, 1]:
            raise serializers.ValidationError('Signal can only be 0 or 1')
        return value