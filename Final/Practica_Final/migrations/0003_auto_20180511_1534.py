# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Practica_Final', '0002_auto_20180510_1538'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comentario',
            name='TEXTO',
            field=models.TextField(default='Null'),
        ),
        migrations.AlterField(
            model_name='comentario',
            name='USUARIO',
            field=models.TextField(default='Null'),
        ),
        migrations.AlterField(
            model_name='museo',
            name='ACCESIBILIDAD',
            field=models.TextField(default='Null'),
        ),
        migrations.AlterField(
            model_name='museo',
            name='BARRIO',
            field=models.CharField(default='Null', max_length=100),
        ),
        migrations.AlterField(
            model_name='museo',
            name='CLASE_VIAL',
            field=models.CharField(default='Null', max_length=100),
        ),
        migrations.AlterField(
            model_name='museo',
            name='CODIGO_POSTAL',
            field=models.CharField(default='Null', max_length=100),
        ),
        migrations.AlterField(
            model_name='museo',
            name='CONTENT_URL',
            field=models.URLField(default='Null'),
        ),
        migrations.AlterField(
            model_name='museo',
            name='COORDENADA_X',
            field=models.CharField(default='Null', max_length=100),
        ),
        migrations.AlterField(
            model_name='museo',
            name='COORDENADA_Y',
            field=models.CharField(default='Null', max_length=100),
        ),
        migrations.AlterField(
            model_name='museo',
            name='DESCRIPCION',
            field=models.TextField(default='Null'),
        ),
        migrations.AlterField(
            model_name='museo',
            name='DESCRIPCION_ENTIDAD',
            field=models.TextField(default='Null'),
        ),
        migrations.AlterField(
            model_name='museo',
            name='DISTRITO',
            field=models.CharField(default='Null', max_length=100),
        ),
        migrations.AlterField(
            model_name='museo',
            name='Dir',
            field=models.CharField(default='Null', max_length=100),
        ),
        migrations.AlterField(
            model_name='museo',
            name='EMAIL',
            field=models.TextField(default='Null'),
        ),
        migrations.AlterField(
            model_name='museo',
            name='EQUIPAMIENTO',
            field=models.TextField(default='Null'),
        ),
        migrations.AlterField(
            model_name='museo',
            name='FAX',
            field=models.TextField(default='Null'),
        ),
        migrations.AlterField(
            model_name='museo',
            name='HORARIO',
            field=models.TextField(default='Null'),
        ),
        migrations.AlterField(
            model_name='museo',
            name='ID_ENTIDAD',
            field=models.CharField(default='Null', max_length=100),
        ),
        migrations.AlterField(
            model_name='museo',
            name='Info',
            field=models.TextField(default='Null'),
        ),
        migrations.AlterField(
            model_name='museo',
            name='LATITUD',
            field=models.CharField(default='Null', max_length=100),
        ),
        migrations.AlterField(
            model_name='museo',
            name='LOCALIDAD',
            field=models.CharField(default='Null', max_length=100),
        ),
        migrations.AlterField(
            model_name='museo',
            name='LONGITUD',
            field=models.CharField(default='Null', max_length=100),
        ),
        migrations.AlterField(
            model_name='museo',
            name='NOMBRE',
            field=models.CharField(default='Null', max_length=100),
        ),
        migrations.AlterField(
            model_name='museo',
            name='NOMBRE_VIA',
            field=models.CharField(default='Null', max_length=100),
        ),
        migrations.AlterField(
            model_name='museo',
            name='NUM',
            field=models.TextField(default='Null'),
        ),
        migrations.AlterField(
            model_name='museo',
            name='Name',
            field=models.CharField(default='Null', max_length=100),
        ),
        migrations.AlterField(
            model_name='museo',
            name='PLANTA',
            field=models.CharField(default='Null', max_length=100),
        ),
        migrations.AlterField(
            model_name='museo',
            name='PROVINCIA',
            field=models.CharField(default='Null', max_length=100),
        ),
        migrations.AlterField(
            model_name='museo',
            name='TELEFONO',
            field=models.CharField(default='Null', max_length=100),
        ),
        migrations.AlterField(
            model_name='museo',
            name='TIPO',
            field=models.CharField(default='Null', max_length=100),
        ),
        migrations.AlterField(
            model_name='museo',
            name='TIPO_NUM',
            field=models.CharField(default='Null', max_length=100),
        ),
        migrations.AlterField(
            model_name='museo',
            name='TRANSPORTE',
            field=models.TextField(default='Null'),
        ),
    ]
