from django.db import models
from Class_Management.models import *
from Assign_Management.storage import OverwriteStorage
from django.contrib.auth import get_user_model
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.core.files.storage import FileSystemStorage

User = get_user_model()
# Create your models here.

class Upload(models.Model):
    title = models.CharField(max_length=50)
    fileUpload = models.FileField(upload_to='file_uploads')
    Uploadfile = models.FileField(upload_to='file_uploads', storage=OverwriteStorage())
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    uploadTime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

@receiver(post_delete, sender=Upload)
def submission_delete(sender, instance, **kwargs):
    instance.fileUpload.delete(False)
    instance.Uploadfile.delete(False)