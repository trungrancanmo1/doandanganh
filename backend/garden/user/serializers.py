from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import AccessToken
from user.services import validate_email

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.CharField(source='avatar.url', read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'avatar']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['email', 'password', 'username', 'first_name', 'last_name']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError('Email is required and can not be empty')
        if not validate_email(str(value)):
            raise serializers.ValidationError('Email is not valid')
        return value


class UserTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['username'] = user.username
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        return token


class UserAvatarUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['avatar']

    def validate_avatar(self, value):
        if not value:
            raise serializers.ValidationError('Avatar is required and can not be empty')
        return value


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'avatar']
        read_only_fields = ['id', 'email', 'username']


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError('User with this email does not exist')
        return value


class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True, min_length=6)
    
    def validate(self, data):
        token = data.get('token')
        try:
            decoded = AccessToken(token)
            user_id = decoded['user_id']
            user = User.objects.get(id=user_id)
            data['user'] = user
        except Exception as e:
            raise serializers.ValidationError({'detail': str(e)})
        return data
        
    def save(self):
        user = self.validated_data['user']
        user.set_password(self.validated_data['password'])
        user.save()