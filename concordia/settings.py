import os
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(PROJECT_DIR)

sys.path.append(BASE_DIR)

sys.path.append(os.path.join(BASE_DIR, 'config'))

from config import Config

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = Config.Get('django_secret_key')

ALLOWED_HOSTS = ['*'] # TODO: place this value in config.json
print ('config mode:', Config.mode)
if Config.mode == "production":
    DEBUG = False
    CSRF_COOKIE_SECURE = True
else:
    DEBUG = True
    CSRF_COOKIE_SECURE = False

sys.path.append(PROJECT_DIR)
AUTH_PASSWORD_VALIDATORS = []
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = os.path.join(BASE_DIR, 'emails')
LANGUAGE_CODE = 'en-us'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
ROOT_URLCONF = 'concordia.urls'
STATIC_ROOT = 'static'
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(PROJECT_DIR, 'static'),
                    os.path.join('/'.join(PROJECT_DIR.split('/')[:-1]), 'transcribr/transcribr/static')]
TEMPLATE_DEBUG = False
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
WSGI_APPLICATION = 'concordia.wsgi.application'

ADMIN_SITE = {
    'site_header': Config.Get('ADMIN_SITE_HEADER'),
    'site_title': Config.Get('ADMIN_SITE_TITLE'),
}

DATABASES = {
    'default': {
        'ENGINE':   Config.Get("database")["adapter"],
        'NAME':     Config.Get("database")["name"],
        'USER':     Config.Get("database")["username"],
        'PASSWORD': Config.Get("database")["password"],
        'HOST':     Config.Get("database")["host"],
        'PORT':     Config.Get("database")["port"]
    }
}


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'transcribr',
    'importer',
    'concordia',
    'faq',
    'concordia.experiments.wireframes',
]

if DEBUG:
    INSTALLED_APPS += ['django_extensions', ]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [os.path.join(PROJECT_DIR, 'templates'), ],
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': [
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
        ],
    },
}]


# Celery settings
CELERY_BROKER_URL = Config.Get('celery')['BROKER_URL']
CELERY_RESULT_BACKEND = Config.Get('celery')['RESULT_BACKEND']

CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_IMPORTS = ('importer.importer.tasks',)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'long': {
            'format': '[{asctime} {levelname} {name}:{lineno}] {message}',
            'datefmt': '%Y-%m-%dT%H:%M:%S',
            'style': '{'
        },
        'short': {
            'format': '[{levelname} {name}] {message}',
            'datefmt': '%Y-%m-%dT%H:%M:%S',
            'style': '{'
        },
    },
    'handlers': {
        'stream': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'long',
        },
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'file': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'level': 'DEBUG',
            'formatter': 'long',
            'filename': '{}/logs/concordia.log'.format(BASE_DIR),
            'when': 'H',
            'interval': 3,
            'backupCount': 16
        }
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'stream'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },

}


################################################################################
# Django-specific settings above
################################################################################

ACCOUNT_ACTIVATION_DAYS = 7

# REGISTRATION_URLS = config(
#     'DJANGO',
#     'REGISTRATION_URLS',
#     'registration.backends.simple.urls'
# )


REST_FRAMEWORK = {
    'PAGE_SIZE': Config.Get("djrf")["PAGE_SIZE"],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
}

TRANSCRIBR = dict(
     netloc="http://0.0.0.0:8000",
)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
