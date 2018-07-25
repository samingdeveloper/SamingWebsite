from django.db import models
from django.db.models import Max
from django.db.models.signals import pre_delete, m2m_changed, post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.validators import MinValueValidator, MaxValueValidator
#from Assign_Management.models import Upload
import math
User = get_user_model()

# Create your models here.
class ClassRoom(models.Model):
    #teacher = models.ManyToManyField("LogIn_Management.User",related_name="teacher",blank=True)
    #ta = models.ManyToManyField("LogIn_Management.User",related_name="ta",blank=True)
    user = models.ManyToManyField("LogIn_Management.User", related_name="user", blank=True)
    className = models.CharField(max_length=255,unique=True)
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
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    def __str__(self):
        return str(self.userId.userId) + " : " + str(self.quizId) + " : " + self.classroom.className

class QuizScore(models.Model):
    quizId = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    passOrFail = models.FloatField(blank=True, null=True, default=0.0)
    total_score = models.FloatField(blank=True, null=True, default=0.0)
    max_score = models.FloatField(blank=True, null=True, default=0.0)
    #code = models.TextField(blank=True, null=True)
    code = models.ForeignKey("Assign_Management.Upload", on_delete=models.SET_NULL,null=True)
    def __str__(self):
        return str(self.userId.userId) + " : " + str(self.quizId) + " : " + self.classroom.className

class QuizTimer(models.Model):
    quizId = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    timer = models.IntegerField(null=True)
    timer_stop = models.DateTimeField(blank=True,null=True)
    start = models.BooleanField(default=False)
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.userId.userId) + " : " + str(self.quizId) + " : " + self.classroom.className

class QuizTracker(models.Model):
    quizDoneCount = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0),MaxValueValidator(100)])
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.userId.userId) + " : " + self.classroom.className

class AddTA(models.Model):
    Email = models.CharField(max_length=255)
    status_choice = (
        ('Teacher', 'Teacher'),
        ('TA', 'TA'),
    )
    title = models.CharField(max_length=100, choices=status_choice)

    def __str__(self):
        return self.Email + ' ' + '(' + self.title + ')'

# ClassRom receiver
@receiver(m2m_changed,sender=ClassRoom.user.through)
def classroom_user_changed(sender,instance,action,pk_set,**kwargs):
    if action == "post_add":
        QuizTracker.objects.bulk_create([
            QuizTracker(classroom=instance,userId=User.objects.get(pk=i)) for i in pk_set
        ])
        for i in pk_set:
            QuizStatus.objects.bulk_create([
                QuizStatus(classroom=instance,userId=User.objects.get(pk=i),quizId=y) for y in Quiz.objects.filter(classroom=instance)
            ])

    elif action == "post_remove":
        for i in pk_set:
            print(action)
            try:
                QuizTracker.objects.get(classroom=instance,userId=User.objects.get(pk=i)).delete()
            except Exception as E:
                print(E)
                continue
            try:
                QuizStatus.objects.filter(classroom=instance,userId=User.objects.get(pk=i)).delete()
            except Exception as E:
                print(E)
                continue
            try:
                QuizScore.objects.filter(classroom=instance,userId=User.objects.get(pk=i)).delete()
            except Exception as E:
                print(E)
                continue
            try:
                QuizTimer.objects.filter(classroom=instance,userId=User.objects.get(pk=i)).delete()
            except Exception as E:
                print(E)
                continue

@receiver(post_save,sender=ClassRoom)
def clasroom_created(sender,instance,**kwargs):
    Group.objects.update_or_create(name=instance.className+"_Teacher")
    Group.objects.update_or_create(name=instance.className+"_TA")

@receiver(pre_delete,sender=ClassRoom)
def clasroom_removed(sender,instance,**kwargs):
    Group.objects.get(name=instance.className+"_Teacher").delete()
    Group.objects.get(name=instance.className+"_TA").delete()