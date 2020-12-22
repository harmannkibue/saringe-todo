
import os
import sys
from decouple import config

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = True
LOCAL_DEV = True
# ALLOWED_HOSTS = ['localhost:8000', '127.0.0.1', '6ae76afe0a29.ngrok.io']
ALLOWED_HOSTS = ['*', ]
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_HOST_USER = config('')
# EMAIL_HOST_PASSWORD = config('')
EMAIL_PORT = 465
EMAIL_USE_SSL = True
DEFAULT_FROM_EMAIL = 'Request Team<email@gmail.com>'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'media')

SITE_URL="https://6d67aacc30a7.ngrok.io"

if 'test' in sys.argv:
    USE_TZ = True
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'request_test_api',
            'USER': 'request_test_user',
            'PASSWORD': 'admin123',
            'HOST': 'localhost',
            'PORT': 5432,
        }
    }
    # DATABASES = {
    #     'default': {
    #         'ENGINE': 'django.db.backends.sqlite3',
    #         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    #     }
    # }

AT_USERNAME = config('AT_USERNAME')
AT_KEY = config('AT_API_KEY')

DARAJA_BASE_URL = config("DARAJA_BASE_URL_LOCAL")

DARAJA_CONSUMER_KEY = config("DARAJA_CONSUMER_KEY")
DARAJA_CONSUMER_KEY_B2C = config("DARAJA_CONSUMER_KEY_B2C")
DARAJA_SECRET_KEY = config("DARAJA_SECRET_KEY")
DARAJA_SECRET_KEY_B2C = config("DARAJA_SECRET_KEY_B2C")

DARAJA_PASSKEY = config("DARAJA_PASSKEY")

# Todo:confirm on this
DARAJA_ENCRYPTION_KEY = config("DARAJA_ENCRYPTION_KEY")

DARAJA_SHORT_CODE = config("DARAJA_SHORT_CODE")
DARAJA_B2C_SHORT_CODE = config("DARAJA_B2C_SHORT_CODE")

DARAJA_INITIATOR = config("DARAJA_INITIATOR")
DARAJA_IS_LIVE = config("DARAJA_IS_LIVE", cast=bool)
ACCOUNT_REF = config("ACCOUNT_REF")
TRANSACTION_DEC = config("TRANSACTION_DEC")

print("The developmennnnnnnt serverrrr eneffjfljalj is running")
