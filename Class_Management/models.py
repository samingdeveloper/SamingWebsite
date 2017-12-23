from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.
class ClassRoom(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,blank=True,null=True)
    className = models.CharField(max_length=255)

    def __str__(self):
        return self.className

class Quiz(models.Model):
    quizTitle = models.CharField(max_length=255)
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
        return self.studentId + " : " + self.quizId + " : " + self.classroom.className

class QuizScore(models.Model):
    quizId = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    studentId = models.ForeignKey(User, on_delete=models.CASCADE)
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    passOrFail = models.FloatField(blank=True, null=True)
    testCase1 = models.FloatField(blank=True, null=True)
    testCase2 = models.FloatField(blank=True, null=True)
    testCase3 = models.FloatField(blank=True, null=True)
    testCase4 = models.FloatField(blank=True, null=True)
    testCase5 = models.FloatField(blank=True, null=True)
    testCase6 = models.FloatField(blank=True, null=True)
    testCase7 = models.FloatField(blank=True, null=True)
    testCase8 = models.FloatField(blank=True, null=True)
    testCase9 = models.FloatField(blank=True, null=True)
    testCase10 = models.FloatField(blank=True, null=True)
    def __str__(self):
        return self.studentId + " : " + self.quizId + " : " + self.classroom.className

class QuizTimer(models.Model):
    quizId = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    studentId = models.ForeignKey(User, on_delete=models.CASCADE)
    timer = models.DateTimeField(blank=True, null=True)
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    def __str__(self):
        return self.studentId + " : " + self.quizId + " : " + self.classroom.className

class QuizTracker(models.Model):
    quizDoneCount = models.IntegerField(default=0)
    studentId = models.ForeignKey(User, on_delete=models.CASCADE)
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    def __str__(self):
        return self.studentId + " : " + self.classroom.className

class AddTA(models.Model):
    Email = models.CharField(max_length=255)
    status_choice = (
        ('Teacher', 'Teacher'),
        ('TA', 'TA'),
    )
    title = models.CharField(max_length=100, choices=status_choice)

    def __str__(self):
        return self.Email + ' ' + '(' + self.title + ')'
