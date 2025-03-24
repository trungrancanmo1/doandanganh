from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

class PlantImage(models.Model):
    timestamp = models.DateTimeField(null=False)
    image = models.ImageField(upload_to='plant_images/')
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