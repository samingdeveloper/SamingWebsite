# Generated by Django 2.0.8 on 2018-11-06 10:48

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ClassRoom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('className', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'ordering': ('className',),
            },
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quizTitle', models.CharField(blank=True, max_length=55, unique=True)),
                ('quizDetail', models.TextField(blank=True, null=True)),
                ('deadline', models.DateTimeField()),
                ('available', models.DateTimeField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('hint', models.CharField(blank=True, max_length=255, null=True)),
                ('mode', models.CharField(choices=[('Pass or Fail', 'Pass or Fail'), ('Scoring', 'Scoring')], default='Scoring', max_length=100)),
                ('max_score', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('text_template_content', models.TextField(blank=True, null=True)),
                ('text_testcode_content', models.TextField(blank=True, null=True)),
                ('text_testcase_content', models.TextField()),
            ],
            options={
                'verbose_name_plural': 'Quizes',
                'ordering': ('available', 'quizTitle', 'category'),
            },
        ),
        migrations.CreateModel(
            name='QuizScore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('passOrFail', models.FloatField(blank=True, default=0.0, null=True)),
                ('total_score', models.FloatField(blank=True, default=0.0, null=True)),
                ('max_score', models.FloatField(blank=True, default=0.0, null=True)),
            ],
            options={
                'ordering': ('userId', 'quizId'),
            },
        ),
        migrations.CreateModel(
            name='QuizStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ('userId', 'quizId'),
            },
        ),
        migrations.CreateModel(
            name='QuizTimer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timer', models.IntegerField(null=True)),
                ('timer_stop', models.DateTimeField(blank=True, null=True)),
                ('start', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ('userId', 'quizId'),
            },
        ),
        migrations.CreateModel(
            name='QuizTracker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quizDoneCount', models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('classroom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Class_Management.ClassRoom')),
            ],
            options={
                'ordering': ('userId', 'classroom'),
            },
        ),
    ]
