from django.db import models
from django.db.models import Max
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
#from Assign_Management.models import Upload
import math
User = get_user_model()

# Create your models here.
class ClassRoom(models.Model):
    user = models.ManyToManyField("LogIn_Management.User",related_name="user")
    teacher = models.ManyToManyField("LogIn_Management.User",related_name="teacher")
    ta = models.ManyToManyField("LogIn_Management.User",related_name="ta")
    className = models.CharField(max_length=255)
    creator = models.ForeignKey("LogIn_Management.User", related_name="creator", on_delete=models.DO_NOTHING, null=True, blank=True)
    def __str__(self):
        return self.className

class Quiz(models.Model):
    quizTitle = models.CharField(unique=True, max_length=255, blank=True)
    quizDetail = models.TextField()
    deadline = models.DateTimeField(blank=True, null=True)
    hint = models.CharField(max_length=1024, blank=True, null=True)
    mode_choices = (
        ("Pass or Fail", "Pass or Fail"),
        ("Scoring", "Scoring")
    )
    mode = models.CharField(max_length=100, choices=mode_choices)
    text_template_content = models.TextField()
    text_testcase_content = models.TextField()
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    def __str__(self):
        return self.quizTitle + " : " + self.classroom.className

class QuizStatus(models.Model):
    quizId = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    studentId = models.ForeignKey(User, on_delete=models.CASCADE)
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    def __str__(self):
        return str(self.studentId.studentId) + " : " + str(self.quizId) + " : " + self.classroom.className

class QuizScore(models.Model):
    quizId = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    studentId = models.ForeignKey(User, on_delete=models.CASCADE)
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    passOrFail = models.FloatField(blank=True, null=True, default=0.0)
    total_score = models.FloatField(blank=True, null=True, default=0.0)
    max_score = models.FloatField(blank=True, null=True, default=0.0)
    #code = models.TextField(blank=True, null=True)
    code = models.ForeignKey("Assign_Management.Upload", on_delete=models.SET_NULL,null=True)
    def __str__(self):
        return str(self.studentId.studentId) + " : " + str(self.quizId) + " : " + self.classroom.className

class QuizTimer(models.Model):
    quizId = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    studentId = models.ForeignKey(User, on_delete=models.CASCADE)
    timer = models.IntegerField(null=True)
    timer_stop = models.DateTimeField(blank=True,null=True)
    start = models.BooleanField(default=False)
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.studentId.studentId) + " : " + str(self.quizId) + " : " + self.classroom.className

class QuizTracker(models.Model):
    quizDoneCount = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0),MaxValueValidator(100)])
    studentId = models.ForeignKey(User, on_delete=models.CASCADE)
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.studentId.studentId) + " : " + self.classroom.className

class AddTA(models.Model):
    Email = models.CharField(max_length=255)
    status_choice = (
        ('Teacher', 'Teacher'),
        ('TA', 'TA'),
    )
    title = models.CharField(max_length=100, choices=status_choice)

    def __str__(self):
        return self.Email + ' ' + '(' + self.title + ')'

