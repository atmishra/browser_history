# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-11 08:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0002_auto_20170111_0742'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='url',
            field=models.URLField(),
        ),
    ]
