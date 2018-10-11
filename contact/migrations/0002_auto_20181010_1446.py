# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-10 14:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactcaptchaformfield',
            name='placeholder',
            field=models.CharField(blank=True, max_length=255, verbose_name='placeholder'),
        ),
        migrations.AddField(
            model_name='contactcaptchaformfield',
            name='placeholder_en',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='placeholder'),
        ),
        migrations.AddField(
            model_name='contactcaptchaformfield',
            name='placeholder_es',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='placeholder'),
        ),
    ]