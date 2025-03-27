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
    UpdateHumidityBoundView,
    RetrieveHumidityBoundView,
    SyncMostRecentHumidityRecord,
    RetrieveMostRecentHumidityRecord,
    RetrieveHumidityRecordListView,
    DeleteOldestHumidityRecord,
    ManageHumidityControlModeView,
)

urlpatterns = [
    path('bound/update/', UpdateHumidityBoundView.as_view(), name='humidity_bound_update'),
    path('bound/get/', RetrieveHumidityBoundView.as_view(), name='humidity_bound_retrieve'),
    path('record/sync/', SyncMostRecentHumidityRecord.as_view(), name='most_recent_humidity_sync'),
    path('record/get/recent/', RetrieveMostRecentHumidityRecord.as_view(), name='most_recent_humidity_retrieve'),
    path('record/get/', RetrieveHumidityRecordListView.as_view(), name='humidity_records_retrieve'),
    path('record/delete/', DeleteOldestHumidityRecord.as_view(), name='oldest_humidity_delete'),
    path('control/mode/', ManageHumidityControlModeView.as_view(), name='humidity_control_mode_manage'),
]
