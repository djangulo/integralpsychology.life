# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-14 00:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0014_auto_20181014_0023'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepagefeaturerelationship',
            name='message',
            field=models.CharField(blank=True, help_text='Message inviting users to go see this feature', max_length=254, null=True),
        ),
    ]
