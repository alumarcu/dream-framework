# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(verbose_name='attribute name', max_length=60)),
                ('description', models.CharField(verbose_name='short description', max_length=250)),
                ('applies_to', models.CharField(max_length=10)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Club',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(verbose_name='club name', max_length=60)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(verbose_name='country name', max_length=60)),
                ('country_code', models.CharField(verbose_name='country iso code', max_length=5)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'countries',
            },
        ),
        migrations.CreateModel(
            name='Division',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('level', models.SmallIntegerField(verbose_name='division level')),
                ('teams_num', models.SmallIntegerField(verbose_name='teams required')),
                ('name', models.CharField(verbose_name='division name', max_length=30)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='League',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(verbose_name='league name', max_length=60)),
                ('min_age', models.SmallIntegerField(verbose_name='minimum age for signup')),
                ('max_age', models.SmallIntegerField(verbose_name='maximum age for signup')),
                ('gender', models.CharField(max_length=1, choices=[('m', 'Male'), ('f', 'Female')], default='u')),
                ('schedule', models.SmallIntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('country', models.ForeignKey(to='core.Country')),
            ],
        ),
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(verbose_name='manager name', max_length=60)),
                ('age', models.SmallIntegerField(null=True, blank=True)),
                ('gender', models.CharField(verbose_name='gender', max_length=1, choices=[('m', 'Male'), ('f', 'Female')], default='u')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ManagerAttribute',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('value', models.DecimalField(verbose_name='value of the attribute', decimal_places=4, max_digits=16)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('attribute', models.ForeignKey(to='core.Attribute')),
                ('manager', models.ForeignKey(to='core.Manager')),
            ],
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('round', models.IntegerField(null=True, blank=True)),
                ('season', models.IntegerField(null=True, blank=True)),
                ('can_be_draw', models.BooleanField(default=True)),
                ('stadium', models.IntegerField(null=True, blank=True)),
                ('journal', models.TextField(blank=True)),
                ('status', models.SmallIntegerField(default=1)),
                ('render_progress', models.SmallIntegerField(null=True, blank=True)),
                ('date_scheduled', models.DateTimeField(verbose_name='scheduled on', null=True, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('division', models.ForeignKey(to='core.Division')),
            ],
            options={
                'verbose_name_plural': 'matches',
            },
        ),
        migrations.CreateModel(
            name='MatchTeam',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('role', models.CharField(verbose_name='team role', max_length=60)),
                ('points', models.SmallIntegerField(verbose_name='scored points', default=0)),
                ('reward', models.SmallIntegerField(verbose_name='team reward', default=0)),
                ('tactics', models.TextField(blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('match', models.ForeignKey(to='core.Match')),
            ],
            options={
                'verbose_name_plural': 'match tactics',
            },
        ),
        migrations.CreateModel(
            name='Npc',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('first_name', models.CharField(verbose_name='npc first name', max_length=15)),
                ('last_name', models.CharField(verbose_name='npc last name', max_length=15)),
                ('nickname', models.CharField(verbose_name='npc nickname', max_length=20, blank=True)),
                ('age', models.SmallIntegerField(null=True, blank=True)),
                ('gender', models.CharField(verbose_name='gender', max_length=1, choices=[('m', 'Male'), ('f', 'Female')], default='u')),
                ('role', models.CharField(verbose_name='role', max_length=20, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('club', models.ForeignKey(to='core.Club', null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='NpcAttribute',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('value', models.DecimalField(verbose_name='value of the attribute', decimal_places=4, max_digits=16)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('attribute', models.ForeignKey(to='core.Attribute')),
                ('npc', models.ForeignKey(to='core.Npc')),
            ],
        ),
        migrations.CreateModel(
            name='Sport',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(verbose_name='team name', max_length=60)),
                ('gender', models.CharField(max_length=1, choices=[('m', 'Male'), ('f', 'Female')], default='u')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('club', models.ForeignKey(to='core.Club')),
            ],
        ),
        migrations.CreateModel(
            name='TeamDivision',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('division', models.ForeignKey(to='core.Division')),
                ('team', models.ForeignKey(to='core.Team')),
            ],
        ),
        migrations.AddField(
            model_name='npc',
            name='team',
            field=models.ForeignKey(to='core.Team', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='matchteam',
            name='team',
            field=models.ForeignKey(to='core.Team'),
        ),
        migrations.AddField(
            model_name='league',
            name='sport',
            field=models.ForeignKey(to='core.Sport'),
        ),
        migrations.AddField(
            model_name='division',
            name='league',
            field=models.ForeignKey(to='core.League'),
        ),
        migrations.AddField(
            model_name='club',
            name='country',
            field=models.ForeignKey(to='core.Country'),
        ),
        migrations.AddField(
            model_name='club',
            name='manager',
            field=models.ForeignKey(to='core.Manager'),
        ),
        migrations.AddField(
            model_name='attribute',
            name='sport',
            field=models.ForeignKey(to='core.Sport'),
        ),
    ]
