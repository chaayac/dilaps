# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dilapjobs', '0006_job_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='logs',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField()),
                ('logtext', models.TextField(default=b'', null=True)),
            ],
        ),
    ]
