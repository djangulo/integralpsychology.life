# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-14 00:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0015_homepagefeaturerelationship_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepagefeaturerelationship',
            name='message_en',
            field=models.CharField(blank=True, help_text='Message inviting users to go see this feature', max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='homepagefeaturerelationship',
            name='message_es',
            field=models.CharField(blank=True, help_text='Message inviting users to go see this feature', max_length=254, null=True),
        ),
    ]
