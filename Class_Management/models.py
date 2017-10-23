from django.db import models

# Create your models here.
class ClassRoom(models.Model):
    className = models.CharField(max_length=255)
    def __str__(self):
        return self.className

class Quiz(models.Model):
    quizDetail = models.CharField(max_length=255)
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    def __str__(self):
        return self.quizDetail
