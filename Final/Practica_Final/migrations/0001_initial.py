# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Museo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Name', models.CharField(default=b'Null', max_length=100)),
                ('Dir', models.CharField(default=b'Null', max_length=100)),
                ('Info', models.TextField(default=b'Null')),
            ],
        ),
    ]
