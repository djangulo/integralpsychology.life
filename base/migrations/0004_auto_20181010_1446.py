# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-10 14:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0040_page_draft_title'),
        ('wagtailforms', '0003_capitalizeverbose'),
        ('wagtailredirects', '0006_redirect_increase_max_length'),
        ('contact', '0002_auto_20181010_1446'),
        ('base', '0003_captchaformfield_placeholder'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='captchaformpage',
            name='image',
        ),
        migrations.RemoveField(
            model_name='captchaformpage',
            name='page_ptr',
        ),
        migrations.RemoveField(
            model_name='formfield',
            name='page',
        ),
        migrations.AddField(
            model_name='captchaformfield',
            name='label_en',
            field=models.CharField(help_text='The label of the form field', max_length=255, null=True, verbose_name='label'),
        ),
        migrations.AddField(
            model_name='captchaformfield',
            name='label_es',
            field=models.CharField(help_text='The label of the form field', max_length=255, null=True, verbose_name='label'),
        ),
        migrations.AddField(
            model_name='captchaformfield',
            name='placeholder_en',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='placeholder'),
        ),
        migrations.AddField(
            model_name='captchaformfield',
            name='placeholder_es',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='placeholder'),
        ),
        migrations.AlterField(
            model_name='captchaformfield',
            name='page',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='form_fields', to='base.FormPage'),
        ),
        migrations.DeleteModel(
            name='CaptchaFormPage',
        ),
        migrations.DeleteModel(
            name='FormField',
        ),
    ]