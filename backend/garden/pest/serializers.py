from rest_framework import serializers
from .models import PlantImage


class PlantImageSerializer(serializers.ModelSerializer):
    image = serializers.CharField(source='image.url', read_only=True)
    annotated_image = serializers.CharField(source='annotated_image.url', read_only=True, default=None)
    
    class Meta:
        model = PlantImage
        fields = ['id', 'image', 'annotated_image', 'predictions', 'timestamp']


class UploadPlantImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantImage
        fields = ['id', 'image', 'timestamp']