# Generated by Django 2.0.3 on 2018-10-22 00:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Class_Management', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Assign_Management', '0002_auto_20181022_0711'),
    ]

    operations = [
        migrations.AddField(
            model_name='upload',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='exam_upload',
            name='exam',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Assign_Management.Exam_Data'),
        ),
        migrations.AddField(
            model_name='exam_upload',
            name='quiz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Assign_Management.Exam_Quiz'),
        ),
        migrations.AddField(
            model_name='exam_upload',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='exam_tracker',
            name='exam',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Assign_Management.Exam_Data'),
        ),
        migrations.AddField(
            model_name='exam_tracker',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='exam_score',
            name='code',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='code', to='Assign_Management.Exam_Upload'),
        ),
        migrations.AddField(
            model_name='exam_score',
            name='exam',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Assign_Management.Exam_Data'),
        ),
        migrations.AddField(
            model_name='exam_score',
            name='quiz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Assign_Management.Exam_Quiz'),
        ),
        migrations.AddField(
            model_name='exam_score',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='exam_quiz',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Assign_Management.Category'),
        ),
        migrations.AddField(
            model_name='exam_quiz',
            name='classroom',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Class_Management.ClassRoom'),
        ),
        migrations.AddField(
            model_name='exam_data',
            name='classroom',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Class_Management.ClassRoom'),
        ),
        migrations.AddField(
            model_name='category',
            name='classroom',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Class_Management.ClassRoom'),
        ),
        migrations.AlterUniqueTogether(
            name='exam_quiz',
            unique_together={('title', 'classroom')},
        ),
        migrations.AlterUniqueTogether(
            name='exam_data',
            unique_together={('name', 'classroom')},
        ),
    ]