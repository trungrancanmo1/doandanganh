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


import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion
from paho.mqtt.enums import MQTTProtocolVersion
import json


EMQX_USER_NAME='hcmut-smart-farm-data-processing-system'
EMQX_PASSWORD='hcmut-smart-farm'
EMQX_URL='z7f54af0.ala.dedicated.aws.emqxcloud.com'

# Create your views here.

mqtt_client = mqtt.Client(callback_api_version=CallbackAPIVersion.VERSION2, protocol=MQTTProtocolVersion.MQTTv5)
mqtt_client.username_pw_set(username=EMQX_USER_NAME, password=EMQX_PASSWORD)

mqtt_client.connect(EMQX_URL, 1883)
class SignalIlluminatorView(views.APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = IlluminatorControlSerializer(data=request.data)

        if serializer.is_valid():
            value = serializer.validated_data['value']

            topic = '/'.join([request.user.username, 'illuminator'])

            timestamp = timezone.now().isoformat()

            payload = {
                'value' : value,
                'type' : 'illuminator',
                'timestamp': timestamp,
            }

            
            decode = json.dumps(payload).encode('utf-8')

            try:
                mqtt_client.publish(topic=topic, payload=decode, qos=2)
            except Exception as e:
                return Response({
                    'error': 'Failed to publish topic',
                    'detail': str(e),
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            obj = IlluminatorControl.objects.create(value=value, timestamp=timestamp)
            serializer = IlluminatorControlSerializer(obj)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RetrieveIlluminatorSignalView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = IlluminatorControlSerializer
    pagination_class = PageNumberPagination
    
    def get_queryset(self):
        return IlluminatorControl.objects.filter(user=self.request.user)