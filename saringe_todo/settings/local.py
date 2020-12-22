
import os
import sys
from decouple import config

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = True
LOCAL_DEV = True
ALLOWED_HOSTS = ['*', ]
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 465
EMAIL_USE_SSL = True

MEDIA_URL = "/media/"

STATIC_URL = "/static/"

MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'media')

STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'static')

STATICFILES_DIRS = (
    os.path.join(os.path.dirname(BASE_DIR), 'templates'),
)

SITE_URL = "https://708aed566785.ngrok.io"

# if 'test' in sys.argv:
#     USE_TZ = True
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.sqlite3',
#             'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#         }
#     }
# else:
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.postgresql_psycopg2',
#             'NAME': 'request_test_api',
#             'USER': 'request_test_user',
#             'PASSWORD': 'admin123',
#             'HOST': 'localhost',
#             'PORT': 5432,
#         }
#     }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

print("The developmennnnnnnt serverrrr eneffjfljalj is running")
