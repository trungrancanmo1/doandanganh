from datetime import datetime, timezone
from rest_framework import generics, views, status
from rest_framework.permissions import IsAuthenticated
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .serializers import MoistureBoundSerializer, MoistureRecordSerializer, MoistureControlModeSerializer
from .models import MoistureBound, MoistureRecord, MoistureControlMode
from django.conf import settings

from utils import ifdb_client, kafka_producer, USER
from garden.settings import INFLUXDB, KAFKA_TOPIC


# Create your views here.

class UpdateMoistureBoundView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MoistureBoundSerializer
    
    def get_object(self):
        obj, _ = MoistureBound.objects.get_or_create(user=self.request.user)
        # Get data from the user's updated value
        min = self.request.data.get('lowest_allowed')
        # min = min if min else obj.lowest_allowed
        max = self.request.data.get('highest_allowed')
        # max = max if max else obj.highest_allowed
        # obj.lowest_allowed = min
        # obj.highest_allowed = max
        # obj.save()

        # min = obj.lowest_allowed
        # max = obj.highest_allowed

        #===================================
        # KAFKA PRODUCING
        #===================================
        data = {
            'user_id': USER['user_id'],
            'env_id': USER['env_id'],
            'sensor_id': USER['sensor_id'][1],
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'type': USER['sensor_type'][1],
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


class RetrieveMoistureBoundView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MoistureBoundSerializer
    
    def get_object(self):
        try:
            obj, _ = MoistureBound.objects.get_or_create(user=self.request.user)
            return obj
        except MoistureBound.DoesNotExist:
            raise exceptions.NotFound('moisture bound not found for this user')


#==========================
# NOTE: ⛓️‍💥 DEPRECATED
#==========================
class SyncMostRecentMoistureRecord(views.APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        raise exceptions.APIException('This endpoint is deprecated and should not be used.')

        aio_username = settings.AIO_USERNAME
        aio_key = settings.AIO_KEY
        try:
            # Get data recorded on Adafruit feed
            client = get_aio_client(aio_username, aio_key)
            feed = get_or_create_feed(f"{request.user.username}-moisture", client)
            new_data = get_unread_data_from_feed(feed.key, client)
            if not new_data:
                return Response(
                    {'detail': 'No new data available'},
                    status=status.HTTP_204_NO_CONTENT,
                )
            
            # Create object list for model bulk create
            objs = [
                MoistureRecord(
                    timestamp=datetime.fromisoformat(r.created_at.replace('Z', '+00:00')),
                    value=float(r.value),
                    user=request.user,
                )
                for r in new_data
            ]
            moistures = MoistureRecord.objects.bulk_create(objs)
            
            # Return success response attached with new data
            serializer = MoistureRecordSerializer(moistures, many=True)
            return Response(
                {
                    'message': f"Sync up {len(moistures)} moisture records",
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


class RetrieveMostRecentMoistureRecord(views.APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        n = request.query_params.get('n', None)
        if n is not None:
            try:
                n = int(n)
            except ValueError:
                raise exceptions.ValidationError('n must be an integer')
            if n <= 0:
                raise exceptions.ValidationError('n must be positive')
            
        # records = MoistureRecord.objects.filter(user=self.request.user).order_by('-timestamp')
        #===================================
        # INFLUX DATABASE
        #===================================
        query = f'''
        SELECT time as timestamp, value
        FROM 'sensor_data'
        WHERE type = 'humidity'
        ORDER BY time DESC
        LIMIT {int(n)}
        '''

        # if n is not None:
        #     records = records[:n]

        table = ifdb_client.query(query=query, database=INFLUXDB['bucket'])
        data_frame = table.to_pandas()
        data_list = data_frame.to_dict(orient='records')
        #===================================
        # INFLUX DATABASE
        #===================================
        
        return Response(data_list, status=status.HTTP_200_OK)
        if n is not None:
            records = records[:n]
        serializer = MoistureRecordSerializer(records, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# NOTE: ⚠️should not be used (use get/recent instead)
class RetrieveMoistureRecordListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MoistureRecordSerializer
    pagination_class = PageNumberPagination
    
    def get_queryset(self):
        return MoistureRecord.objects.filter(user=self.request.user)


#==========================
# NOTE: ⛓️‍💥 DEPRECATED
#==========================
class DeleteOldestMoistureRecord(views.APIView):
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
        records = MoistureRecord.objects.filter(user=request.user).order_by('timestamp')
        if n is not None:
            records = records[:n]
        count = records.count()
        
        for record in records:
            record.delete()
        
        return Response(
            {'message': f"Deleted {count} oldest records"},
            status=status.HTTP_200_OK,
        )


class ManageMoistureControlModeView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MoistureControlModeSerializer
    
    def get_object(self):
        obj, _ = MoistureControlMode.objects.get_or_create(user=self.request.user)
        return obj