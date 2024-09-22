from __future__ import absolute_import, unicode_literals  # This should be the first line

import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finance_tracker.settings')

app = Celery('finance_tracker')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# Setting up the weekly email schedule
app.conf.beat_schedule = {
    'send-weekly-summary': {
        'task': 'expenses.tasks.send_weekly_summary',
        'schedule': crontab(day_of_week=6, hour=0, minute=0),  # Sunday at midnight
    },
    'send-reminders-every-hour': {
        'task': 'reminders.tasks.send_reminders',
        'schedule': crontab(minute=0, hour='*'),  # Runs every hour
    },
}
