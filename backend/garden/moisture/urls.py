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
    UpdateMoistureBoundView,
    RetrieveMoistureBoundView,
    SyncMostRecentMoistureRecord,
    RetrieveMostRecentMoistureRecord,
    RetrieveMoistureRecordListView,
    DeleteOldestMoistureRecord,
    ManageMoistureControlModeView,
)

urlpatterns = [
    path('bound/update/', UpdateMoistureBoundView.as_view(), name='moisture_bound_update'),
    path('bound/get/', RetrieveMoistureBoundView.as_view(), name='moisture_bound_retrieve'),
    path('record/sync/', SyncMostRecentMoistureRecord.as_view(), name='most_recent_moisture_sync'),
    path('record/get/recent/', RetrieveMostRecentMoistureRecord.as_view(), name='most_recent_moisture_retrieve'),
    path('record/get/', RetrieveMoistureRecordListView.as_view(), name='moisture_records_retrieve'),
    path('record/delete/', DeleteOldestMoistureRecord.as_view(), name='oldest_moisture_delete'),
    path('control/mode/', ManageMoistureControlModeView.as_view(), name='moisture_control_mode_manage'),
]
