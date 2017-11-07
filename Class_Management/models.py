from django.db import models

# Create your models here.
class ClassRoom(models.Model):
    className = models.CharField(max_length=255)

    def __str__(self):
        return self.className

class Quiz(models.Model):
    quizTitle = models.CharField(max_length=255)
    quizDetail = models.CharField(max_length=1024)
    deadline = models.DateTimeField(blank=True, null=True)
    hint = models.CharField(max_length=1024, blank=True, null=True)
    text_template_content = models.TextField()
    text_testcase_content = models.TextField()
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    def __str__(self):
        return self.quizTitle

