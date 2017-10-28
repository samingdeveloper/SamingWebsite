from django.shortcuts import render
from .models import ClassRoom
from django.http import Http404
from django.contrib.auth.models import User

def index(request):
    list_classroom = ClassRoom.objects.all()
    context = {
        'list_classroom': list_classroom
    }
    return render(request, 'Classroom.html', context)

def inside(request,className):
    try:
        quiz = ClassRoom.objects.get(pk=className)
    except ClassRoom.DoesNotExist:
        raise Http404("Classroom does not exist")
    return render(request, 'Inside.html', {'quiz': quiz})

def Home(request):
    var = request.session['var']
    if User.objects.get(username=var).extraauth.year:
        context = {
            'var':User.objects.get(username=var).extraauth.year
        }
    return render(request,'SelectClassroom.html',context)

def Submit(request):
    return render(request,'SubmitRoom.html')