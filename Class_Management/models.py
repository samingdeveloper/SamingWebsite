from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class ClassRoom(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,blank=True,null=True)
    className = models.CharField(max_length=255)

    def __str__(self):
        return self.className

class Quiz(models.Model):
    quizTitle = models.CharField(max_length=255)
    quizDetail = models.TextField()
    deadline = models.DateTimeField(blank=True, null=True)
    hint = models.CharField(max_length=1024, blank=True, null=True)
    text_template_content = models.TextField()
    text_testcase_content = models.TextField()
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    def __str__(self):
        return self.quizTitle

class AddTA(models.Model):
    Email = models.CharField(max_length=255)
    status_choice = (
        ('Teacher', 'Teacher'),
        ('TA', 'TA'),
    )
    title = models.CharField(max_length=100, choices=status_choice)

    def __str__(self):
        return self.Email + ' ' + '(' + self.title + ')'
