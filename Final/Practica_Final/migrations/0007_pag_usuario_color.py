# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Practica_Final', '0006_museo_num_coments'),
    ]

    operations = [
        migrations.AddField(
            model_name='pag_usuario',
            name='COLOR',
            field=models.TextField(default='#fff'),
        ),
    ]
