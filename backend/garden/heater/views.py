from django.shortcuts import render

# Create your views here.
from django.utils import timezone
from rest_framework import generics, views, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .serializers import ControlHeaterSerializer


from garden.settings import USER, MEASUREMENT, INFLUXDB
from utils import make_topic, send_command, ifdb_client

from influxdb_client_3 import Point


import json

# Create your views here.
#===================================
# INFLUX DATABASE ADDED
# 👌👌👌👌👌
#===================================
class ControlHeaterView(views.APIView):
    permission_classes = [IsAuthenticated]


    def post(self, request):
        serializer = ControlHeaterSerializer(data=request.data)

        if serializer.is_valid():
            value = serializer.validated_data['value']
            timestamp = timezone.localtime().isoformat()

            # 1. prepare the payload
            payload = {
                'user_id' : USER['user_id'],
                'env_id' : USER['env_id'],
                'actuator_id' : 'actuator-104',
                'timestamp' : timestamp,
                'type' : 'heater',
                'value' : float(value)
            }

            # 2. encode the payload
            decoded = json.dumps(payload).encode('utf-8')

            # 3. publish the payload and persist to influxdb
            #   - publish the payload
            topic = make_topic(payload['actuator_id'], 'command', payload['type'])
            send_command(decoded, topic=topic)
            #   - persist to the database
            point = (
                        Point(MEASUREMENT) 
                        .tag(key='user_id', value=payload['user_id']) 
                        .tag(key='env_id', value=payload['env_id'])
                        .tag(key='actuator_id', value=payload['actuator_id'])
                        .tag(key='type', value=payload['type'])
                        .field(field='value', value=payload['value'])
                        .time(time=payload['timestamp'])
                    )
            
            ifdb_client.write(database=INFLUXDB['bucket'], record=point)

            # response
            response = {
                'value' : value,
                'timestamp' : timestamp
            }

            return Response(data=response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#===================================
# INFLUX DATABASE ADDED
# 👌👌👌👌👌
#===================================
class GetHeaterHistoryView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ControlHeaterSerializer
    pagination_class = PageNumberPagination
    
    def get_queryset(self):

        #===================================
        # INFLUX DATABASE
        #===================================
        query = f'''
        SELECT time as timestamp, value
        FROM 'actuator_data'
        WHERE 
        type = 'heater'
        AND
        TIME > now() - interval '1 day'
        ORDER BY time DESC
        '''

        table = ifdb_client.query(query=query, database=INFLUXDB['bucket'])
        data_frame = table.to_pandas()
        data_list = data_frame.to_dict(orient='records')
        #===================================
        # INFLUX DATABASE
        #===================================
        return data_list