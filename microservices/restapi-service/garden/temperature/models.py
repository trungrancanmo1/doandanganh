from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

class TemperatureBound(models.Model):
    lowest_allowed = models.FloatField(default=0)
    highest_allowed = models.FloatField(default=0)
    user = models.OneToOneField(
        to=get_user_model(),
        on_delete=models.CASCADE,
        related_name='temperature_bound_of',
    )
    
    def __str__(self):
        username = self.user.username
        email = self.user.email
        highest = self.highest_allowed
        lowest = self.lowest_allowed
        return f"{username} ({email}): from {lowest} to {highest}"


class TemperatureRecord(models.Model):
    timestamp = models.DateTimeField(null=False)
    value = models.FloatField(null=False)
    user = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.CASCADE,
        related_name='temperature_record_of',
    )
    
    class Meta:
        ordering = ['user', '-timestamp']
    
    def __str__(self):
        username = self.user.username
        email = self.user.email
        timestamp = self.timestamp
        value = self.value
        return f"{username} ({email}): record {value} at {timestamp}"


class TemperatureControlMode(models.Model):
    manual = models.BooleanField(default=True)
    user = models.OneToOneField(
        to=get_user_model(),
        on_delete=models.CASCADE,
        related_name='temperature_control_mode_of',
    )
    
    def __str__(self):
        username = self.user.username
        email = self.user.email
        return f"{username} ({email}): {'manual' if self.manual else 'automatic'} control"