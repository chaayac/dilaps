# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dilapjobs', '0004_auto_20151210_2250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='client',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='councilassets',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='img',
            field=models.TextField(default=b'', null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='latitude',
            field=models.TextField(default=b'', null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='letters',
            field=models.TextField(default=b'', null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='longitude',
            field=models.TextField(default=b'', null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='neighbours',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='notes',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='postcode',
            field=models.TextField(default=b'', null=True),
        ),
    ]
