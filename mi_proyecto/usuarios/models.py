from django.db import models
from django.contrib.auth.models import AbstractUser
from nucleos.models import Nucleo

class Usuario(AbstractUser):
    RANGO_CHOICES = [
        ('superior', 'Superior'),
        ('basico', 'Basico'),
    ]
    rango = models.CharField(max_length=8, choices=RANGO_CHOICES, default='basico')
    nucleo = models.ForeignKey(Nucleo, on_delete=models.SET_NULL, null=True, blank=True)

    def es_superior(self):
        return self.rango == 'superior'
