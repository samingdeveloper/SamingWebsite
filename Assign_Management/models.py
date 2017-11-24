from django.db import models
from Class_Management.models import Quiz
from Assign_Management.storage import OverwriteStorage
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
# Create your models here.


class Upload(models.Model):
    title = models.CharField(max_length=50)
    fileUpload = models.FileField(upload_to='file_uploads')
    Uploadfile = models.FileField(upload_to='file_uploads', storage=OverwriteStorage())
    user = models.ForeignKey(User)
    quiz = models.ForeignKey(Quiz)
    uploadTime = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.title



