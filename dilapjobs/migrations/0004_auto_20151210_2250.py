# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dilapjobs', '0003_job_img'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='latitude',
            field=models.TextField(default=b''),
        ),
        migrations.AddField(
            model_name='job',
            name='longitude',
            field=models.TextField(default=b''),
        ),
        migrations.AddField(
            model_name='job',
            name='postcode',
            field=models.TextField(default=b''),
        ),
    ]
