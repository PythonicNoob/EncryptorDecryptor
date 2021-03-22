from django import forms
from .models import data

class dataForm(forms.ModelForm):
    encrypt = forms.CharField(max_length=15)

    class Meta:
        model = data
        exclude = ['id', 'encrypt']



