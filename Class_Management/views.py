from django.shortcuts import render,HttpResponseRedirect
from .models import ClassRoom,Quiz
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
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/LogOut')
    elif User.objects.get(username=var).extraauth.year:
        context = {
            'var':User.objects.get(username=var).extraauth.year,
            'classname':ClassRoom.objects.get(id=User.objects.get(username=var).extraauth.year),
            'quiz':Quiz.objects.filter(classroom=ClassRoom.objects.get(id=User.objects.get(username=var).extraauth.year)),
        }
        return render(request,'Home.html',context)

def Submit(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/LogOut')
    else:
        return render(request,'SubmitRoom.html')