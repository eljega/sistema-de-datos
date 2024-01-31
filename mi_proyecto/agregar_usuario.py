from django.contrib.auth.models import User, Group
from nucleos.models import Nucleo

supremo_group, _ = Group.objects.get_or_create(name='Supremo')
basico_group, _ = Group.objects.get_or_create(name='Basico')

supremo_user = User.objects.create_user('nombre_supremo', password='contraseña_segura')
supremo_user.groups.add(supremo_group)
supremo_user.save()

for nucleo in Nucleo.objects.all():
    user = User.objects.create_user(f'usuario_{nucleo.nombre}', password='contraseña_segura')
    user.groups.add(basico_group)
    user.save()
    user.nucleo = nucleo
    user.save()