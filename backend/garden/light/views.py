from datetime import datetime, timezone
from rest_framework import generics, views, status
from rest_framework.permissions import IsAuthenticated
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .serializers import LightBoundSerializer, LightRecordSerializer, LightControlModeSerializer
from .models import LightBound, LightRecord, LightControlMode
from django.conf import settings

from utils import ifdb_client, kafka_producer
from garden.settings import INFLUXDB, USER, KAFKA_TOPIC
import pandas as pd

# Create your views here.

class UpdateLightBoundView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LightBoundSerializer
    
    def get_object(self):
        obj, _ = LightBound.objects.get_or_create(user=self.request.user)

        min = obj.lowest_allowed
        max = obj.highest_allowed

        #===================================
        # KAFKA PRODUCING
        #===================================
        data = {
            'user_id': USER['user_id'],
            'env_id': USER['env_id'],
            'sensor_id': USER['sensor_id'][2],
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'type': USER['sensor_type'][2],
            'max' : max,
            'min' : min,
            'mail' : USER['email']
            }

        key = '/'.join(
            [
                data['user_id'],
                data['env_id'],
                data['sensor_id']
            ]
        )

        kafka_producer.send(
            topic=KAFKA_TOPIC,
            value=data,
            key=key,
            # headers='',
            # partition='',
            # timestamp_ms=''
        )

        kafka_producer.flush()

        # logger.info('Produced a threshold configuration for the temperature')

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


#==========================
# NOTE: ⛓️‍💥 DEPRECATED
#==========================
class SyncMostRecentLightRecord(views.APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        raise exceptions.APIException('This endpoint is deprecated and should not be used.')

        aio_username = settings.AIO_USERNAME
        aio_key = settings.AIO_KEY
        try:
            # Get data recorded on Adafruit feed
            client = get_aio_client(aio_username, aio_key)
            feed = get_or_create_feed(f"{request.user.username}-light", client)
            new_data = get_unread_data_from_feed(feed.key, client)
            if not new_data:
                return Response(
                    {'detail': 'No new data available'},
                    status=status.HTTP_204_NO_CONTENT,
                )
            
            # Create object list for model bulk create
            objs = [
                LightRecord(
                    timestamp=datetime.fromisoformat(r.created_at.replace('Z', '+00:00')),
                    value=float(r.value),
                    user=request.user,
                )
                for r in new_data
            ]
            lights = LightRecord.objects.bulk_create(objs)
            
            # Return success response attached with new data
            serializer = LightRecordSerializer(lights, many=True)
            return Response(
                {
                    'message': f"Sync up {len(lights)} light records",
                    'data': serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response(
                {
                    'error': 'Failed to fetch data from Adafruit IO',
                    'detail': str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


#===================================
# INFLUX DATABASE ADDED
#===================================
class RetrieveMostRecentLightRecord(views.APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        n = request.query_params.get('n', None)
        # NOTE: SHOULD USE marshmallow
        if n is not None:
            try:
                n = int(n)
            except ValueError:
                raise exceptions.ValidationError('n must be an integer')
            if n <= 0:
                raise exceptions.ValidationError('n must be positive')
            
        # records = LightRecord.objects.filter(user=self.request.user).order_by('-timestamp')
        # if n is not None:
        #     records = records[:n]

        #===================================
        # INFLUX DATABASE
        #===================================
        query = f'''
        SELECT time as timestamp, value
        FROM 'sensor_data'
        WHERE type = 'light'
        ORDER BY time DESC
        LIMIT {int(n)}
        '''

        table = ifdb_client.query(query=query, database=INFLUXDB['bucket'])
        data_frame = table.to_pandas()
        data_list = data_frame.to_dict(orient='records')
        
        return Response(data_list, status=status.HTTP_200_OK)
        #===================================
        # INFLUX DATABASE
        #===================================

        serializer = LightRecordSerializer(records, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# NOTE: ⚠️should not be used (use get/recent instead)
class RetrieveLightRecordListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LightRecordSerializer
    pagination_class = PageNumberPagination
    
    def get_queryset(self):

        return LightRecord.objects.filter(user=self.request.user)


# NOTE: InfluxDB has its own retention policy
class DeleteOldestLightRecord(views.APIView):
    permission_classes = [IsAuthenticated]
    
    def delete(self, request):
        n = request.query_params.get('n', None)
        if n is not None:
            try:
                n = int(n)
            except ValueError:
                raise exceptions.ValidationError('n must be an integer')
            if n <= 0:
                raise exceptions.ValidationError('n must be positive')
        records = LightRecord.objects.filter(user=request.user).order_by('timestamp')
        if n is not None:
            records = records[:n]
        count = records.count()
        
        for record in records:
            record.delete()
        
        return Response(
            {'message': f"Deleted {count} oldest records"},
            status=status.HTTP_200_OK,
        )


class ManageLightControlModeView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LightControlModeSerializer
    
    def get_object(self):
        obj, _ = LightControlMode.objects.get_or_create(user=self.request.user)
        return obj