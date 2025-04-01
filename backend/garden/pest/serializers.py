from rest_framework import serializers
from .models import PlantImage


class PlantImageSerializer(serializers.ModelSerializer):
    image = serializers.CharField(source='image.url', read_only=True)
    
    class Meta:
        model = PlantImage
        fields = ['id', 'image', 'timestamp']


class UploadPlantImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantImage
        fields = ['id', 'image', 'timestamp']