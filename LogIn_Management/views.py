from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect
from django.http import HttpResponse
from django.template import loader
from django.contrib import messages
from django.contrib.auth import (authenticate,login,logout,get_user_model)
from django.middleware.csrf import CsrfViewMiddleware
from Class_Management import Template
#from .models import Tracker
User = get_user_model()
# Create your views here.

def LogIn_Page(request):
    #check_csrf(request)
    if request.user.is_authenticated:
        return HttpResponseRedirect('/LogOut')

    elif request.method=="POST":
        userId = request.POST.get('userId','')
        password = request.POST.get('password','')
        template = loader.get_template('LogIn_Page.html')
        user_a = authenticate(request, username=userId, password=password)
        context = {
            'var1':userId,
        }
        #if user is not None:
            #login(request, user)
            # Redirect to a success page.
            #return render(request,'LogIn_Page.html',context)
        #else:
            # Return an 'invalid login' error message.
            #return HttpResponse(template.render(context,request))
        #if user.objects.filter(userId=userId) or user.objects.filter(userId=userId) and user.objects.filter(userPassWord=password):
        if user_a is not None:
            login(request, user_a)
            #if request.user_a.is_admin:

            #return render(request, 'SelectClassroom.html', context)
            return HttpResponseRedirect("/ClassRoom/")

        else:
            messages.error(request, 'Invalid user ID or password.')
            return HttpResponse(template.render(context, request))
    else:
        return render(request, 'LogIn_Page.html')

def LogOut_Page(request):
    return render(request, 'LogIn_Page.html')

def Change_Password(request):
    if request.method == "POST":
        new_pass = request.POST.get("newpassword")
        con_pass = request.POST.get("confirmpassword")
        if new_pass == con_pass:
            u = User.objects.get(userId__exact=request.user.userId)
            u.set_password(new_pass)
            u.save()
            return render(request, 'Change_Password.html', {'change_pass_status':"You've successfully change your password."})
        else:
            return render(request, 'Change_Password.html',
                          {'change_pass_status': "You've failed to change your password."})

    else:
        return render(request,'Change_Password.html')

def Forgot_Password(request):
    if request.method == "POST":
        Email = request.POST.get("Email")
        if new_pass == con_pass:
            u = User.objects.get(userId__exact=request.user.userId)
            u.set_password(new_pass)
            u.save()
            return render(request, 'Forgot_Password.html', {'change_pass_status':"You've successfully change your password."})
        else:
            return render(request, 'Forgot_Password.html',
                          {'change_pass_status': "You've failed to change your password."})
    else:
        return render(request,'Forgot_Password.html')
        #'''header_str = 'Hello, Python Variable'
    #template = loader.get_template('LogIn_Page.html')
    #context = {
   #     'var1':header_str
   # }'''
    #return HttpResponse(template.render(context,request))
    #return render(request,'LogIn_Page.html',context)

        #def check_csrf(request):
         # reason = CsrfViewMiddleware().process_view(request, None, (), {})
         # if reason:
            # CSRF failed
           # raise PermissionException() # do what you need to do here'''

def Admin_Panel(request):
    if not request.user.is_authenticated or not request.user.is_admin:
        return HttpResponseRedirect('/LogOut')
    else:
        return render(request, 'AdminPanel/AdminPanel.html')
