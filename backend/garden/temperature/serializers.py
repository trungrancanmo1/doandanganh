from rest_framework import serializers
from .models import TemperatureBound, TemperatureRecord, TemperatureControlMode

ABSOLUTE_ZERO_IN_CELCIUS = -273.15


class TemperatureBoundSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemperatureBound
        fields = ['lowest_allowed', 'highest_allowed']
    
    def validate_lowest_allowed(self, value):
        if value < ABSOLUTE_ZERO_IN_CELCIUS:
            raise serializers.ValidationError('Temperature cannot be lower than absolute zero')
        return value

    def validate_highest_allowed(self, value):
        if value < ABSOLUTE_ZERO_IN_CELCIUS:
            raise serializers.ValidationError('Temperature cannot be lower than absolute zero')
        return value
    
    def validate(self, data):
        lowest_allowed = data.get('lowest_allowed')
        highest_allowed = data.get('highest_allowed')
        
        if not lowest_allowed or not highest_allowed:
            return data
        
        if lowest_allowed > highest_allowed:
            raise serializers.ValidationError({'highest_allowed' : 'Upper bound cannot be lower than lower bound'})
        return data


class TemperatureRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemperatureRecord
        fields = ['timestamp', 'value']
    
    def validate_value(self, value):
        if value < ABSOLUTE_ZERO_IN_CELCIUS:
            raise serializers.ValidationError('Temperature cannot be lower than absolute zero')
        return value


class TemperatureControlModeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemperatureControlMode
        fields = ['manual']