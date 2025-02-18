"""
Django settings for <project name> project.

Generated by 'django-admin startproject' using Django 3.0.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import dj_database_url
import os

from django.utils.module_loading import import_string

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'xv9xt@2tan9p%i-#8r5d_w5i77@)ev66u47sv!_mu1-8tgz9b*'
SECRET_KEY = os.environ.get('SECRET_KEY', default='your secret key')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = 'RENDER' not in os.environ

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
]

RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
   ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

ENV_KEY_PROD = 'production'
ENV_KEY_DEV = 'development'
ENV = os.environ.get('ENVIRONMENT', ENV_KEY_DEV)
# if ENV != ENV_KEY_PROD:
#     ENV = ENV_KEY_DEV

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',

    'accounts',
    'proxy',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    # # See middleware class at https://pypi.org/project/django-cors-headers/
    # 'corsheaders.middleware.CorsPostCsrfMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = '<project name>.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

LOGIN_REDIRECT_URL = 'index'
LOGOUT_REDIRECT_URL = 'index'

WSGI_APPLICATION = '<project name>.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
}

if ENV == ENV_KEY_PROD:
    DATABASES['default'] = dj_database_url.config(
       # Feel free to alter this value to suit your needs.
       default='postgresql://postgres:postgres@localhost:5432/<project name>',
       conn_max_age=600
    )


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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

AUTH_USER_MODEL = 'accounts.User'


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

if not DEBUG:
   # Tell Django to copy statics to the `staticfiles` directory
   # in your application directory on Render.
   STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

   # Turn on WhiteNoise storage backend that takes care of compressing static files
   # and creating unique names for each version so they can safely be cached forever.
   STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# CORS + CSRF

# If CORS_REPLACE_HTTPS_REFERER is True, CorsMiddleware will change the Referer header
# to something that will pass Django’s CSRF checks whenever the CORS checks pass
# CORS_REPLACE_HTTPS_REFERER = True
CORS_ALLOW_ALL_ORIGINS = True

# CORS_ORIGIN_WHITELIST = [
#     'http://localhost:8000',
#     # 'http://localhost:3000',
#     # 'https://flight-search-frontend.onrender.com/',
# ]

# CSRF_TRUSTED_ORIGINS = [
#     'localhost:8000',
#     # 'localhost:3000',
#     # 'https://flight-search-frontend.onrender.com/',
# ]


# Django REST Framework

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'NO_CSRF_AUTHENTICATION_CLASSES': (
        'accounts.utils.CsrfExemptSessionAuth',
        'rest_framework.authentication.TokenAuthentication',
    )
}

NO_CSRF_AUTH_CLASSES = tuple([
    import_string(path)
    for path in REST_FRAMEWORK['NO_CSRF_AUTHENTICATION_CLASSES']
])
