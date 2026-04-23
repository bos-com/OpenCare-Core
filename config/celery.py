"""
Celery configuration for opencare-africa project.
"""

import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')

app = Celery('healthcare_backend')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


# Celery Beat Schedule
app.conf.beat_schedule = {
    'health-check-daily': {
        'task': 'apps.analytics.tasks.daily_health_check',
        'schedule': 86400.0,  # Daily
    },
    'backup-database-weekly': {
        'task': 'apps.core.tasks.backup_database',
        'schedule': 604800.0,  # Weekly
    },
    'cleanup-old-records': {
        'task': 'apps.core.tasks.cleanup_old_records',
        'schedule': 2592000.0,  # Monthly
    },
    'generate-analytics-report': {
        'task': 'apps.analytics.tasks.generate_analytics_report',
        'schedule': 86400.0,  # Daily
    },
}
