from django import forms
from .models import Due

class DueForm(forms.ModelForm):
    class Meta:
        model = Due
        fields = ['amount', 'person_entity', 'borrowed_on', 'return_date', 'reason', ]
        widgets = {
            'borrowed_on': forms.DateInput(attrs={'type': 'date'}),
            'return_date': forms.DateInput(attrs={'type': 'date'}),
        }
# dues/forms.py


class BorrowerEmailForm(forms.Form):
    borrower_email = forms.EmailField(
        label="Borrower's Email",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': "Enter borrower's email"}),
        required=True
    )


