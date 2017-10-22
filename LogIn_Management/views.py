from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect
from django.http import HttpResponse
from django.template import loader
from django.contrib import messages
from django.contrib.auth import (authenticate,login,logout,get_user_model)
from .models import user

# Create your views here.
def LogIn_Page(request):

    return render(request, 'LogIn_Page.html')

def LogIn_Auth(request):
    if request.method=="POST":
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        template = loader.get_template('LogIn_Page.html')
        #user = authenticate(request, username=username, password=password)
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
        if user.objects.filter(userId=username) or user.objects.filter(studentId=username) and user.objects.filter(userPassWord=password):
            #login(request, user)
            return render(request, 'index.html', context)
        else:
            messages.error(request, 'Sorry, userId or password is not valid.')
            return HttpResponse(template.render(context, request))




        #'''header_str = 'Hello, Python Variable'
    #template = loader.get_template('LogIn_Page.html')
    #context = {
   #     'var1':header_str
   # }'''
    #return HttpResponse(template.render(context,request))
    #return render(request,'LogIn_Page.html',context)