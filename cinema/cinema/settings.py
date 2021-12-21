from os import path as os_path
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-pd+lbd5_w&!a0h-q0h^#65!+l7y$b_p0wjq^ur0iwo-3=qxvx_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # apps
    'main',
    'admin',
    'user',

    # custom libs
    'crispy_forms',
    'debug_toolbar',
    'django_cleanup.apps.CleanupConfig',
    'django_celery_beat',
    'django_celery_results',
]

CRISPY_TEMPLATE_PACK = 'bootstrap4'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'cinema.urls'

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

WSGI_APPLICATION = 'cinema.wsgi.application'


# REDIS related settings
REDIS_HOST = 'localhost'
REDIS_PORT = '6379'
CELERY_BROKER_URL = CELERY_RESULT_BACKEND = f'redis://{REDIS_HOST}:{REDIS_PORT}/0'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'cinema',
        'USER': 'letiso',
        'PASSWORD': '1243',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

AUTH_USER_MODEL = 'user.CustomUser'

LOGIN_URL = '/user/login'

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Europe/Kiev'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = os_path.join(BASE_DIR, 'files/media')

STATICFILES_DIRS = [
    BASE_DIR / "files/static",
]

MEDIA_DIRS = [
    BASE_DIR / "files/media",
]


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

INTERNAL_IPS = [
    '127.0.0.1',
]