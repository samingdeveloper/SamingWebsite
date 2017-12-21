from django.db import models
from Class_Management.models import Quiz
from Assign_Management.storage import OverwriteStorage
from django.contrib.auth import get_user_model
from django.core.files.storage import FileSystemStorage

User = get_user_model()
# Create your models here.

class Upload(models.Model):
    title = models.CharField(max_length=50)
    fileUpload = models.FileField(upload_to='file_uploads')
    Uploadfile = models.FileField(upload_to='file_uploads', storage=OverwriteStorage())
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    uploadTime = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.title


