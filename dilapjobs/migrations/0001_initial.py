# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='job',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('jobnumber', models.TextField()),
                ('address', models.TextField()),
                ('timestamp', models.DateTimeField()),
                ('client', models.TextField()),
                ('councilassets', models.TextField()),
                ('neighbours', models.TextField()),
                ('notes', models.TextField()),
            ],
        ),
    ]
