# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-10 15:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_auto_20181010_1455'),
    ]

    operations = [
        migrations.AddField(
            model_name='captchaformfield',
            name='hide_label',
            field=models.BooleanField(default=False),
        ),
    ]
