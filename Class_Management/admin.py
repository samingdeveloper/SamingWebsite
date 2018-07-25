from django.contrib import admin
from django.shortcuts import redirect
from Class_Management.models import *
# Register your models here.
def export_csv(modeladmin, request, queryset):
    import csv
    from django.utils.encoding import smart_str
    from django.http import HttpResponse
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Quiscore.csv'
    writer = csv.writer(response, csv.excel)
    response.write(u'\ufeff'.encode('utf8')) # BOM (optional...Excel needs it to open UTF-8 file properly)
    writer.writerow([
        smart_str(u"Title"),
        smart_str(u"userId"),
        smart_str(u"Classroom"),
        smart_str(u"PassOrFail"),
        smart_str(u"TotalScore"),
        smart_str(u"MaxScore")

    ])
    for obj in queryset:
        writer.writerow([
            smart_str(obj.quizId.quizTitle),
            smart_str(obj.userId.userId),
            smart_str(obj.classroom),
            smart_str(obj.passOrFail),
            smart_str(obj.total_score),
            smart_str(obj.max_score)
        ])
    return response
export_csv.short_description = u"Export CSV"

def moss(modeladmin, request, queryset):
    import mosspy
    userid = 367349587
    m = mosspy.Moss(userid, "python")
    for i in queryset:
        try:
            m.addFile(i.code.Uploadfile.path)
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

class ClassRoomAdmin(admin.ModelAdmin):
    filter_horizontal = ('user',)

class QuizScoreAdmin(admin.ModelAdmin):
    actions = [export_csv,moss]


admin.site.register(ClassRoom,ClassRoomAdmin)
admin.site.register(Quiz)
admin.site.register(QuizStatus)
admin.site.register(QuizScore,QuizScoreAdmin)
admin.site.register(QuizTimer)
admin.site.register(QuizTracker)
admin.site.register(AddTA)