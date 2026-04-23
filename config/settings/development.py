"""
Development settings for opencare-africa project.
"""

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1,0.0.0.0').split(',')

# Database - Use SQLite for development
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Debug Toolbar
if config('USE_DEBUG_TOOLBAR', default=True, cast=bool):
    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
    INTERNAL_IPS = ['127.0.0.1', 'localhost']

# Silk Profiler
if config('USE_SILK_PROFILER', default=False, cast=bool):
    INSTALLED_APPS += ['silk']
    MIDDLEWARE += ['silk.middleware.SilkyMiddleware']

# Email - Use console backend for development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Static files - Serve from development server
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# Media files - Serve from development server
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Logging - More verbose for development
LOGGING['root']['level'] = 'DEBUG'
LOGGING['loggers']['django']['level'] = 'DEBUG'

# CORS - Allow all origins in development
CORS_ALLOW_ALL_ORIGINS = True

# Disable HTTPS requirements
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# Allow all hosts for development
ALLOWED_HOSTS = ['*']

# Development-specific apps
# Note: django_extensions is already included in base settings
