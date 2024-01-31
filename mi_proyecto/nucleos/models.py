from typing import Any
from django.db import models

class Nucleo(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=50)
    fecha_apertura = models.DateField()
    direccion = models.TextField()
    telefono = models.CharField(max_length=20)
    estatus_inmueble = models.CharField(max_length=100)
    infraestructura = models.TextField()
    nombre_responsable = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


