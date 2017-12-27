from django.contrib import admin
from Class_Management.models import *
# Register your models here.
admin.site.register(ClassRoom)
admin.site.register(Quiz)
admin.site.register(QuizStatus)
admin.site.register(QuizScore)
admin.site.register(QuizTimer)
admin.site.register(QuizTracker)
admin.site.register(AddTA)