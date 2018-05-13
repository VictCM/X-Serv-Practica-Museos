# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Practica_Final', '0003_auto_20180511_1534'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pag_Usuario',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('Usuario', models.CharField(default='Null', max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='museo',
            name='Dir',
        ),
        migrations.RemoveField(
            model_name='museo',
            name='Info',
        ),
        migrations.RemoveField(
            model_name='museo',
            name='Name',
        ),
        migrations.AddField(
            model_name='pag_usuario',
            name='Museos',
            field=models.ManyToManyField(to='Practica_Final.Museo'),
        ),
    ]
