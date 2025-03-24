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
    UpdateTemperatureBoundView,
    RetrieveTemperatureBoundView,
    RetrieveMostRecentTemperatureRecord,
    RetrieveTemperatureRecordListView,
    SyncMostRecentTemperatureRecord,
    DeleteOldestTemperatureRecord,
)

urlpatterns = [
    path('bound/update/', UpdateTemperatureBoundView.as_view(), name='temperature_bound_update'),
    path('bound/get/', RetrieveTemperatureBoundView.as_view(), name='temperature_bound_retrieve'),
    path('record/get/recent/', RetrieveMostRecentTemperatureRecord.as_view(), name='most_recent_temperature_retrieve'),
    path('record/get/', RetrieveTemperatureRecordListView.as_view(), name='temperature_records_retrieve'),
    path('record/sync/', SyncMostRecentTemperatureRecord.as_view(), name='most_recent_temperature_sync'),
    path('record/delete/', DeleteOldestTemperatureRecord.as_view(), name='oldest_temperature_delete'),
]
