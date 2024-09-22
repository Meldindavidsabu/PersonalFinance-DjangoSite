from django import forms

class CurrencyConversionForm(forms.Form):
    from_currency = forms.CharField(label='From Currency', max_length=3)
    to_currency = forms.CharField(label='To Currency', max_length=3)
    amount = forms.DecimalField(label='Amount', max_digits=10, decimal_places=2)
