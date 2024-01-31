from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import datetime


def validar_edad(value):
    if not 1 <= value <= 50:
        raise ValidationError(f'La edad debe estar entre 1 y 50 años. La edad proporcionada fue {value}.')


class Alumno(models.Model):
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    ]

    TIPO_SANGRE_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]

    SEXO_CHOICES = [
        ('masculino', 'Masculino'),
        ('femenino', 'Femenino'),
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
    numero_documento = models.CharField(max_length=50, blank=True, null=True)
    descripcion = models.TextField()
    id_alumno = models.AutoField(primary_key=True)
    nucleo = models.ForeignKey('nucleos.Nucleo', on_delete=models.CASCADE)
    catedra = models.CharField(max_length=100)
    
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    ]
    estatus = models.CharField(
        max_length=8,
        choices=ESTADO_CHOICES,
        default='activo',
    )
    
    tipo_sangre = models.CharField(max_length=3, choices=TIPO_SANGRE_CHOICES, default='na')
    sexo = models.CharField(max_length=9, choices=SEXO_CHOICES, default='na')
    nivel_educativo = models.CharField(max_length=10, choices=NIVEL_EDUCATIVO_CHOICES, default='na')
    nombre_de_representante = models.CharField(max_length=100)
    numero_de_telefono = models.CharField(max_length=20)
    direccion_de_habitacion = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        hoy = datetime.date.today()
        edad_calculada = hoy.year - self.fecha_nacimiento.year - ((hoy.month, hoy.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day))
        if edad_calculada != self.edad:
            raise ValidationError('La edad no coincide con la fecha de nacimiento.')
        super(Alumno, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
