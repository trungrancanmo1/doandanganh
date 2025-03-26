from django.utils import timezone
from rest_framework import generics, views, status
from rest_framework.permissions import IsAuthenticated
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .serializers import IlluminatorControlSerializer
from .models import IlluminatorControl
from django.conf import settings

from aio_helper.client import get_aio_client
from aio_helper.feed import get_or_create_feed
from aio_helper.data import get_unread_data_from_feed

# Create your views here.

class SignalIlluminatorView(views.APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = IlluminatorControlSerializer(data=request.data)
        if serializer.is_valid():
            aio_username = settings.AIO_USERNAME
            aio_key = settings.AIO_KEY
            try:
                client = get_aio_client(aio_username, aio_key)
                feed = get_or_create_feed(f"{request.user.username}-illuminator", client) 
                signal = serializer.validated_data['value']
                data = client.send_data(feed.key, float(signal))
                obj = IlluminatorControl.objects.create(value=data.value, timestamp=data.created_at, user=request.user)
            except Exception as e:
                return Response(
                    {
                        'error': 'Failed to send data to Adafruit IO',
                        'detail': str(e),
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
            serializer = IlluminatorControlSerializer(obj)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RetrieveIlluminatorSignalView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = IlluminatorControlSerializer
    pagination_class = PageNumberPagination
    
    def get_queryset(self):
        return IlluminatorControl.objects.filter(user=self.request.user)