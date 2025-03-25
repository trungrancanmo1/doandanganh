from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from rest_framework import generics, views, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import (
    RegisterSerializer,
    UserSerializer,
    UserTokenObtainPairSerializer,
    UserAvatarUploadSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
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


class UpdateUserProfileView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = User.objects.all()
    
    def get_object(self):
        return self.request.user


class RequestPasswordResetView(views.APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.get(email=email)
            
            refresh = RefreshToken.for_user(user)
            reset_token = str(refresh.access_token)
            reset_link = f"{settings.FRONTEND_URL}/reset-password/{reset_token}"
            
            html_content = render_to_string('mails/password_reset_mail.html', {
                'user': user,
                'reset_link': reset_link,
            })
            
            emsg = EmailMultiAlternatives(
                subject='Yêu cầu thay đổi mật khẩu Smart Sprout',
                body=f"Vui lòng nhấp chuột đường liên kết bên dưới để đổi mật khẩu: {reset_link}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[user.email],
            )
            emsg.attach_alternative(html_content, 'text/html')
            
            try:
                emsg.send()
            except Exception as e:
                return Response({'detail': str(e)}, status=status.HTTP_502_BAD_GATEWAY)
            return Response({'detail': 'Send password reset mail successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConfirmPasswordResetView(views.APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        