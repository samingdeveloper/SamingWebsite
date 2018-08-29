from django.db import models
from django.db.models import Max
from django.db.models.signals import pre_delete, m2m_changed, pre_save, post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist
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

#class Rank(models.Model):
#    userId = models.ForeignKey(User, on_delete=models.CASCADE)
#    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
#    #elo = models.FloatField(default=0, validators=[MinValueValidator(0)])
#    rank_choices = (
#        (0, "Bronze"),
#        (1, "Silver"),
#        (2, "Gold"),
#        (3, "Platinum"),
#        (4, "Diamond"),
#        (5, "Master"),
#        (6, "Challenger"),
#    )
#    rank = models.SmallIntegerField(choices=rank_choices, default=0)
#    fixture = models.BooleanField(default=False)
#    def __str__(self):
#        return self.classroom.className + ' : ' + self.userId.userId #+ ' : ' + self.elo

class Quiz(models.Model):
    quizTitle = models.CharField(unique=True, max_length=55, blank=True)
    quizDetail = models.TextField(blank=True,null=True)
    deadline = models.DateTimeField()
    available = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)
    hint = models.CharField(max_length=255, blank=True, null=True)
    #exam = models.BooleanField(default=False)
    category = models.ForeignKey('Assign_Management.Category', blank=True, null=True, on_delete=models.CASCADE ,related_name='category')
    #rank_choices = (
    #    (0, "Bronze"),
    #    (1, "Silver"),
    #    (2, "Gold"),
    #    (3, "Platinum"),
    #    (4, "Diamond"),
    #    (5, "Master"),
    #    (6, "Challenger"),
    #)
    #rank = models.SmallIntegerField(choices=rank_choices, default=0)
    mode_choices = (
        ("Pass or Fail", "Pass or Fail"),
        ("Scoring", "Scoring")
    )
    mode = models.CharField(max_length=100, choices=mode_choices, default="Scoring")
    max_score = models.FloatField(default=0, validators=[MinValueValidator(0), ])
    text_template_content = models.TextField(blank=True,null=True)
    text_testcode_content = models.TextField()
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
    code = models.ForeignKey("Assign_Management.Upload", on_delete=models.SET_NULL,null=True,related_name='code')
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
    quizDoneCount = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0),])
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.userId.userId) + " : " + self.classroom.className

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

@receiver(pre_save,sender=ClassRoom)
def classroom_create(sender,instance,**kwargs):
    import re
    if not (bool(re.match('^[a-zA-Z0-9\w.@+_-]+$', instance.className))):
        raise ValueError("Classname must contains only alphabet or numeric.")

@receiver(post_save,sender=ClassRoom)
def clasroom_created(sender,instance,**kwargs):
    Group.objects.update_or_create(name=instance.className+"_Teacher")
    Group.objects.update_or_create(name=instance.className+"_TA")


@receiver(pre_delete,sender=ClassRoom)
def clasroom_removed(sender,instance,**kwargs):
    try:
        Group.objects.get(name=instance.className+"_Teacher").delete()
        Group.objects.get(name=instance.className+"_TA").delete()
    except Exception as E:
        print(E)

#@receiver(post_save, sender=QuizTracker, weak=False)
#def rank_update(sender,instance,**kwargs):
#    try:
#        rank = Rank.objects.get(userId=instance.userId, classroom=instance.classroom)#.update(rank=int(QuizTracker.objects.get(userId=instance.userId,classroom=instance.classroom).quizDoneCount/int((len(Quiz.objects.filter(classroom=instance.classroom))/7))))
#        if rank.fixture:
#            return None
#        rank.rank = int(QuizTracker.objects.get(userId=instance.userId,classroom=instance.classroom).quizDoneCount/int((len(Quiz.objects.filter(classroom=instance.classroom))/7))) - 1
#    except ObjectDoesNotExist:
#        rank = Rank(userId=instance.userId, classroom=instance.classroom)
#        if rank.fixture:
#            return None
#        try:
#            rank.rank = int(QuizTracker.objects.get(userId=instance.userId, classroom=instance.classroom).quizDoneCount / int((len(Quiz.objects.filter(classroom=instance.classroom))/7))) -1
#        except ZeroDivisionError:
#            rank = Rank.objects.get(userId=instance.userId, classroom=instance.classroom)
#            rank.rank = 0
#    except ValueError:
#        rank = Rank.objects.get(userId=instance.userId, classroom=instance.classroom)
#        rank.rank = 0
#    except ZeroDivisionError:
#        rank = Rank.objects.get(userId=instance.userId, classroom=instance.classroom)
#        rank.rank = 0
#    rank.save()
#
#@receiver(pre_delete, sender=QuizTracker, weak=False)
#def rank_remove(sender,instance,**kwargs):
#    try:
#        rank = Rank.objects.get(userId=instance.userId,classroom=instance.classroom)
#        if rank.fixture:
#            return None
#        rank.delete()
#        rank.save()
#    except ObjectDoesNotExist:
#        pass
