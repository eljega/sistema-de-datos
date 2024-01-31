from django.contrib.auth.models import User, Group
from nucleos.models import Nucleo

# Crea los grupos si aún no existen
supremo_group, _ = Group.objects.get_or_create(name='Supremo')
basico_group, _ = Group.objects.get_or_create(name='Basico')

# Crea un usuario supremo
supremo_user = User.objects.create_user('nombre_supremo', password='contraseña_segura')
supremo_user.groups.add(supremo_group)
supremo_user.save()

# Asigna núcleos a usuarios específicos
for nucleo in Nucleo.objects.all():
    user = User.objects.create_user(f'usuario_{nucleo.nombre}', password='contraseña_segura')
    user.groups.add(basico_group) # Agrega el usuario al grupo Básico
    user.save()
    # Aquí se asumiría que el modelo User tiene un campo para relacionarse con Nucleo
    # Si ese campo se llamara 'nucleo', harías lo siguiente:
    user.nucleo = nucleo
    user.save()