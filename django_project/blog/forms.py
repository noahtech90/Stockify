from django import forms
from .models import Security

class TickerForm(forms.ModelForm):
    ticker = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Enter "BA" and search', 'class': 'ticker-field'}))
    class Meta:
        model = Security
        fields = ['ticker']
