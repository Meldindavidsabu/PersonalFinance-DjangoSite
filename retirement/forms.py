from django import forms
from .models import RetirementGoal

class RetirementGoalForm(forms.ModelForm):
    class Meta:
        model = RetirementGoal
        fields = ['goal_name', 'target_amount', 'current_amount', 'retirement_age', 
                  'monthly_savings', 'annual_contributions', 'expected_rate_of_return',
                  'inflation_rate', 'priority', 'target_date', 'description']
        widgets = {
            'target_date': forms.DateInput(attrs={'type': 'date'}),
        }
