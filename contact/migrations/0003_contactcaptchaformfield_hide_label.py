# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-10 15:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0002_auto_20181010_1446'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactcaptchaformfield',
            name='hide_label',
            field=models.BooleanField(default=False),
        ),
    ]