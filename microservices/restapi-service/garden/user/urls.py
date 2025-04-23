"""
URL configuration for garden project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegisterView,
    UserTokenObtainPairView,
    UserProfileView,
    UserAvatarUploadView,
    UpdateUserProfileView,
    RequestPasswordResetView,
    ConfirmPasswordResetView,
)

urlpatterns = [
    path('signup/', RegisterView.as_view(), name='signup'),
    path('login/', UserTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/get/', UserProfileView.as_view(), name='user_profile_retrieve'),
    path('profile/avatar/upload/', UserAvatarUploadView.as_view(), name='user_avatar_upload'),
    path('profile/update/', UpdateUserProfileView.as_view(), name='user_profile_update'),
    path('password/reset/', RequestPasswordResetView.as_view(), name='password_reset_request'),
    path('password/reset/confirm/', ConfirmPasswordResetView.as_view(), name='password_reset_confirm'),
]
