# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Practica_Final', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('USUARIO', models.TextField(default=b'Null')),
                ('TEXTO', models.TextField(default=b'Null')),
                ('FECHA', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='museo',
            name='ACCESIBILIDAD',
            field=models.TextField(default=b'Null'),
        ),
        migrations.AddField(
            model_name='museo',
            name='BARRIO',
            field=models.CharField(default=b'Null', max_length=100),
        ),
        migrations.AddField(
            model_name='museo',
            name='CLASE_VIAL',
            field=models.CharField(default=b'Null', max_length=100),
        ),
        migrations.AddField(
            model_name='museo',
            name='CODIGO_POSTAL',
            field=models.CharField(default=b'Null', max_length=100),
        ),
        migrations.AddField(
            model_name='museo',
            name='CONTENT_URL',
            field=models.URLField(default=b'Null'),
        ),
        migrations.AddField(
            model_name='museo',
            name='COORDENADA_X',
            field=models.CharField(default=b'Null', max_length=100),
        ),
        migrations.AddField(
            model_name='museo',
            name='COORDENADA_Y',
            field=models.CharField(default=b'Null', max_length=100),
        ),
        migrations.AddField(
            model_name='museo',
            name='DESCRIPCION',
            field=models.TextField(default=b'Null'),
        ),
        migrations.AddField(
            model_name='museo',
            name='DESCRIPCION_ENTIDAD',
            field=models.TextField(default=b'Null'),
        ),
        migrations.AddField(
            model_name='museo',
            name='DISTRITO',
            field=models.CharField(default=b'Null', max_length=100),
        ),
        migrations.AddField(
            model_name='museo',
            name='EMAIL',
            field=models.TextField(default=b'Null'),
        ),
        migrations.AddField(
            model_name='museo',
            name='EQUIPAMIENTO',
            field=models.TextField(default=b'Null'),
        ),
        migrations.AddField(
            model_name='museo',
            name='FAX',
            field=models.TextField(default=b'Null'),
        ),
        migrations.AddField(
            model_name='museo',
            name='HORARIO',
            field=models.TextField(default=b'Null'),
        ),
        migrations.AddField(
            model_name='museo',
            name='ID_ENTIDAD',
            field=models.CharField(default=b'Null', max_length=100),
        ),
        migrations.AddField(
            model_name='museo',
            name='LATITUD',
            field=models.CharField(default=b'Null', max_length=100),
        ),
        migrations.AddField(
            model_name='museo',
            name='LOCALIDAD',
            field=models.CharField(default=b'Null', max_length=100),
        ),
        migrations.AddField(
            model_name='museo',
            name='LONGITUD',
            field=models.CharField(default=b'Null', max_length=100),
        ),
        migrations.AddField(
            model_name='museo',
            name='NOMBRE',
            field=models.CharField(default=b'Null', max_length=100),
        ),
        migrations.AddField(
            model_name='museo',
            name='NOMBRE_VIA',
            field=models.CharField(default=b'Null', max_length=100),
        ),
        migrations.AddField(
            model_name='museo',
            name='NUM',
            field=models.TextField(default=b'Null'),
        ),
        migrations.AddField(
            model_name='museo',
            name='PLANTA',
            field=models.CharField(default=b'Null', max_length=100),
        ),
        migrations.AddField(
            model_name='museo',
            name='PROVINCIA',
            field=models.CharField(default=b'Null', max_length=100),
        ),
        migrations.AddField(
            model_name='museo',
            name='TELEFONO',
            field=models.CharField(default=b'Null', max_length=100),
        ),
        migrations.AddField(
            model_name='museo',
            name='TIPO',
            field=models.CharField(default=b'Null', max_length=100),
        ),
        migrations.AddField(
            model_name='museo',
            name='TIPO_NUM',
            field=models.CharField(default=b'Null', max_length=100),
        ),
        migrations.AddField(
            model_name='museo',
            name='TRANSPORTE',
            field=models.TextField(default=b'Null'),
        ),
        migrations.AddField(
            model_name='comentario',
            name='MUSEO',
            field=models.ForeignKey(to='Practica_Final.Museo'),
        ),
    ]
