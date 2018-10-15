# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-14 01:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import wagtail.search.index


class Migration(migrations.Migration):

    dependencies = [
        ('wagtaildocs', '0008_document_file_size'),
        ('base', '0016_auto_20181014_0029'),
    ]

    operations = [
        migrations.CreateModel(
            name='StyleSnippet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(max_length=254, verbose_name='identifier')),
                ('class_name', models.CharField(help_text='Name of the CSS class name that the snippet willbe rendered with. Be careful not to choose a class name that will interfere with the rest of the styles. The same class name needs to match the class defined in the style_file.', max_length=254, verbose_name='class name')),
                ('style_file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wagtaildocs.Document', verbose_name='style file')),
            ],
            options={
                'verbose_name': 'style snippet',
                'verbose_name_plural': 'style snippets',
            },
            bases=(wagtail.search.index.Indexed, models.Model),
        ),
        migrations.AddField(
            model_name='homepagefeaturerelationship',
            name='style',
            field=models.ForeignKey(blank=True, help_text='Style snippet to use, will use a default style if left blank.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='base.StyleSnippet'),
        ),
    ]