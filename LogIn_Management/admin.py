from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from Class_Management.models import ClassRoom
from .models import *


# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class classNameInline(admin.StackedInline):
    model = ClassRoom
    can_delete = False
    verbose_name_plural = 'ClassRoom'

class extraauthInline(admin.StackedInline):
    model = extraauth
    can_delete = False
    verbose_name_plural = 'extraauth'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (extraauthInline, classNameInline )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Tracker)
admin.site.register(extraauth)