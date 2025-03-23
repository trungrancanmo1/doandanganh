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
from .views import (
    UpdateLightBoundView,
    RetrieveLightBoundView,
    SyncMostRecentLightRecord,
    RetrieveMostRecentLightRecord,
)

urlpatterns = [
    path('bound/update/', UpdateLightBoundView.as_view(), name='light_bound_update'),
    path('bound/get/', RetrieveLightBoundView.as_view(), name='light_bound_retrieve'),
    path('record/sync/', SyncMostRecentLightRecord.as_view(), name='most_recent_light_sync'),
    path('record/get/', RetrieveMostRecentLightRecord.as_view(), name='most_recent_light_retrieve'),
]
