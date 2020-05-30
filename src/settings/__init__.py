"""
Django settings.

Generated by 'django-admin startproject' using Django 3.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
from corsheaders.defaults import default_headers
import cloudinary

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']
# CORS
CORS_ORIGIN_WHITELIST = ["http://127.0.0.1:5000", "http://localhost:5000"]
CORS_ALLOW_HEADERS = default_headers + ('if-modified-since', 'if-none-match',
                                        'cache-control')
CORS_ALLOW_CREDENTIALS = True

AUTH_USER_MODEL = 'user.User'
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third Party apps
    'rest_framework',
    'corsheaders',
    'cloudinary',

    # Apps
    'src.apps.core.apps.CoreConfig',
    'src.apps.image.apps.ImageConfig',
    'src.apps.home.apps.HomeConfig',
    'src.apps.user.apps.UserConfig',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'src.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, '../templates')],
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

WSGI_APPLICATION = 'src.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': os.environ.get('DB_HOST'),
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASS'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
        'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, '../static')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'staticfiles')]

FILE_UPLOAD_HANDLERS = (
    "django.core.files.uploadhandler.TemporaryFileUploadHandler", )

ALLOWED_FILE_TYPES = ('PNG', 'png', 'jpg', 'jpeg', 'JPEG')
MAX_IMAGE_SIZE = 5 * 1024 * 1024

# REST FRAMEWORK CONFIGS
# https://www.django-rest-framework.org/
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES':
    ('rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly', ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES':
    ('djangorestframework_camel_case.render.CamelCaseJSONRenderer', ),
    'DEFAULT_PARSER_CLASSES': (
        'djangorestframework_camel_case.parser.CamelCaseFormParser',
        'djangorestframework_camel_case.parser.CamelCaseMultiPartParser',
        'djangorestframework_camel_case.parser.CamelCaseJSONParser',
    ),
}

cloudinary.config(cloud_name=os.environ.get('CLOUDINARY_NAME'),
                  api_key=os.environ.get('CLOUDINARY_KEY'),
                  api_secret=os.environ.get('CLOUDINARY_SECRET'))

CLOUDINARY_DEFAULT_TAGS = ["thefreezarnigeria"]
CLOUDINARY_FOLDER = "thefreezarnigeria"

# Celery related settings
RABBITMQ_HOST = os.environ.get('RABBITMQ_HOST')
RABBITMQ_USER = os.environ.get('RABBITMQ_USER')
RABBITMQ_PWD = os.environ.get('RABBITMQ_PWD')
RABBITMQ_VHOST = os.environ.get('RABBITMQ_VHOST')
RABBITMQ_PORT = os.environ.get('RABBITMQ_PORT', 5672)
BROKER_URL = 'amqp://' + RABBITMQ_USER + ':' + RABBITMQ_PWD + '@' + \
             RABBITMQ_HOST + ':' + RABBITMQ_PORT + '/' + RABBITMQ_VHOST

CELERY_BROKER_URL = os.getenv('RABBITMQ_URL', BROKER_URL)
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
