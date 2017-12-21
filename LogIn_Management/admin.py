from django.contrib import admin
#from django.contrib.auth.models import User
from Class_Management.models import ClassRoom
from .models import *
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserAdminCreationForm, UserAdminChangeForm
User = get_user_model()


# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton

class classNameInline(admin.StackedInline):
    model = ClassRoom
    can_delete = False
    verbose_name_plural = 'ClassRoom'

'''class extraauthInline(admin.StackedInline):
    model = extraauth
    can_delete = False
    verbose_name_plural = 'extraauth'''

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    inlines = (classNameInline)
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'admin','staff','active')
    list_filter = ('admin','staff','active')
    fieldsets = (
        ('User info', {'fields': ('email', 'username', 'password')}),
        ('Personal info', {'fields': ('first_name','last_name')}),
        ('Permissions', {'fields': ('admin','staff','active','groups','user_permissions')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    search_fields = ('email','username')
    ordering = ('email',)
    #filter_horizontal = ()


'''class UserAdmin(admin.ModelAdmin):
    search_fields = ['email']
    form = UserAdminChangeForm #update view
    add_form = UserAdminCreationForm #create view'''


    #class Meta:
     #   model = CustomUser

# Define a new User admin
#class UserAdmin(BaseUserAdmin):
    #inlines = (extraauthInline, classNameInline )

# Re-register UserAdmin
#admin.site.unregister(User)
admin.site.register(User, UserAdmin)
#admin.site.register(Tracker)
#admin.site.register(extraauth)
# Register your models here.
#admin.site.register(User, UserAdmin)
# Remove Group Model from admin. We're not using it.
admin.site.unregister(Group)