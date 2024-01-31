from django.db import models

class Instrumento(models.Model):
    fecha = models.DateField(auto_now_add=True)
    
    POLIZA_SEGURO_CHOICES = [
        ('si', 'Sí'),
        ('no', 'No'),
    ]
    poliza_seguro = models.CharField(max_length=3, choices=POLIZA_SEGURO_CHOICES, default='no')

    nombre_persona = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255)
    numero_expediente_procesal = models.CharField(max_length=100)

    PROCEDENCIA_CHOICES = [
        ('fmsb', 'FMSB'),
        ('dsr', 'DSR'),
        ('comodato', 'Comodato'),
        ('otro', 'Otro'),
    ]
    procedencia = models.CharField(
        max_length=100,
        choices=PROCEDENCIA_CHOICES,
        default='otro'
    )

    CONDICION_CHOICES = [
        ('operativo', 'Operativo'),
        ('inoperativo', 'Inoperativo'),
        ('danada', 'Dañada'),
        ('obsoleto', 'Obsoleto'),
        ('deuso', 'De uso'),
    ]
    condicion = models.CharField(max_length=100, choices=CONDICION_CHOICES, default='operativo')

    COMODATO_CHOICES = [
        ('si', 'Sí'),
        ('no', 'No'),
        ('na', 'N/A'),
        ('sc', 'S/C'),
    ]
    comodato_vigente = models.CharField(
        max_length=100,
        choices=COMODATO_CHOICES,
        default='na',
    )

    item = models.CharField(max_length=100)
    marca = models.CharField(max_length=100)
    cantidad = models.IntegerField()
    modelo = models.CharField(max_length=100)
    medida = models.CharField(max_length=100)
    color = models.CharField(max_length=50)
    serial = models.CharField(max_length=100)
    inventario = models.CharField(max_length=100)
    accesorio = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=100)
    descripcion = models.TextField()
    id_instrumento = models.AutoField(primary_key=True)
    nucleo = models.ForeignKey('nucleos.Nucleo', on_delete=models.CASCADE)

    def __str__(self):
        return self.item
