# forms.py

from django import forms
from .models import Alumno
from nucleos.models import Nucleo

class AlumnoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user') 
        super(AlumnoForm, self).__init__(*args, **kwargs)
        if not user.es_superior():
            self.fields['nucleo'].queryset = Nucleo.objects.filter(id=user.nucleo.id)

    class Meta:
        model = Alumno
        fields = '__all__'
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
        }
