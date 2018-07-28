# Generated by Django 2.0 on 2018-07-25 11:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Class_Management', '0001_initial'),
        ('Assign_Management', '0003_upload_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='quiztracker',
            name='userId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='quiztimer',
            name='classroom',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Class_Management.ClassRoom'),
        ),
        migrations.AddField(
            model_name='quiztimer',
            name='quizId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Class_Management.Quiz'),
        ),
        migrations.AddField(
            model_name='quiztimer',
            name='userId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='quizstatus',
            name='classroom',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Class_Management.ClassRoom'),
        ),
        migrations.AddField(
            model_name='quizstatus',
            name='quizId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Class_Management.Quiz'),
        ),
        migrations.AddField(
            model_name='quizstatus',
            name='userId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='quizscore',
            name='classroom',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Class_Management.ClassRoom'),
        ),
        migrations.AddField(
            model_name='quizscore',
            name='code',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Assign_Management.Upload'),
        ),
        migrations.AddField(
            model_name='quizscore',
            name='quizId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Class_Management.Quiz'),
        ),
        migrations.AddField(
            model_name='quizscore',
            name='userId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='quiz',
            name='classroom',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Class_Management.ClassRoom'),
        ),
        migrations.AddField(
            model_name='classroom',
            name='creator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='creator', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='classroom',
            name='user',
            field=models.ManyToManyField(blank=True, related_name='user', to=settings.AUTH_USER_MODEL),
        ),
    ]
