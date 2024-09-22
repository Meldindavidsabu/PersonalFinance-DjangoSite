# reminders/tasks.py

from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Reminder
from django.utils import timezone

@shared_task
def send_reminders():
    now = timezone.now()
    reminders = Reminder.objects.filter(date=now.date(), time__lte=now.time(), is_notified=False)
    for reminder in reminders:
        send_mail(
            subject='Reminder: ' + reminder.title,
            message=reminder.description,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[reminder.user.email],
        )
        reminder.is_notified = True
        reminder.save()
