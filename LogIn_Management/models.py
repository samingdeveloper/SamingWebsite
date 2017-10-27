from django.db import models

# Create your models here.
class user(models.Model):
    studentId = models.CharField(max_length=255)
    userName = models.CharField(max_length=255)
    userPassWord = models.CharField(max_length=255)
    quizDone = models.IntegerField(default=0)
    quizTrack = models.FloatField(default=0)
    totalScore = models.FloatField(default=0)
    # Show object when transform to string.
    def __str__(self):
        return self.studentId + ' - ' + self.userName + ' - ' + self.userPassWord + ' - ' + self.quizDone + ' - ' + self.quizTrack + ' - ' + self.totalScore


