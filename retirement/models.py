from django.db import models
from django.contrib.auth.models import User

class RetirementGoal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='retirement_goals')
    goal_name = models.CharField(max_length=255)
    target_amount = models.DecimalField(max_digits=12, decimal_places=2)
    current_amount = models.DecimalField(max_digits=12, decimal_places=2)
    retirement_age = models.IntegerField()
    monthly_savings = models.DecimalField(max_digits=10, decimal_places=2)
    annual_contributions = models.DecimalField(max_digits=10, decimal_places=2)
    expected_rate_of_return = models.DecimalField(max_digits=5, decimal_places=2)
    inflation_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)  # Default to 0.00 if not set
    priority = models.CharField(max_length=50, choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')])
    target_date = models.DateField()
    description = models.TextField(blank=True)

    def __str__(self):
        return self.goal_name

    def progress_percentage(self):
        """Calculate progress as a percentage of target amount."""
        if self.target_amount == 0:
            return 0
        return (self.current_amount / self.target_amount) * 100
