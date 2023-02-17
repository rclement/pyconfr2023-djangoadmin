import os
import dj_database_url
import django_stubs_ext

from pathlib import Path
from django.core.management.utils import get_random_secret_key
from dotenv import load_dotenv


load_dotenv()
django_stubs_ext.monkeypatch()

BASE_DIR = Path(__file__).resolve().parent.parent

APP_ENVIRONMENT = os.getenv("APP_ENVIRONMENT", "production")
SECRET_KEY = os.getenv("SECRET_KEY", get_random_secret_key())
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")
FORCE_HTTPS = os.getenv("FORCE_HTTPS") == "true"
DATABASE_URL = os.getenv("DATABASE_URL")

PRODUCTION = APP_ENVIRONMENT == "production"
DEBUG = APP_ENVIRONMENT == "development"
TESTING = APP_ENVIRONMENT == "testing"

INSTALLED_APPS = [
    "whitenoise.runserver_nostatic",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "app.apps.AppAdminConfig",
    "app.accounts",
    "app.timetracking",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

SECURE_SSL_REDIRECT = FORCE_HTTPS
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https") if PRODUCTION else None

SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"
SESSION_COOKIE_NAME = "session"
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = PRODUCTION

CSRF_COOKIE_SECURE = PRODUCTION

ROOT_URLCONF = "app.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "app" / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "app.wsgi.application"

DATABASES = {
    "default": dj_database_url.config(default=DATABASE_URL),
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_ROOT = BASE_DIR / "staticfiles"
STATIC_URL = "static/"
STATICFILES_DIRS = [
    BASE_DIR / "app" / "static",
]
STATICFILES_STORAGE = (
    "django.contrib.staticfiles.storage.StaticFilesStorage"
    if TESTING
    else "whitenoise.storage.CompressedManifestStaticFilesStorage"
)

MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "media/"
DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "accounts.User"
