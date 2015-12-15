# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dilapjobs', '0005_auto_20151213_2147'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='status',
            field=models.TextField(default=b'Incomplete'),
        ),
    ]
