from django.db import models
from django.contrib.auth.models import User

# Model for storing reminders for users
class Reminder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Reference to the user who created the reminder
    title = models.CharField(max_length=255)  # Title of the reminder
    description = models.TextField()  # Detailed description of the reminder
    date = models.DateField()  # Date for the reminder
    time = models.TimeField()  # Time for the reminder
    is_notified = models.BooleanField(default=False)  # Flag to indicate if the user has been notified

    def __str__(self):
        return self.title  # String representation of the model, showing the title
