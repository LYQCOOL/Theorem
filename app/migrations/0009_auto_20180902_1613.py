# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-09-02 16:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_auto_20180902_1555'),
    ]

    operations = [
        migrations.AlterField(
            model_name='relation2',
            name='t11',
            field=models.IntegerField(verbose_name='relationship_t11'),
        ),
        migrations.AlterField(
            model_name='relation2',
            name='t12',
            field=models.IntegerField(verbose_name='relationship_t12'),
        ),
        migrations.AlterField(
            model_name='relation2',
            name='t21',
            field=models.IntegerField(verbose_name='relationship_t21'),
        ),
        migrations.AlterField(
            model_name='relation2',
            name='t22',
            field=models.IntegerField(verbose_name='relationship_t22'),
        ),
    ]
