# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Practica_Final', '0005_auto_20180512_1729'),
    ]

    operations = [
        migrations.AddField(
            model_name='museo',
            name='NUM_COMENTS',
            field=models.IntegerField(default=0),
        ),
    ]
