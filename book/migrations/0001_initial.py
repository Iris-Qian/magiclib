# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=100)),
                ('rating', models.CharField(max_length=10)),
                ('rating_people', models.CharField(max_length=10)),
                ('introduction', models.CharField(max_length=5000)),
            ],
        ),
    ]
