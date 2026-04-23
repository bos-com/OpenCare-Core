"""
Django settings for OpenCare_Africa project.
"""

import os

# Set the Django settings module based on environment
DJANGO_ENV = os.environ.get('DJANGO_ENV', 'development')

if DJANGO_ENV == 'production':
    from .settings.production import *
elif DJANGO_ENV == 'test':
    from .settings.test import *
else:
    from .settings.development import *
