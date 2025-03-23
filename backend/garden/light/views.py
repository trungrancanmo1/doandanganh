from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework import exceptions
from .serializers import LightBoundSerializer
from .models import LightBound

# Create your views here.

class UpdateLightBoundView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LightBoundSerializer
    
    def get_object(self):
        obj, _ = LightBound.objects.get_or_create(user=self.request.user)
        return obj


class RetrieveLightBoundView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LightBoundSerializer
    
    def get_object(self):
        try:
            obj, _ = LightBound.objects.get_or_create(user=self.request.user)
            return obj
        except LightBound.DoesNotExist:
            raise exceptions.NotFound('light bound not found for this user')