"""
Django settings for teambuilder project.
"""

import os

from django.core.exceptions import ImproperlyConfigured

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Set the Environment (production or dev)
ENVIRONMENT = os.environ.get('ENVIRONMENT', default='production')

# Get the SendGrid API key
SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')


if ENVIRONMENT == 'production':
    SECRET_KEY = os.environ.get("CR_SECRET_KEY") or ImproperlyConfigured("CR_SECRET_KEY not set")
else:
    SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = int(os.environ.get('DEBUG', default=0))

if ENVIRONMENT == 'production':
    # allowed hosts get parsed from a comma-separated list
    hosts = os.environ.get("CR_HOSTS") or ImproperlyConfigured("CR_HOSTS not set")
    try:
        ALLOWED_HOSTS = hosts.split(",")
    except:
        raise ImproperlyConfigured("CR_HOSTS could not be parsed")
else:
    ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # Third-party
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'debug_toolbar',
    'storages',

    # Local
    'pages.apps.PagesConfig',
    'accounts.apps.AccountsConfig',
    'projects.apps.ProjectsConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'teambuilder.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
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

WSGI_APPLICATION = 'teambuilder.wsgi.application'


# Database
if ENVIRONMENT == 'production':
    name = os.environ.get("CR_DB_NAME") or ImproperlyConfigured("CR_DB_NAME not set")
    user = os.environ.get("CR_DB_USER") or ImproperlyConfigured("CR_DB_USER not set")
    password = os.environ.get("CR_DB_PASSWORD") or ImproperlyConfigured("CR_DB_PASSWORD not set")
    host = os.environ.get("CR_DB_HOST") or ImproperlyConfigured("CR_DB_HOST not set")
    port = os.environ.get("CR_DB_PORT") or ImproperlyConfigured("CR_DB_PORT not set")

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": name,
            "USER": user,
            "PASSWORD": password,
            "HOST": host,
            "PORT": port,
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'postgres',
            'USER': 'postgres',
            'PASSWORD': 'postgres_dev_db-pw',
            'HOST': 'db',
            'PORT': 5432
        }
    }



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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'), ]  # Local static files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Production static files

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

MEDIA_URL = '/media/'  # URL for use in templates for media files
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

SITE_ID = 2

LOGIN_REDIRECT_URL = "/"

# SendGrid Email settings
EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"
# Toggle sandbox mode (when running in DEBUG mode)
SENDGRID_SANDBOX_MODE_IN_DEBUG = False
# echo to stdout or any other file-like object that is passed to the backend via the stream kwarg.
SENDGRID_ECHO_TO_STDOUT = False
DEFAULT_FROM_EMAIL = 'Team Builder <admin@teambuilder.chrisguy.co>'

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = True
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = "/accounts/profile/edit/"
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = True


ACCOUNT_FORMS = {
    'signup': 'accounts.forms.CustomSignUpForm',
    'login': 'accounts.forms.CustomLoginForm'
}


if ENVIRONMENT == 'production':
    SECURE_BROWSER_XSS_FILTER = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_REFERRER_POLICY = 'same-origin'
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


# AWS
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME')
AWS_DEFAULT_ACL = None
AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
DEFAULT_FILE_STORAGE = 'accounts.custom_storage.MediaStorage'

if ENVIRONMENT != 'production':
    INTERNAL_IPS = ['127.0.0.1', ]
    import socket

    # tricks to have debug toolbar when developing with docker
    ip = socket.gethostbyname(socket.gethostname())
    INTERNAL_IPS += [ip[:-1] + '1']

