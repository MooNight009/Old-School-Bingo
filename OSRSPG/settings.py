"""
Django settings for OSRSPG project.

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os.path
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ['RDS_SECRET_KEY_DJANGO']

DEBUG = False

# TODO: Remove any unnecessary hosts
ALLOWED_HOSTS = [
    'oldschoolbingo.com',
    'www.oldschoolbingo.com',
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages',

    # For redirecting http to https and website health in aws
    'health_check',
    'health_check.db',
    'health_check.cache',
    'health_check.storage',

    'applications.bingo',
    'applications.invocation',
    'applications.player',
    'applications.submission',
    'applications.team',
    'applications.tile',
    'applications.common',
    'applications.defaults',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # Custom middleware for eb health
    'applications.common.middleware.HealthCheckMiddleware'
]

ROOT_URLCONF = 'OSRSPG.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'OSRSPG.wsgi.application'

# PostgreSQL Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
if 'RDS_DB_NAME' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ['RDS_DB_NAME'],
            'USER': os.environ['RDS_USERNAME'],
            'PASSWORD': os.environ['RDS_PASSWORD'],
            'HOST': os.environ['RDS_HOSTNAME'],
            'PORT': os.environ['RDS_PORT'],
        }
    }

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'
# TODO: Do I need to remove the following two?
USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

print(os.environ)
if 'RDS_USE_S3' in os.environ:  # TODO: Use a better detection method AND combine with database
    # aws settings
    AWS_ACCESS_KEY_ID = os.environ['RDS_AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY = os.environ['RDS_AWS_SECRET_ACCESS_KEY']
    AWS_STORAGE_BUCKET_NAME = os.environ['RDS_AWS_STORAGE_BUCKET_NAME']
    AWS_S3_REGION_NAME = os.environ['RDS_AWS_S3_REGION_NAME']
    AWS_DEFAULT_REGION = os.environ['RDS_AWS_S3_REGION_NAME']  # TODO: Switch to custom var for each region

    AWS_DEFAULT_ACL = 'public-read'

    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}

    # s3 static settings
    STATIC_LOCATION = 'static'
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{STATIC_LOCATION}/'
    STATICFILES_STORAGE = 'applications.defaults.storage_backends.StaticStorage'

    # s3 public media settings
    PUBLIC_MEDIA_LOCATION = 'media'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/'
    DEFAULT_FILE_STORAGE = 'applications.defaults.storage_backends.PublicMediaStorage'
else:
    # TODO: Check if this is necessary or triggered at all
    print('Is line 182 in settings.py triggered?')
    STATIC_ROOT = os.path.join(BASE_DIR, "..", "www", "static")
    STATIC_URL = '/static/'
    STATICFILES_DIRS = [
        BASE_DIR / 'static',
    ]

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Login details
LOGIN_URL = '/login'
LOGIN_REDIRECT_URL = '/'

# Email details
EMAIL_BACKEND = 'django_ses.SESBackend'

# Upload limit
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5 MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5 MB
