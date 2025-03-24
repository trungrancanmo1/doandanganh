from django.contrib import admin
from .models import TemperatureBound, TemperatureRecord

# Register your models here.
admin.site.register(TemperatureBound)
admin.site.register(TemperatureRecord)