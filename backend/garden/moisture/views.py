from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework import exceptions
from .serializers import MoistureBoundSerializer
from .models import MoistureBound

# Create your views here.

class UpdateMoistureBoundView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MoistureBoundSerializer
    
    def get_object(self):
        obj, _ = MoistureBound.objects.get_or_create(user=self.request.user)
        return obj


class RetrieveMoistureBoundView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MoistureBoundSerializer
    
    def get_object(self):
        try:
            obj, _ = MoistureBound.objects.get_or_create(user=self.request.user)
            return obj
        except MoistureBound.DoesNotExist:
            raise exceptions.NotFound('moisture bound not found for this user')