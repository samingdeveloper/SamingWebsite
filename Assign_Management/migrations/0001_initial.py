# Generated by Django 2.0.3 on 2018-07-25 12:14

import Assign_Management.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Upload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('Uploadfile', models.FileField(upload_to=Assign_Management.models.callable_path)),
                ('score', models.FloatField(blank=True, default=0.0, null=True)),
                ('uploadTime', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
