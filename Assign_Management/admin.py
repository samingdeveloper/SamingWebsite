from django.contrib import admin
from django.shortcuts import redirect
from Assign_Management.models import *

def moss(modeladmin, request, queryset):
    import mosspy
    userid = 367349587
    m = mosspy.Moss(userid, "python")
    for i in queryset:
        try:
            m.addFile(i.Uploadfile.path)
        except Exception as E:
            print(E)
            continue
    url = m.send()  # Submission Report URL
    return redirect(url)
    # Save report file
    #m.saveWebPage(url, "media/report/report.html")
    # Download whole report locally including code diff links
    #mosspy.download_report(url, "media/report/", connections=8)
moss.short_description = u"MOSS"

# Class here.
class UploadAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'quiz', 'score', 'uploadTime', 'classroom')
    search_fields = ('title',  'quiz__quizTitle', 'user__userId', 'classroom__className')
    actions = [moss]

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')

class Exam_DataAdmin(admin.ModelAdmin):
    list_display = ('name', 'max_score', 'available', 'deadline', 'classroom')
    search_fields = ('name', 'classroom__className')

class Exam_QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'mode')#, 'classroom')
    search_fields = ('title', 'category__name', 'mode')#, 'classroom__className')

class Exam_UploadAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'quiz', 'exam', 'score', 'uploadTime')
    search_fields = ('title', 'user', 'exam_title', 'quiz__title', )

class Exam_ScoreAdmin(admin.ModelAdmin):
    list_display = ('user', 'exam', 'quiz', 'passOrFail', 'total_score', 'max_score')
    search_fields = ('user', 'exam_title', 'quiz__title', )

class Exam_TrackerAdmin(admin.ModelAdmin):
    list_display = ('user', 'exam', 'picked')
    search_fields = ('user', 'exam_title', )

# Register your models here.
admin.site.register(Upload,UploadAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Exam_Data,Exam_DataAdmin)
admin.site.register(Exam_Quiz,Exam_QuizAdmin)
admin.site.register(Exam_Upload,Exam_UploadAdmin)
admin.site.register(Exam_Score,Exam_ScoreAdmin)
admin.site.register(Exam_Tracker,Exam_TrackerAdmin)