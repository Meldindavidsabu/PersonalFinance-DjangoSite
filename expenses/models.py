from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Validator to ensure positive amounts for both Expense and Income
def validate_positive(value):
    if value <= 0:
        raise ValidationError('Amount must be greater than zero.')

# Choices for Expense Categories
CATEGORY_CHOICES = [
    ('Food', 'Food'),
    ('Transport', 'Transport'),
    ('Entertainment', 'Entertainment'),
    ('Utilities', 'Utilities'),
    ('Healthcare', 'Healthcare'),
    ('Other', 'Other'),
]

class Expense(models.Model):
    # Link each expense to a user
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Title of the expense
    title = models.CharField(max_length=255, verbose_name="Expense Title")
    # Amount of the expense
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[validate_positive], verbose_name="Expense Amount")
    # Date of the expense
    date = models.DateField(db_index=True)
    # Category of the expense
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, verbose_name="Expense Category")
    # Description of the expense
    description = models.TextField(blank=True, verbose_name="Expense Description")

    def __str__(self):
        return f"{self.title} - ₹{self.amount}"

def validate_positive(value):
    if value <= 0:
        raise ValidationError("The value must be positive.")

class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name="Income Title")
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[validate_positive], verbose_name="Income Amount")
    date = models.DateField(db_index=True)
    source = models.CharField(max_length=50, verbose_name="Income Source")
    description = models.TextField(blank=True, verbose_name="Income Description")

    def __str__(self):
        return f"{self.title} - ₹{self.amount}"