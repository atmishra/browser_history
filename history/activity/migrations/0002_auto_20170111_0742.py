# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-11 07:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='url',
            field=models.URLField(unique=True),
        ),
    ]