from .base import *
import django_heroku

DEBUG = False
ALLOWED_HOSTS = ['*']

CORS_ORIGIN_ALLOW_ALL = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'dcpv057i5gjqcc',
        'USER': 'nhruspamqaixhv',
        'PASSWORD': 'd8d7d7a970e0e8fd47d34f8529d0654c6252353040145e1196bdc7e46b997298',
        'HOST': 'ec2-54-75-229-28.eu-west-1.compute.amazonaws.com',
        'PORT': '5432',
    }
}

import dj_database_url
DATABASES['default'] =dj_database_url.config(conn_max_age=600, ssl_require=True)

# configure Django App for Heroku
django_heroku.settings(locals())