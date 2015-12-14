# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dilapjobs', '0002_job_letters'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='img',
            field=models.TextField(default=b''),
        ),
    ]
