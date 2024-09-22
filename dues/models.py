from django.db import models
from django.contrib.auth.models import User
from django.core.mail import send_mail
from datetime import date  # Import date here

class Due(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    person_entity = models.CharField(max_length=255)
    borrowed_on = models.DateField()
    return_date = models.DateField()
    reason = models.TextField()
    dues_cleared = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.person_entity} owes {self.amount}"

    def send_due_reminder(self, borrower_email):
        subject = f"Payment Reminder: {self.amount} is due from {self.person_entity}"
        message_user = f"Collect {self.amount} from {self.person_entity} today."
        message_borrower = f"Dear {self.person_entity}, please pay {self.amount} to {self.user.username} today."

        send_mail(subject, message_user, 'no-reply@financetracker.com', [self.user.email])
        send_mail(subject, message_borrower, 'no-reply@financetracker.com', [borrower_email])

    @classmethod
    def get_filtered_dues(cls, user, amount=None, person_entity=None, borrowed_on=None, return_date=None, reason=None):
        queryset = cls.objects.filter(user=user)
        
        if amount is not None:
            queryset = queryset.filter(amount=amount)
        if person_entity:
            queryset = queryset.filter(person_entity__icontains=person_entity)
        if borrowed_on:
            queryset = queryset.filter(borrowed_on=borrowed_on)
        if return_date:
            queryset = queryset.filter(return_date=return_date)
        if reason:
            queryset = queryset.filter(reason__icontains=reason)

        return queryset

    @classmethod
    def get_total_amount(cls, user, **filters):
        return cls.get_filtered_dues(user, **filters).aggregate(total_amount=models.Sum('amount'))['total_amount'] or 0

    def days_remaining(self):
        delta = self.return_date - date.today()
        return delta.days if delta.days >= 0 else 0
