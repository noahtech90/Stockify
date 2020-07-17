from django import forms
from .models import Security

class TickerForm(forms.ModelForm):
    ticker = forms.CharField(max_length=30)
    class Meta:
        model = Security
        fields = ['ticker']
