from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework import exceptions
from .serializers import HumidityBoundSerializer
from .models import HumidityBound

# Create your views here.

class UpdateHumidityBoundView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = HumidityBoundSerializer
    
    def get_object(self):
        obj, _ = HumidityBound.objects.get_or_create(user=self.request.user)
        return obj


class RetrieveHumidityBoundView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = HumidityBoundSerializer
    
    def get_object(self):
        try:
            obj, _ = HumidityBound.objects.get_or_create(user=self.request.user)
            return obj
        except HumidityBound.DoesNotExist:
            raise exceptions.NotFound('humidity bound not found for this user')