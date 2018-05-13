# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Practica_Final', '0004_auto_20180512_1601'),
    ]

    operations = [
        migrations.CreateModel(
            name='Museo_Usuario',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('FECHA', models.TextField(default='Null')),
                ('MUSEO', models.ForeignKey(to='Practica_Final.Museo')),
            ],
        ),
        migrations.RemoveField(
            model_name='pag_usuario',
            name='Museos',
        ),
        migrations.RemoveField(
            model_name='pag_usuario',
            name='Usuario',
        ),
        migrations.AddField(
            model_name='pag_usuario',
            name='TITULO',
            field=models.TextField(default='Null'),
        ),
        migrations.AddField(
            model_name='pag_usuario',
            name='USUARIO',
            field=models.TextField(default='Null'),
        ),
        migrations.AddField(
            model_name='pag_usuario',
            name='MUSEOS',
            field=models.ManyToManyField(to='Practica_Final.Museo_Usuario'),
        ),
    ]
