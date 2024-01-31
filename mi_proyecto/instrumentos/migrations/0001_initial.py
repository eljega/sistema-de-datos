# Generated by Django 5.0.1 on 2024-01-13 02:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('nucleos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Instrumento',
            fields=[
                ('item', models.CharField(max_length=100)),
                ('marca', models.CharField(max_length=100)),
                ('cantidad', models.IntegerField()),
                ('modelo', models.CharField(max_length=100)),
                ('medida', models.CharField(max_length=100)),
                ('color', models.CharField(max_length=50)),
                ('serial', models.CharField(max_length=100)),
                ('inventario', models.CharField(max_length=100)),
                ('accesorio', models.CharField(max_length=100)),
                ('condicion', models.CharField(max_length=100)),
                ('ubicacion', models.CharField(max_length=100)),
                ('procedencia', models.CharField(max_length=100)),
                ('comodato_vigente', models.BooleanField(default=False)),
                ('descripcion', models.TextField()),
                ('id_instrumento', models.AutoField(primary_key=True, serialize=False)),
                ('nucleo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nucleos.nucleo')),
            ],
        ),
    ]