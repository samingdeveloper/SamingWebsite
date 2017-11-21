from django.db import models
from Class_Management.models import Quiz
from django.contrib.auth.models import User
# Create your models here.

class Upload(models.Model):
    title = models.CharField(max_length=50)
    fileUpload = models.FileField(upload_to='file_uploads')
    user = models.ForeignKey(User)
    quiz = models.ForeignKey(Quiz)
    uploadTime = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.title

