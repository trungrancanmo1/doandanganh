from django.contrib import admin
from .models import HumidityBound, HumidityRecord

# Register your models here.
admin.site.register(HumidityBound)
admin.site.register(HumidityRecord)