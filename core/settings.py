"""
Django settings for DataLinkCRM project.
"""
import os
from pathlib import Path
from decouple import config
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='django-insecure-kt0w2p6f9q8y5h3m1v4x6z7b0c1n2b3x4y5z6w7q8r9s0t1u2v3w4x5y6z7')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '.vercel.app', '.herokuapp.com', 'localhost:8000']

# Application definition
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'django.contrib.postgres',  # Disabled for SQLite development
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'rest_framework_simplejwt',
    'crispy_forms',
    'crispy_bootstrap5',
    'widget_tweaks',
    'import_export',
    'django_filters',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.github',
    'storages',
    'corsheaders',
    'django_htmx',
    'django.contrib.humanize',
    'django_bootstrap5',
]

LOCAL_APPS = [
    'core',
    'authentication',
    'dashboard',
    'customers',
    'projects',
    'subscriptions',
    'payments',
    'communications',
    'analytics',
    'settings',
    'widgets',
    'calendar',
    'maps',
    'reports',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_htmx.middleware.HtmxMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.global_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'
ASGI_APPLICATION = 'core.asgi.application'

# Database
# Database - Using SQLite for development
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Supabase Configuration
SUPABASE_URL = config('SUPABASE_URL', default='https://lwsvighhclplixrzygyg.supabase.co')
SUPABASE_ANON_KEY = config('SUPABASE_ANON_KEY', default='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imx3c3ZpZ2hoY2xwbGl4cnp5Z3lnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjI3NDU1MzUsImV4cCI6MjA3ODMyMTUzNX0.RWYNK-A_Qn8IBdupQnCMc8nTibL91NQOxhEWo-DmzwU')

# Password validation
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
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Nairobi'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Authentication settings
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/auth/login/'
LOGIN_URL = '/auth/login/'

# Django REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.FileUploadParser',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20
}

# Simple JWT settings
from datetime import timedelta
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,
}

# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='brauhmani31@gmail.com')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='oakjazoekos')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='noreply@datalinkcrm.com')

# Payment Integration Settings

# Stripe Configuration
STRIPE_PUBLISHABLE_KEY = config('STRIPE_PUBLISHABLE_KEY', default='your_stripe_publishable_key_here')
STRIPE_SECRET_KEY = config('STRIPE_SECRET_KEY', default='your_stripe_secret_key_here')
STRIPE_WEBHOOK_SECRET = config('STRIPE_WEBHOOK_SECRET', default='')

# M-PESA Configuration
MPESA_AUTH_URL = config('MPESA_AUTH_URL', default='https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials')
MPESA_ONLINEPAYMENT_URL = config('MPESA_ONLINEPAYMENT_URL', default='https://api.safaricom.co.ke/mpesa/stkpush/v1/processrequest')
MPESA_ENV = config('MPESA_ENV', default='sandbox')
MPESA_BUSINESS_SHORTCODE = config('MPESA_BUSINESS_SHORTCODE', default='174379')
MPESA_PARTY_B = config('MPESA_PARTY_B', default='174379')
MPESA_CONSUMER_KEY = config('MPESA_CONSUMER_KEY', default='TnDaW9OW8POrUGA1Vz0FO3PDPKEGVTjhIw0rqNtjBufXJsS3')
MPESA_CONSUMER_SECRET = config('MPESA_CONSUMER_SECRET', default='OjPltJPJSzM8nKzSOPP2IG8TwRBnwmfe5YMWpOs01uJhN6gq8brqTeBzAybcyHkQ')
MPESA_BUSINESS_SHORT_CODE = config('MPESA_BUSINESS_SHORT_CODE', default='174379')
MPESA_PASS_KEY = config('MPESA_PASS_KEY', default='bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919')

# M-PESA Callback URLs (Update after deployment)
MPESA_CALLBACK_URL = config('MPESA_CALLBACK_URL', default='https://your-project-name.herokuapp.com/api/mpesa-callback')
MPESA_TIMEOUT_URL = config('MPESA_TIMEOUT_URL', default='https://your-project-name.herokuapp.com/api/mpesa-timeout')

# Crispy Forms Bootstrap 5
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# CORS settings
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://datalinkcrm.com",
    "https://www.datalinkcrm.com",
]

# Phone number for Kenya
KENYA_PHONE_COUNTRY_CODE = '+254'
PHONE_NUMBER_PATTERN = r'^\+254[0-9]{9}$'

# Kenya-specific date settings
DATE_FORMAT = 'Y-m-d'
DATETIME_FORMAT = 'Y-m-d H:i:s'
USE_L10N = False
DATE_FORMAT = 'Y-m-d'

# Bootstrap 5 settings
BOOTSTRAP5 = {
    'required_css_class': 'required',
    'set_placeholder': False,
    'success_css_class': 'is-valid',
    'formset_tags': {
        'formset': 'formset',
        'form': 'form',
        'management_form': 'management-form',
        'non_form_errors': 'alert alert-danger non-form-errors',
        'errors': 'alert alert-danger form-errors',
        'layout': 'form-layout',
    }
}

# Mapbox API Key (if using Mapbox for maps)
MAPBOX_ACCESS_TOKEN = config('MAPBOX_ACCESS_TOKEN', default='')

# Celery Configuration (for background tasks)
CELERY_BROKER_URL = config('CELERY_BROKER_URL', default='redis://localhost:6379/0')
CELERY_RESULT_BACKEND = config('CELERY_RESULT_BACKEND', default='redis://localhost:6379/0')

# Cache configuration
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': config('REDIS_URL', default='redis://localhost:6379/1'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# Session configuration
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'
SESSION_COOKIE_AGE = 86400  # 24 hours

# Security settings (for production)
SECURE_SSL_REDIRECT = not DEBUG
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# File upload settings
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
FILE_UPLOAD_TEMP_DIR = os.path.join(BASE_DIR, 'tmp')
os.makedirs(FILE_UPLOAD_TEMP_DIR, exist_ok=True)

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'django.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'core': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

# Ensure logs directory exists
os.makedirs(BASE_DIR / 'logs', exist_ok=True)