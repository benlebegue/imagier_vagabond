import sys
from os import path
from imagier.env import *

# Make sure we can import python modules from our project root
_root = path.abspath(path.dirname(__file__) + "/..")
if _root not in sys.path:
    sys.path.insert(0, _root)

# Static files, e.g. CSS
# Collected in STATICFILES_DIRS by the collectstatic command,
# and output goes in STATIC_ROOT (which should be empty)
STATIC_ROOT = _root + "/public/static"
STATICFILES_DIRS = [_root + "/static"]
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"

# User-uploaded media
MEDIA_ROOT = _root + "/public/media"

SITE_ID = 1
TIME_ZONE = "Europe/Paris"
LANGUAGE_CODE = "fr-fr"
USE_I18N = True

ALLOWED_HOSTS = [
    "imagiervagabond.fr",
    "imagiervagabond.localhost",
    "localhost",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": DATABASE_NAME,
        "USER": DATABASE_USER,
        "PASSWORD": DATABASE_PASSWORD,
        "HOST": DATABASE_HOST,
        "PORT": DATABASE_PORT,
    }
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
        "LOCATION": _root + "/cache",
    }
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": _root + "/logs/debug.log",
        },
    },
    "loggers": {
        "django.request": {
            "handlers": ["file"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            _root + "/templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.contrib.messages.context_processors.messages",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.request",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
            ]
        },
    },
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]

INSTALLED_APPS = (
    # Core utilities
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.admin",
    "django.contrib.staticfiles",
    # Third-party applications
    "sorl.thumbnail",
    # Custom-made applications
    "imagier.shared",
    "imagier.expos",
    "imagier.agenda",
    "imagier.pages",
)

ROOT_URLCONF = "imagier.urls"

# sorl.thumbnail config
THUMBNAIL_QUALITY = 90
# THUMBNAIL_PREFIX = "cache/"
