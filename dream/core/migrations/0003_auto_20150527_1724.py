# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20150527_1432'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matchteam',
            name='role',
            field=models.CharField(max_length=10, verbose_name='team role', choices=[('home', 'home'), ('away', 'away')]),
        ),
        migrations.AlterField(
            model_name='matchteam',
            name='tactics',
            field=models.TextField(verbose_name='team tactics (json)', default='{}'),
        ),
    ]
