# Generated by Django 5.0.1 on 2024-01-29 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nucleos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='nucleo',
            name='nombre_responsable',
            field=models.CharField(default='No especificado', max_length=100),
            preserve_default=False,
        ),
    ]