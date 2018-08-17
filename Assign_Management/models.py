from Class_Management.models import *
from Assign_Management.storage import OverwriteStorage

from django.db import models
from django.db.models.signals import *
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.core.files.storage import FileSystemStorage

User = get_user_model()

def callable_path(instance, filename):
    return os.path.join('media/random', filename)
# Create your models here.

class Upload(models.Model):
    title = models.CharField(max_length=255)
    Uploadfile = models.FileField(upload_to=callable_path)
    user = models.ForeignKey("LogIn_Management.User", on_delete=models.CASCADE)
    quiz = models.ForeignKey("Class_Management.Quiz", on_delete=models.CASCADE)
    score = models.FloatField(blank=True, null=True, default=0.0)
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    uploadTime = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title

class Category(models.Model):
    name = models.CharField(max_length=255,unique=True)
    slug = models.SlugField(blank=True,null=True)
    #classroom = models.ForeignKey('Class_Management.ClassRoom',on_delete=models.CASCADE,related_name="cate_classroom")
    #parent = models.ForeignKey('self',blank=True,null=True,related_name='children',on_delete=models.CASCADE)
    class Meta:
        #unique_together = ('slug','parent',)
        verbose_name_plural = "categories"
    def __str__(self):
        return self.name
    #def __str__(self):
    #    full_path = [self.name]
    #    k = self.parent
    #    while k is not None:
    #        full_path.append(k.name)
    #        k = k.parent
    #    return ' -> '.join(full_path[::-1])


class Exam_Data(models.Model):
    classroom = models.ForeignKey(ClassRoom,on_delete=models.CASCADE)
    name = models.CharField(max_length=255,unique=True)
    detail = models.TextField(blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True)
    available = models.DateTimeField()
    deadline = models.DateTimeField()
    def __str__(self):
        return self.classroom.className + ' : ' + self.name

class Exam_Quiz(models.Model):
    title = models.CharField(unique=True, max_length=55, blank=True)
    detail = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.CASCADE)
    mode_choices = (
        ("Pass or Fail", "Pass or Fail"),
        ("Scoring", "Scoring")
    )
    mode = models.CharField(max_length=100, choices=mode_choices, default="Scoring")
    text_template_content = models.TextField(blank=True, null=True)
    text_testcode_content = models.TextField()
    text_testcase_content = models.TextField()
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    def __str__(self):
        return self.title

class Exam_Upload(models.Model):
    title = models.CharField(max_length=255)
    exam = models.ForeignKey(Exam_Data,on_delete=models.CASCADE)
    Uploadfile = models.FileField(upload_to=callable_path)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Exam_Quiz, on_delete=models.CASCADE)
    score = models.FloatField(blank=True, null=True, default=0.0)
    uploadTime = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title

class Exam_Score(models.Model):
    exam = models.ForeignKey(Exam_Data,on_delete=models.CASCADE)
    quiz = models.ForeignKey(Exam_Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    code = models.ForeignKey(Exam_Upload,on_delete=models.SET_NULL,null=True,related_name='code')
    passOrFail = models.FloatField(blank=True, null=True, default=0.0)
    total_score = models.FloatField(blank=True, null=True, default=0.0)
    max_score = models.FloatField(blank=True, null=True, default=0.0)
    def __str__(self):
        return str(self.user.userId) + " : " + str(self.quiz)

class Exam_Tracker(models.Model):
    exam = models.ForeignKey(Exam_Data,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    picked = ArrayField(models.CharField(max_length=255,blank=True),blank=True,null=True)
    def __str__(self):
        return self.user.userId + ' : ' + self.exam.name

@receiver(post_delete, sender=Upload, weak=False)
def submission_delete(sender, instance, **kwargs):
    instance_var = {"classroom":instance.classroom,
                    "user":instance.user,
                    "quiz":instance.quiz
                    }
    try:
        #print("in try")
        list_upload_obj = Upload.objects.filter(classroom=instance_var["classroom"],
                                                user=instance_var["user"],
                                                quiz=instance_var["quiz"],
                                                score__lte=Upload.objects.filter(classroom=instance_var["classroom"],
                                                                                    user=instance_var["user"],
                                                                                    quiz=instance_var["quiz"], ).aggregate(
                                                    Max("score"))["score__max"])
        #print("try success")
        #print(list_upload_obj[0])
        x = QuizScore.objects.get(classroom=instance_var["classroom"],userId=instance_var["user"],quizId=instance_var["quiz"])
        #print(x)
        if x.code == None:
            if instance_var["quiz"].mode is "Scoring":
                x.passOrFail = 0
                x.total_score = list_upload_obj[0].score
            else:
                x.passOrFail = list_upload_obj[0].score
                x.total_score = 0
            x.code = list_upload_obj[0]
            #print(x.code)
            x.save()
            #return list_upload_obj[0]
    except Exception as e:
        #print("5555")
        #print(e)
        try:
            x = QuizScore.objects.get(classroom=instance_var["classroom"],userId=instance_var["user"],quizId=instance_var["quiz"])
            x.passOrFail = 0
            x.total_score = 0
            x.code = None
            x.save()
        except:
            pass
        #return None
    instance.Uploadfile.delete(False)

@receiver(post_delete, sender=Exam_Upload, weak=False)
def exam_file_delete(sender, instance, **kwargs):
    instance_var = {"classroom":instance.exam.classroom,
                    "user":instance.user,
                    "quiz":instance.quiz
                    }
    try:
        #print("in try")
        list_upload_obj = Exam_Upload.objects.filter(exam__classroom=instance_var["classroom"],
                                                user=instance_var["user"],
                                                quiz=instance_var["quiz"],
                                                score__lte=Exam_Upload.objects.filter(exam__classroom=instance_var["classroom"],
                                                                                    user=instance_var["user"],
                                                                                    quiz=instance_var["quiz"], ).aggregate(Max("score"))["score__max"])
        #print("try success")
        #print(list_upload_obj[0])
        x = Exam_Score.objects.get(exam__classroom=instance_var["classroom"],user=instance_var["user"],quiz=instance_var["quiz"])
        #print(x)
        if x.code == None:
            if instance_var["quiz"].mode is "Scoring":
                x.passOrFail = 0
                x.total_score = list_upload_obj[0].score
            else:
                x.passOrFail = list_upload_obj[0].score
                x.total_score = 0
            x.code = list_upload_obj[0]
            #print(x.code)
            x.save()
            #return list_upload_obj[0]
    except Exception as e:
        #print("5555")
        #print(e)
        try:
            x = Exam_Score.objects.get(exam__classroom=instance_var["classroom"],user=instance_var["user"],quiz=instance_var["quiz"])
            x.passOrFail = 0
            x.total_score = 0
            x.code = None
            x.save()
        except:
            pass
        #return None
    instance.Uploadfile.delete(False)