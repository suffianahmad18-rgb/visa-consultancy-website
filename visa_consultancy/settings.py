# visa_consultancy/settings.py
import os
from pathlib import Path
import dj_database_url
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config("SECRET_KEY", default="django-insecure-development-key-change-in-production")

DEBUG = config("DEBUG", default=False, cast=bool)  # Changed to False by default for production

ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="127.0.0.1,localhost,.onrender.com").split(",")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third party
    "crispy_forms",
    "crispy_bootstrap5",
    "ckeditor",
    "django_filters",
    "django_extensions",
    "whitenoise.runserver_nostatic",  # Add this for WhiteNoise
    # Local apps
    "accounts.apps.AccountsConfig",
    "core",
    "study_destinations",
    "applications",
    "appointments",
    "messaging",
    "testimonials",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Add WhiteNoise right after security
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# Only add cache middleware if not in DEBUG mode and not on Render's ephemeral filesystem
if not DEBUG and not os.environ.get('RENDER'):
    MIDDLEWARE.insert(0, "django.middleware.cache.UpdateCacheMiddleware")
    MIDDLEWARE.append("django.middleware.cache.FetchFromCacheMiddleware")

ROOT_URLCONF = "visa_consultancy.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "core.context_processors.site_settings",
            ],
        },
    },
]

WSGI_APPLICATION = "visa_consultancy.wsgi.application"

# Database - Use dj_database_url for Render PostgreSQL
DATABASES = {
    "default": dj_database_url.config(
        default=config("DATABASE_URL", default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}"),
        conn_max_age=600,
        ssl_require=not DEBUG  # Require SSL in production
    )
}

# For local development with MySQL (comment out when pushing to Render)
if not config("DATABASE_URL", default=None) and not os.environ.get('RENDER'):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": config("DB_NAME"),
            "USER": config("DB_USER"),
            "PASSWORD": config("DB_PASSWORD"),
            "HOST": config("DB_HOST"),
            "PORT": config("DB_PORT"),
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = "static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")] if os.path.exists(os.path.join(BASE_DIR, "static")) else []
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# WhiteNoise storage for compressed static files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files (user uploads) - Use cloud storage for Render
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# For Render's ephemeral storage, consider using cloud storage for media
if os.environ.get('RENDER'):
    # Option 1: Use temporary directory (uploads will disappear on redeploy)
    import tempfile
    MEDIA_ROOT = tempfile.mkdtemp()
    
    # Option 2: Use cloud storage like AWS S3 (uncomment and configure if needed)
    # INSTALLED_APPS += ['storages']
    # DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    # AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
    # AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
    # AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
    # AWS_S3_REGION_NAME = config('AWS_S3_REGION_NAME', default='us-east-1')

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Crispy Forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Authentication
LOGIN_URL = "accounts:login"
LOGIN_REDIRECT_URL = "core:home"
LOGOUT_REDIRECT_URL = "core:home"

# Email Configuration
EMAIL_BACKEND = config("EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend")
EMAIL_HOST = config("EMAIL_HOST", default="smtp.gmail.com")
EMAIL_PORT = config("EMAIL_PORT", default=587, cast=int)
EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=True, cast=bool)
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", default="noreply@visaconsultancy.com")

EMAIL_CONFIG = {
    "application_submitted": {
        "subject": "Visa Application Submitted - {{application_id}}",
        "template": "emails/application_submitted.html",
    },
    "status_updated": {
        "subject": "Application Status Updated - {{application_id}}",
        "template": "emails/status_updated.html",
    },
    "document_requested": {
        "subject": "Additional Documents Required - {{application_id}}",
        "template": "emails/document_requested.html",
    },
}
EMAIL_TIMEOUT = 30

# Cache Configuration - Use Redis if available, otherwise locmem
if config("REDIS_URL", default=None) and not os.environ.get('RENDER_SKIP_CACHE'):
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.redis.RedisCache",
            "LOCATION": config("REDIS_URL"),
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            },
            "KEY_PREFIX": "visa_consultancy",
        }
    }
else:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "LOCATION": "unique-snowflake",
        }
    }

# Cache timeouts
CACHE_TIMEOUTS = {
    "visa_categories": 3600,
    "application_stats": 300,
    "user_sessions": 1800,
    "country_data": 86400,
}

# Cache middleware settings (only if not on Render or with proper Redis)
if not os.environ.get('RENDER') or config("REDIS_URL", default=None):
    CACHE_MIDDLEWARE_ALIAS = "default"
    CACHE_MIDDLEWARE_SECONDS = 300
    CACHE_MIDDLEWARE_KEY_PREFIX = "visa_consultancy"

# CKEditor config
CKEDITOR_CONFIGS = {
    "default": {
        "toolbar": "full",
        "height": 300,
        "width": "100%",
    },
}

# Celery Configuration - Disable on Render if no Redis
if config("REDIS_URL", default=None):
    CELERY_BROKER_URL = config("REDIS_URL")
    CELERY_RESULT_BACKEND = config("REDIS_URL")
    CELERY_ACCEPT_CONTENT = ['json']
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_TIMEZONE = TIME_ZONE

# Security settings for production
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

# Render-specific settings
if os.environ.get('RENDER'):
    # Disable cache middleware on Render's free tier (no Redis by default)
    MIDDLEWARE = [m for m in MIDDLEWARE if 'CacheMiddleware' not in m]
    
    # Ensure ALLOWED_HOSTS includes Render domain
    RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
    if RENDER_EXTERNAL_HOSTNAME:
        ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)