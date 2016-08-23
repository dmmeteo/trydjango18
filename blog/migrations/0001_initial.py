# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name=b'Publication date')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('content', models.TextField(max_length=10000)),
            ],
        ),
    ]
