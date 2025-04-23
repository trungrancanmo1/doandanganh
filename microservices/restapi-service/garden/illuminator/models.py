from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

# Create your models here.

class IlluminatorControl(models.Model):
    timestamp = models.DateTimeField(null=False)
    value = models.FloatField(null=False)
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='illuminator_control_of',
    )
    
    class Meta:
        ordering = ['user', '-timestamp']
    
    def __str__(self):
        username = self.user.username
        email = self.user.email
        timestamp = self.timestamp
        value = self.value
        return f"{username} ({email}): signal {value} at {timestamp}"