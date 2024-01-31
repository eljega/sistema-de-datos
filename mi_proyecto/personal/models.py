from django.db import models
from django.core.exceptions import ValidationError
import datetime


def validar_edad(value):
    if not 1 <= value <= 50:
        raise ValidationError(f'La edad debe estar entre 1 y 50 años. La edad proporcionada fue {value}.')


class Personal(models.Model):
    ESTATUS_CHOICES = [
        ('renuncia', 'Renuncia'),
        ('suspension', 'Suspensión'),
        ('traslado', 'Traslado'),
    ]
    NIVEL_EDUCATIVO_CHOICES = [
        ('primaria', 'Primaria'),
        ('secundaria', 'Secundaria'),
        ('superior', 'Superior'),
        ('ninguno', 'Ninguno'),
    ]
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    edad = models.IntegerField(validators=[validar_edad])
    fecha_nacimiento = models.DateField()
    numero_documento = models.CharField(max_length=50)
    descripcion = models.TextField()
    cargo = models.CharField(max_length=100)
    funcion = models.CharField(max_length=100)
    nivel_educativo = models.CharField(max_length=10, choices=NIVEL_EDUCATIVO_CHOICES, default='na')
    fecha_ingreso = models.DateField()
    id_personal = models.AutoField(primary_key=True)
    nucleo = models.ForeignKey('nucleos.Nucleo', on_delete=models.CASCADE)
    direccion_habitacion = models.TextField()
    talla_camisa = models.CharField(max_length=50)
    talla_pantalon = models.CharField(max_length=50)
    talla_zapato = models.CharField(max_length=50)
    cargo = models.CharField(max_length=100)
    colateral = models.CharField(max_length=100)
    estatus = models.CharField(max_length=10, choices=ESTATUS_CHOICES, default='renuncia')
    def save(self, *args, **kwargs):
        # Calcula la edad basada en la fecha de nacimiento
        hoy = datetime.date.today()
        edad_calculada = hoy.year - self.fecha_nacimiento.year - ((hoy.month, hoy.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day))

        if edad_calculada != self.edad:
            raise ValidationError('La edad no coincide con la fecha de nacimiento.')

        super(Personal, self).save(*args, **kwargs)

    def __str__(self):
        return self.nombre
    # ...

