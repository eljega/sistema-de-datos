from django import forms
from .models import Nucleo

class NucleoForm(forms.ModelForm):
    class Meta:
        model = Nucleo
        fields = '__all__'
        widgets = {
        'fecha_apertura': forms.DateInput(attrs={'type': 'date'}),
    }

