from django import forms
from .models import Personal
from nucleos.models import Nucleo

class PersonalForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')  # Tomamos el usuario como argumento
        super(PersonalForm, self).__init__(*args, **kwargs)
        if not user.es_superior():
            # Filtramos las opciones del campo 'nucleo' para que solo muestre el del usuario
            self.fields['nucleo'].queryset = Nucleo.objects.filter(id=user.nucleo.id)

    class Meta:
        model = Personal
        fields = '__all__'
        widgets = {
        'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
        'fecha_ingreso': forms.DateInput(attrs={'type': 'date'}),
    }

