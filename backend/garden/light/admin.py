from django.contrib import admin
from .models import LightBound, LightRecord, LightControlMode

# Register your models here.
admin.site.register(LightBound)
admin.site.register(LightRecord)
admin.site.register(LightControlMode)