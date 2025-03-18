'''
    - 
'''
from rest_framework.views import APIView
from rest_framework.response import Response


class OverviewView(APIView):
    def get(self, request, format=None):
        return Response({'message': 'data'}, status=200)