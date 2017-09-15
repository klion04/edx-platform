# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certificates', '0010_certificatetemplate_language'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='certificatetemplate',
            unique_together=set([('organization_id', 'course_key', 'mode', 'language')]),
        ),
    ]
