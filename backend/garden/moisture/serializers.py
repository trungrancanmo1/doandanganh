from rest_framework import serializers
from .models import MoistureBound, MoistureRecord, MoistureControlMode


class MoistureBoundSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoistureBound
        fields = ['lowest_allowed', 'highest_allowed']
    
    def validate_lowest_allowed(self, value):
        if value < 0 or value > 100:
            raise serializers.ValidationError('Moisture must lie between 0 and 100')
        return value

    def validate_highest_allowed(self, value):
        if value < 0 or value > 100:
            raise serializers.ValidationError('Moisture must lie between 0 and 100')
        return value
    
    def validate(self, data):
        lowest_allowed = data.get('lowest_allowed')
        highest_allowed = data.get('highest_allowed')
        
        if not lowest_allowed or not highest_allowed:
            return data
        
        if lowest_allowed > highest_allowed:
            raise serializers.ValidationError({'highest_allowed' : 'Upper bound cannot be lower than lower bound'})
        return data


class MoistureRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoistureRecord
        fields = ['timestamp', 'value']
    
    def validate_value(self, value):
        if value < 0 or value > 100:
            raise serializers.ValidationError('Moisture must lie between 0 and 100')
        return value


class MoistureControlModeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoistureControlMode
        fields = ['manual']