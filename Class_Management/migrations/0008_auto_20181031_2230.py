# Generated by Django 2.0.3 on 2018-10-31 15:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Class_Management', '0007_auto_20181030_1735'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='classroom',
            options={'ordering': ('className',)},
        ),
        migrations.AlterModelOptions(
            name='quiz',
            options={'ordering': ('quizTitle', 'category', 'available'), 'verbose_name_plural': 'Quizes'},
        ),
        migrations.AlterModelOptions(
            name='quizscore',
            options={'ordering': ('userId', 'quizId')},
        ),
        migrations.AlterModelOptions(
            name='quizstatus',
            options={'ordering': ('userId', 'quizId')},
        ),
        migrations.AlterModelOptions(
            name='quiztimer',
            options={'ordering': ('userId', 'quizId')},
        ),
        migrations.AlterModelOptions(
            name='quiztracker',
            options={'ordering': ('userId', 'classroom')},
        ),
    ]
