import os
import sys
import django_heroku

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEBUG = False
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'harmannkibue@gmail.com'
EMAIL_HOST_PASSWORD = '1234'
EMAIL_PORT = 465
EMAIL_USE_SSL = True
DEFAULT_FROM_EMAIL = 'The Saringe Todo <email@gmail.com>'

LOCAL_DEV = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'mydatabase'
    }
    #     {
    #     'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #     'NAME': 'request_test_db',
    #     'USER': 'request_test_user',
    #     'PASSWORD': 'admin123',
    #     'HOST': 'localhost',
    #     'PORT': 5432,
    # }
}

SITE_URL = 'https://requestafrica.com'

AWS_QUERYSTRING_AUTH = False
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
AWS_ACCESS_KEY_ID = 'AKIAZ5SXBADM2BL5QQMX'
print("The aws acccess key is", AWS_ACCESS_KEY_ID)
AWS_SECRET_ACCESS_KEY = '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'
# AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME")
AWS_STORAGE_BUCKET_NAME = 'harmanns3'
AWS_S3_CUSTOM_DOMAIN = AWS_STORAGE_BUCKET_NAME + '.s3.amazonaws.com'
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

MEDIA_URL1 = 'https://' + AWS_STORAGE_BUCKET_NAME + '.s3.amazonaws.com/'
MEDIA_URL = MEDIA_URL1 + 'mediafiles/'
ADMIN_MEDIA_PREFIX = MEDIA_URL1 + 'admin/'

if 'test' in sys.argv:
    USE_TZ = True
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'mydatabase'
    }

CORS_ORIGIN_ALLOW_ALL = True
django_heroku.settings(locals())

print("The productionnnnnnnn serverrrrrrrrrr is running")
