# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-09-02 15:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_relation2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='relation2',
            name='t11',
            field=models.CharField(default='', max_length=64, verbose_name='relationship_operator'),
        ),
    ]
