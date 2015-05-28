# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ActionRequirement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('condition', models.CharField(verbose_name='condition', max_length=30)),
                ('value', models.CharField(verbose_name='condition value', max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='EngineParam',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('section', models.CharField(verbose_name='section', max_length=100, db_index=True)),
                ('key', models.CharField(verbose_name='key', max_length=250, db_index=True, unique=True)),
                ('value', models.CharField(verbose_name='value', max_length=250)),
                ('description', models.CharField(default='', blank=True, max_length=250, verbose_name='description')),
            ],
        ),
        migrations.CreateModel(
            name='FieldZone',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('code', models.CharField(verbose_name='zone code', max_length=5)),
                ('row', models.SmallIntegerField(default=0)),
                ('col', models.SmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='PlayerAction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(verbose_name='action name', max_length=30)),
                ('description', models.CharField(verbose_name='action description', blank=True, max_length=250)),
                ('enabled', models.BooleanField(default=False, verbose_name='action enabled')),
            ],
        ),
        migrations.CreateModel(
            name='Requirement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(verbose_name='requirement name', max_length=30)),
                ('type', models.CharField(default='int', choices=[('bool', 'bool'), ('enum', 'enum'), ('int', 'int')], max_length=10, verbose_name='requirement type')),
            ],
        ),
        migrations.CreateModel(
            name='RequirementEnumValue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('value', models.CharField(verbose_name='enum value', max_length=30)),
                ('requirement', models.ForeignKey(to='soccer.Requirement')),
            ],
        ),
        migrations.AddField(
            model_name='actionrequirement',
            name='action',
            field=models.ForeignKey(to='soccer.PlayerAction'),
        ),
        migrations.AddField(
            model_name='actionrequirement',
            name='requirement',
            field=models.ForeignKey(to='soccer.Requirement'),
        ),
    ]
