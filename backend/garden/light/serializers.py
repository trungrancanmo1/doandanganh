from rest_framework import serializers
from .models import LightBound, LightRecord


class LightBoundSerializer(serializers.ModelSerializer):
    class Meta:
        model = LightBound
        fields = ['lowest_allowed', 'highest_allowed']
    
    def validate_lowest_allowed(self, value):
        if value < 0:
            raise serializers.ValidationError('Light unit cannot be negative')
        return value

    def validate_highest_allowed(self, value):
        if value < 0:
            raise serializers.ValidationError('Light unit cannot be negative')
        return value
    
    def validate(self, data):
        lowest_allowed = data.get('lowest_allowed')
        highest_allowed = data.get('highest_allowed')
        
        if not lowest_allowed or not highest_allowed:
            return data
        
        if lowest_allowed > highest_allowed:
            raise serializers.ValidationError({'highest_allowed' : 'Upper bound cannot be lower than lower bound'})
        return data


class LightRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = LightRecord
        fields = ['timestamp', 'value']
    
    def validate_value(self, value):
        if value < 0:
            raise serializers.ValidationError('Light unit cannot be negative')
        return value