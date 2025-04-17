import requests
from rest_framework import serializers
from django.conf import settings


def validate_email(email):
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