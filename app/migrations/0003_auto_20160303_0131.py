# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-03-03 01:31
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_url_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='click',
            old_name='tweet',
            new_name='url',
        ),
    ]