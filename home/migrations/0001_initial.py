# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-02 16:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import wagtail.core.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0040_page_draft_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomePage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('body', wagtail.core.fields.RichTextField(blank=True)),
                ('body_en', wagtail.core.fields.RichTextField(blank=True, null=True)),
                ('body_es', wagtail.core.fields.RichTextField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]