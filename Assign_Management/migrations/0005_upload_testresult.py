# Generated by Django 2.0.3 on 2018-10-27 15:35

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Assign_Management', '0004_upload_uploadipv4'),
    ]

    operations = [
        migrations.AddField(
            model_name='upload',
            name='testResult',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=1024), blank=True, null=True, size=None),
        ),
    ]
