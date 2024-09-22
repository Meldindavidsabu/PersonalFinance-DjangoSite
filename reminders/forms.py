from django import forms
from .models import Reminder

class ReminderForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Date"
    )
    time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'}),
        label="Time",
        required=False
    )

    class Meta:
        model = Reminder  # Changed from Event to Reminder
        fields = ['title', 'description', 'date', 'time']
        labels = {
            'title': 'Title',
            'description': 'Description',
        }
