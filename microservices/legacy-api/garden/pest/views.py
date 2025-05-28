from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.pagination import PageNumberPagination
from .models import PlantImage
from .serializers import PlantImageSerializer, UploadPlantImageSerializer

# Create your views here.

class UploadPlantImageView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = PlantImage.objects.all()
    serializer_class = UploadPlantImageSerializer
    parser_classes = (MultiPartParser, FormParser)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RetrievePlantImageListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PlantImageSerializer
    pagination_class = PageNumberPagination
    
    def get_queryset(self):
        return PlantImage.objects.filter(user=self.request.user)