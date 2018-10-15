# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-14 01:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0017_auto_20181014_0105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stylesnippet',
            name='style_file',
            field=models.ForeignKey(help_text='Only filenames ending in .css, .scss or .sass will be processed.', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wagtaildocs.Document', verbose_name='style file'),
        ),
    ]
