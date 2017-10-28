from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class extraauth(models.Model):
    user = models.OneToOneField(User)
    year = models.IntegerField(default=1)
    studentId = models.CharField(max_length=255)


class Tracker(models.Model):
    quizDone = models.IntegerField(default=0)
    quizTrack = models.FloatField(default=0)
    totalScore = models.FloatField(default=0)




