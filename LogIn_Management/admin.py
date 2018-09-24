from django.contrib import admin
#from django.contrib.auth.models import User
from Class_Management.models import ClassRoom
from .models import *
from django.conf.urls import url
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.shortcuts import HttpResponseRedirect
from .forms import UserAdminCreationForm, UserAdminChangeForm
User = get_user_model()


# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton

'''class classNameInline(admin.StackedInline):
    model = ClassRoom
    can_delete = False
    verbose_name_plural = 'ClassRoom'''

'''class extraauthInline(admin.StackedInline):
    model = extraauth
    can_delete = False
    verbose_name_plural = 'extraauth'''

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    change_list_template = "./user_changelist.html"
    # inlines = (classNameInline,)
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('userId', 'email', 'is_admin','is_staff','is_active')
    list_filter = ('is_admin','is_staff','is_active')
    fieldsets = (
        ('User info', {'fields': ('email', 'userId', 'password')}),
        ('Personal info', {'fields': ('first_name','last_name','userId')}),
        ('Permissions', {'fields': ('is_admin','is_staff','is_active','groups','user_permissions')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        ('User info', {
            'classes': ('wide',),
            'fields': ('email', 'userId', 'password1', 'password2')
        }
        ),
        ('Personal info', {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name')
        }
        ),
    )
    search_fields = ('email','userId')
    ordering = ('userId','email')
    #filter_horizontal = ()
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            url(r'^import_user/', self.import_user),
        ]
        return my_urls + urls

    def import_user(self, request):
        if request.method == 'POST' and request.user.is_admin:
            try:
                from django.contrib import messages
                from django.core.validators import validate_email
                csv_file = request.FILES.get('upload_testcase', False)
                if not csv_file.name.endswith('.csv'):
                    self.message_user(request, "file must endswith '.csv'", level=messages.ERROR)
                    return HttpResponseRedirect("../")
                elif csv_file.multiple_chunks():
                    self.message_user(request, "select a single file.", level=messages.ERROR)
                    return HttpResponseRedirect("../")
                csv_data = csv_file.read().decode("utf-8")
                lines = csv_data.split("\n")
                counter = 0
                total = 0
                failed_counter = -1
                failed_list = []
                for num,line in enumerate(lines):
                    fields = line.replace(',', '\t').split('\t')
                    # print(fields)
                    total = num
                    #if num is 0:
                    #    if fields[0].startswith('/'):
                    #        fields[0] = fields[0][1:]
                    #    else:
                    #        pass
                    try:
                        if not bool(re.match('^[a-zA-Z0-9\w.@+_-]+$', str(fields[0]).rstrip())):
                            try:
                                raise ValueError(fields[0][:-1].rstrip())
                            except Exception as e:
                                print(e)
                            failed_counter += 1
                            failed_list.append(fields[0])
                            continue
                        elif request.POST.get('text') == "import":
                            u, created = User.objects.update_or_create(userId=fields[0],
                                                                       email=fields[1],
                                                                       first_name=fields[2],
                                                                       last_name=fields[3],
                                                                       is_active=True)
                            if created:
                                u.set_password("FIBO")
                                counter += 1
                            else:
                                pass
                            u.save()
                        elif request.POST.get('text') == "delete":
                            print(fields,len(fields))
                            if len(fields) == 4:
                                try:
                                    User.objects.get(userId=fields[0]).delete()
                                                     #email=fields[1],
                                                     #first_name=fields[2],
                                                     #last_name=fields[3]).delete()
                                    counter += 1
                                except ObjectDoesNotExist:
                                    failed_counter += 1
                                    failed_list.append(fields[0])
                            elif len(fields) == 1:
                                try:
                                    validate_email(fields[0][:-1].rstrip())
                                    User.objects.get(email=fields[0].rstrip()).delete()
                                    counter += 1
                                except ObjectDoesNotExist:
                                    failed_counter += 1
                                    failed_list.append(fields[0].rstrip())
                                except Exception as E:
                                    print(E)
                                    try:
                                        User.objects.get(userId=fields[0].rstrip()).delete()
                                        counter += 1
                                    except ObjectDoesNotExist:
                                        failed_counter += 1
                                        failed_list.append(fields[0].rstrip())

                            else:
                                try:
                                    User.objects.get(userId=fields[0]).delete()
                                    counter += 1
                                except ObjectDoesNotExist:
                                    failed_counter += 1
                                    failed_list.append(fields[0])
                    except Exception as e:
                        print(e)
                        failed_counter += 1
                        failed_list.append(fields[0])
                        continue
                if request.POST.get('text') == "import":
                    status = str(counter)+'/'+str(total)+" users were imported.\n"+str(failed_counter)+' failed: '+','.join(failed_list)[:-1]
                else:
                    status = str(counter)+'/'+str(total)+" users were deleted.\n"+str(failed_counter)+' failed: '+','.join(failed_list)[:-1]
                self.message_user(request,status)
                return HttpResponseRedirect("../")
            except Exception as e:
                print(e)
                self.message_user(request, e, level=messages.ERROR)
                return HttpResponseRedirect("../")

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
#admin.site.unregister(Group)