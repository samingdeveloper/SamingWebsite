from django.shortcuts import render,redirect
from django.shortcuts import HttpResponseRedirect
from django.http import HttpResponse
from django.template import loader
from django.contrib import messages
from django.contrib.auth import (authenticate,login,logout,get_user_model)
from django.contrib.auth.models import User
from django.middleware.csrf import CsrfViewMiddleware
from Class_Management import Template
from .models import Tracker
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
# Create your views here.

def LogIn_Page(request):
    #check_csrf(request)
    if request.user.is_authenticated:
        return HttpResponseRedirect('/LogOut')
    else:
        return render(request, 'LogIn_Page.html')
def LogOut_Page(request):

    return render(request, 'LogIn_Page.html')

def LogIn_Auth(request):
    if request.method=="POST":
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        template = loader.get_template('LogIn_Page.html')
        user_a = authenticate(request, username=username, password=password)
        context = {
            'var1':username,
        }
        '''if user is not None:
            login(request, user)
            # Redirect to a success page.
            return render(request,'LogIn_Page.html',context)
        else:
            # Return an 'invalid login' error message.
            return HttpResponse(template.render(context,request))'''
        #if user.objects.filter(userId=username) or user.objects.filter(studentId=username) and user.objects.filter(userPassWord=password):
        if user_a is not None:
            login(request, user_a)
            #if request.user_a.is_superuser:
            request.session['var'] = username
            #return render(request, 'SelectClassroom.html', context)
            return HttpResponseRedirect("/ClassRoom/Home")
        else:
            messages.error(request, 'Sorry, userId or password is not valid.')
            return HttpResponse(template.render(context, request))

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'Change_Password.html', {
        'form': form
    })
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
           # raise PermissionException() # do what you need to do here
