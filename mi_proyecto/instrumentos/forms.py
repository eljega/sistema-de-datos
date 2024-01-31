from django import forms
from .models import Instrumento
from nucleos.models import Nucleo

class InstrumentoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Asegúrate de que 'user' sea opcional
        super(InstrumentoForm, self).__init__(*args, **kwargs)
        if user and not user.es_superior():
            self.fields['nucleo'].queryset = Nucleo.objects.filter(id=user.nucleo.id)

    class Meta:
        model = Instrumento
        fields = '__all__'


