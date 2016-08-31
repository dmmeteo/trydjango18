"""
Django settings for rss_agregator project.

Generated by 'django-admin startproject' using Django 1.8.14.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'my!)g1v$-d5y91=fdkbl=36k2!t^t52*bszts%kz$zcfdx%mz1'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    # third party apps
    'crispy_forms',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
    'disqus',
    'django_couch',
    # my apps
    'aggregator',
    'blog',
    'filters'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'rss_aggregator.urls'

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
                'django.contrib.messages.context_processors.messages'
            ],
        },
    },
]

WSGI_APPLICATION = 'rss_aggregator.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'rss',
        'USER': 'vkrilasov',
        'PASSWORD': ''
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'EET'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static_root')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

# Additional configuration starts here.

# Crispy forms settings.
CRISPY_TEMPLATE_PACK = 'bootstrap3'

# E-mail settings.
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = "silvestre.phoenix@gmail.com"
EMAIL_HOST_PASSWORD = "Power06051996"
EMAIL_USE_TLS = True

SERVER_EMAIL = EMAIL_HOST_USER
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Third party backends.
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

SITE_ID = 1

# Redirect settings
LOGIN_REDIRECT_URL = '/'

ACCOUNT_EMAIL_REQUIRED = True

# User will be able to authenticate by means email and user name.
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'


# CouchDB settings
COUCHDB = {
    'db': {
        'server': 'http://127.0.0.1:5984',
        'database': 'rss_aggregator',
        'default': True
    }
}

COUCHDB_VIEWS_DIR = os.path.join(BASE_DIR, 'couchdb-design-docs')

# Disqus settigns
DISQUS_API_KEY = 'bLFHResitay5LrFaKFjoHZ45wyWhc9119brXI3lYqrG7rPoncH0UlgURGiycGA17'
DISQUS_WEBSITE_SHORTNAME = 'localhost-8000-1'
