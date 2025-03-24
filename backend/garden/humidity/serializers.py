from rest_framework import serializers
from .models import HumidityBound, HumidityRecord


class HumidityBoundSerializer(serializers.ModelSerializer):
    class Meta:
        model = HumidityBound
        fields = ['lowest_allowed', 'highest_allowed']
    
    def validate_lowest_allowed(self, value):
        if value < 0 or value > 100:
            raise serializers.ValidationError('Humidity must lie between 0 and 100')
        return value

    def validate_highest_allowed(self, value):
        if value < 0 or value > 100:
            raise serializers.ValidationError('Humidity must lie between 0 and 100')
        return value
    
    def validate(self, data):
        lowest_allowed = data.get('lowest_allowed')
        highest_allowed = data.get('highest_allowed')
        
        if not lowest_allowed or not highest_allowed:
            return data
        
        if lowest_allowed > highest_allowed:
            raise serializers.ValidationError({'highest_allowed' : 'Upper bound cannot be lower than lower bound'})
        return data


class HumidityRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = HumidityRecord
        fields = ['timestamp', 'value']
    
    def validate_value(self, value):
        if value < 0 or value > 100:
            raise serializers.ValidationError('Humidity must lie between 0 and 100')
        return value