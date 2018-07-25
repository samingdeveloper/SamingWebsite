from django.db import models
from Class_Management.models import *
from Assign_Management.storage import OverwriteStorage
from django.contrib.auth import get_user_model
from django.db.models.signals import post_delete
from django.dispatch import receiver
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
    classroom = models.ForeignKey("Class_Management.ClassRoom", on_delete=models.CASCADE)
    uploadTime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

@receiver(post_delete, sender=Upload)
def submission_delete(sender, instance, **kwargs):
    instance_var = {"classroom":instance.classroom,
                    "user":instance.user,
                    "quiz":instance.quiz
                    }
    try:
        print("in try")
        list_upload_obj = Upload.objects.filter(classroom=instance_var["classroom"],
                                                user=instance_var["user"],
                                                quiz=instance_var["quiz"],
                                                score__lte=Upload.objects.filter(classroom=instance_var["classroom"],
                                                                                    user=instance_var["user"],
                                                                                    quiz=instance_var["quiz"], ).aggregate(
                                                    Max("score"))["score__max"])
        print("try success")
        print(list_upload_obj[0])
        x = QuizScore.objects.get(classroom=instance_var["classroom"],userId=instance_var["user"],quizId=instance_var["quiz"])
        print(x)
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
        print("5555")
        print(e)
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