'''
    - Rest API expose
'''
from rest_framework.views import APIView
from rest_framework.response import Response
from firebase import firestore_db


class LightView(APIView):
    def get(self, request, format=None):
        return Response({'message': 'data'}, status=200)