from django.shortcuts import render
from .models import ClassRoom,Quiz
from django.http import Http404
from django.contrib.auth.models import User

def Home(request):
    var = request.session['var']
    if User.objects.get(username=var).extraauth.year:
        context = {
            'var':User.objects.get(username=var).extraauth.year,
            'classname':ClassRoom.objects.get(id=User.objects.get(username=var).extraauth.year),
            'quiz':Quiz.objects.filter(classroom=ClassRoom.objects.get(id=User.objects.get(username=var).extraauth.year)),
        }
    return render(request,'Home.html',context)

def Submit(request):
    return render(request,'SubmitRoom.html')
