from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth import get_user_model

# Create your models here.

class PlantImage(models.Model):
    timestamp = models.DateTimeField(null=False)
    image = CloudinaryField('plant_image')
    annotated_image = CloudinaryField('annotated_plant_image', blank=True, null=True)
    predictions = models.JSONField(blank=True, null=True)
    user = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.CASCADE,
        related_name='plant_image_of',
    )
    
    class Meta:
        ordering = ['user', '-timestamp']
    
    def __str__(self):
        username = self.user.username
        email = self.user.email
        timestamp = self.timestamp
        return f"{username} ({email}): image {self.id} at {timestamp}"