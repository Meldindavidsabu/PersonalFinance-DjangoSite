from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ReminderForm
from .models import Reminder
from django.core.mail import send_mail
from django.utils import timezone
from django.conf import settings
import logging
import requests

# Setting up logging
logger = logging.getLogger(__name__)

# Calendarific API key and URL
CALENDARIFIC_API_KEY = 'lcoF3hRpYNWPggGyajLVzxKlxf6w35mF'
CALENDARIFIC_API_URL = 'https://calendarific.com/api/v2/holidays'

def get_indian_holidays():
    """Fetch upcoming Indian holidays from Calendarific API."""
    try:
        today = timezone.now().date()
        params = {
            'api_key': CALENDARIFIC_API_KEY,
            'country': 'IN',
            'year': today.year,
            'type': 'national'
        }
        response = requests.get(CALENDARIFIC_API_URL, params=params)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        data = response.json()
        holidays = data.get('response', {}).get('holidays', [])
        
        # Filter holidays to get only future dates
        upcoming_holidays = [
            {
                'name': holiday.get('name'),
                'date': holiday.get('date', {}).get('iso'),
                'description': holiday.get('description', '')
            }
            for holiday in holidays if holiday.get('date', {}).get('iso') >= today.isoformat()
        ]
        return upcoming_holidays
    except requests.RequestException as e:
        logger.error(f"Error fetching holidays: {e}")
        return []

@login_required
def calendar_view(request):
    reminders = Reminder.objects.filter(user=request.user, date__gte=timezone.now().date())
    holidays = get_indian_holidays()
    return render(request, 'reminders/calendar.html', {'reminders': reminders, 'holidays': holidays})

@login_required
def add_reminder(request):
    if request.method == 'POST':
        form = ReminderForm(request.POST)
        if form.is_valid():
            reminder = form.save(commit=False)
            reminder.user = request.user
            reminder.save()
            return redirect('calendar')
    else:
        form = ReminderForm()
    return render(request, 'reminders/reminder_form.html', {'form': form})

@login_required
def edit_reminder(request, pk):
    reminder = get_object_or_404(Reminder, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ReminderForm(request.POST, instance=reminder)
        if form.is_valid():
            form.save()
            return redirect('calendar')
    else:
        form = ReminderForm(instance=reminder)
    return render(request, 'reminders/reminder_formedit.html', {'form': form, 'edit_mode': True})

@login_required
def delete_reminder(request, pk):
    reminder = get_object_or_404(Reminder, pk=pk, user=request.user)
    if request.method == 'POST':
        reminder.delete()
        return redirect('calendar')
    return render(request, 'reminders/confirm_delete.html', {'reminder': reminder})

@login_required
def notifications_view(request):
    reminders = Reminder.objects.filter(user=request.user, is_notified=False)
    return render(request, 'reminders/notifications.html', {'reminders': reminders})

@login_required
def reminder_list(request):
    reminders = Reminder.objects.filter(user=request.user).order_by('date', 'time')
    holidays = get_indian_holidays()  # Fetch holidays for any potential use in the list view
    return render(request, 'reminders/reminder_list.html', {'reminders': reminders, 'holidays': holidays})

def send_reminders():
    now = timezone.now()
    reminders = Reminder.objects.filter(date=now.date(), time__lte=now.time(), is_notified=False)
    
    logger.info(f"Checking for reminders at {now}. Found {reminders.count()} reminders to send.")
    
    for reminder in reminders:
        send_mail(
            subject='Reminder: ' + reminder.title,
            message=reminder.description,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[reminder.user.email],
        )
        reminder.is_notified = True
        reminder.save()
        
        logger.info(f"Sent reminder for {reminder.title} to {reminder.user.email}")
