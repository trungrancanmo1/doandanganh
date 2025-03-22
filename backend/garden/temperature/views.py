from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework import exceptions
from .serializers import TemperatureBoundSerializer
from .models import TemperatureBound


# Create your views here.

class UpdateTemperatureBoundView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TemperatureBoundSerializer
    
    def get_object(self):
        obj, _ = TemperatureBound.objects.get_or_create(user=self.request.user)
        return obj


class RetrieveTemperatureBoundView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TemperatureBoundSerializer
    
    def get_object(self):
        try:
            obj, _ = TemperatureBound.objects.get_or_create(user=self.request.user)
            return obj
        except TemperatureBound.DoesNotExist:
            raise exceptions.NotFound('temperature bound not found for this user')
    
    