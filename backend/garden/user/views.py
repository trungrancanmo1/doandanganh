from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import (
    RegisterSerializer,
    UserSerializer,
    UserTokenObtainPairSerializer,
    UserAvatarUploadSerializer,
)

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer


class UserTokenObtainPairView(TokenObtainPairView):
    serializer_class = UserTokenObtainPairSerializer


class UserProfileView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = User.objects.all()
    
    def get_object(self):
        return self.request.user


class UserAvatarUploadView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserAvatarUploadSerializer
    parser_classes = [MultiPartParser, FormParser]
    queryset = User.objects.all()
    
    def get_object(self):
        return self.request.user
