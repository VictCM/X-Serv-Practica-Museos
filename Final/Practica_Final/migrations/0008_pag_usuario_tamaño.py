# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Practica_Final', '0007_pag_usuario_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='pag_usuario',
            name='TAMAÑO',
            field=models.TextField(default='50%'),
        ),
    ]
