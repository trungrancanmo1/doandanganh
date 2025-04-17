"""
Django settings for garden project.

Generated by 'django-admin startproject' using Django 5.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

import os
import cloudinary

from dotenv import load_dotenv
from pathlib import Path
from datetime import timedelta

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJ_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG_MODE') == 'True'

ALLOWED_HOSTS = ['doandanganh.onrender.com', 'localhost']



# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    
    'django.contrib.staticfiles',
    'cloudinary',
    'cloudinary_storage',
    
    'rest_framework',
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',
    
    'api',
    'garden',
    'notification',
    'overview',
    'temperature',
    'humidity',
    'moisture',
    'light',
    'pest',
    'user',
    
    'illuminator',

    'utils'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    
    'corsheaders.middleware.CorsMiddleware',
    
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'garden.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'garden.wsgi.application'

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=7 * 24 * 60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=30),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": False,

    "ALGORITHM": "HS256",
    "VERIFYING_KEY": "",
    "AUDIENCE": None,
    "ISSUER": None,
    "JSON_ENCODER": None,
    "JWK_URL": None,
    "LEEWAY": 0,

    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",

    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",

    "JTI_CLAIM": "jti",

    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),

    "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
    "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
    "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
    "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",
}


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASS'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_POST'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Email validation

EMAIL_VALIDATION_API_URL = os.getenv('EMAIL_VALIDATION_API_URL')
EMAIL_VALIDATION_API_KEY = os.getenv('EMAIL_VALIDATION_API_KEY')


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

MEDIA_URL = '/media/'

CLOUDINARY_STORAGE = {
    'CLOUD_NAME':os.getenv('CD_CLOUD_NAME'),
    'API_KEY': os.getenv('CD_API_KEY'),
    'API_SECRET': os.getenv('CD_API_SECRET'),
}

cloudinary.config(
    cloud_name=os.getenv('CD_CLOUD_NAME'),
    api_key=os.getenv('CD_API_KEY'),
    api_secret=os.getenv('CD_API_SECRET'),
)

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


CORS_ALLOW_ALL_ORIGINS = True   # Temporarily allow all origins
AUTH_USER_MODEL = 'user.User'

AIO_USERNAME = os.getenv('AIO_USERNAME')
AIO_KEY      = os.getenv('AIO_KEY')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

FRONTEND_URL = os.getenv('FRONTEND_URL')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


#==========================
# INFLUX DATABASE
#==========================
INFLUXDB = {
    "host": "https://eu-central-1-1.aws.cloud2.influxdata.com",  # Change to your InfluxDB host
    "token": os.getenv('INFLUXDB_TOKEN'),
    "org": "hcmut-student",
    "bucket": "hcmut-smart-farm",
}
MEASUREMENT = 'actuator_data'


#==========================
# 💀💀💀💀💀💀💀💀💀💀
# 💀🚫🚫🚫🚫🚫🚫🚫🚫💀
# 💀💀💀💀💀💀💀💀💀💀
# ASSUME THERE IS ONE USER
#==========================
APP_NAME        ='hcmut-smart-farm'
USER = {
    'user_id' : 'VVRsnPoAEqSbUa9QLwXLgj2D9Zx2',
    'env_id' : 'my_simple_garden',
    'sensor_id' : [
        'sensor-101',
        'sensor-102',
        'sensor-103'
    ],
    'actuator_id' : [
        'actuator-101',
        'actuator-102',
        'actuator-103',
        'actuator-104'
    ],
    'sensor_type' : [
        'temperature',
        'humidity',
        'light'
    ],
    'actuator_type' : [
        'fan',
        'pump',
        'light',
        'heater'
    ],
}

TOPIC_TYPE = [
    'command',
    'data',
    'status'
]


#==========================
# MQTT BROKER INFO
#==========================
MQTT_BROKER = {
    'username' : os.getenv('EMQX_USER_NAME'),
    'password' : os.getenv('EMQX_PASSWORD'),
    'url' : os.getenv('EMQX_URL')
}


#==========================
# KAFKA BROKER
#==========================
KAFKA_BROKER = os.getenv('KAFKA_BROKER')
KAFKA_TOPIC  = os.getenv('KAFKA_TOPIC')
KAFKA_ENCODE = os.getenv('KAFKA_ENCODE')

#==========================
# OBJECT DETECTION WORKFLOW
#==========================
OBJDET_API_URL = os.getenv('OBJDET_API_URL')
OBJDET_API_KEY = os.getenv('OBJDET_API_KEY')
OBJDET_WORKSPACE = os.getenv('OBJDET_WORKSPACE')
OBJDET_WORKFLOW = os.getenv('OBJDET_WORKFLOW')
