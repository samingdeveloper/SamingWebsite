from django.db import models

# Create your models here.
class user(models.Model):
    userId = models.CharField(max_length=255)
    userPassWord = models.CharField(max_length=255)
    studentId = models.CharField(max_length=255)
    #Show object when transform to string.
    def __str__(self):
        return self.userId + ' - ' + self.userPassWord + ' - ' + self.studentId