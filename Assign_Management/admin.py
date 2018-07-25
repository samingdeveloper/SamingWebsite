from django.contrib import admin
from django.shortcuts import redirect
from Assign_Management.models import Upload

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
    actions = [moss]

# Register your models here.
admin.site.register(Upload,UploadAdmin)