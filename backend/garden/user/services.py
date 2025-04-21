import requests
from rest_framework import serializers
from django.conf import settings


# Deprecated: ZeroBounce is not available
def _validate_email(email):
    url = settings.EMAIL_VALIDATION_API_URL
    params = {
        'api_key': settings.EMAIL_VALIDATION_API_KEY,
        'email': email,
    }
    response = requests.get(url, params)
    if response.status_code != 200:
        raise serializers.ValidationError(f'Failed to validate email with {url}')
    response = response.json()
    return response['status'] == 'valid'


# Currently used with hunter.io
def validate_email(email):
    url = settings.EMAIL_VALIDATION_API_URL
    params = {
        'api_key': settings.EMAIL_VALIDATION_API_KEY,
        'email': email,
    }
    response = requests.get(url, params).json()
    data = response.get('data')
    if not data:
        raise serializers.ValidationError(f'Failed to validate email with {url}')
    status = data.get('status')
    if not status:
        raise serializers.ValidationError(f'Failed to validate email with {url}')
    return status == 'valid'