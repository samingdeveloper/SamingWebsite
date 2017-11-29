from django.shortcuts import render,HttpResponseRedirect,get_object_or_404
from .models import ClassRoom,Quiz
from django.http import Http404
from django.contrib.auth.models import User
from LogIn_Management.models import extraauth,Tracker

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
    var = request.user.username
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/LogOut')
    elif User.objects.get(username=var).extraauth.year:
        context = {
            'var':User.objects.get(username=var).extraauth.year,
            'classname':ClassRoom.objects.get(id=User.objects.get(username=var).extraauth.year),
            #'quiz':Quiz.objects.filter(classroom=ClassRoom.objects.get(id=User.objects.get(username=var).extraauth.year)),
        }
        return render(request,'Home.html',context)

def StudentInfo(request):
    var = request.user.username
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/LogOut')
    else:
        #y = User.objects.all().values_list('year', flat=True)
        '''z = extraauth.objects.all().values_list('studentId', flat=True)
        x = User.objects.all()
        for i in x:
            if i.extraauth.year == 1:
                print(i.extraauth.year)
        #quiz = Quiz.objects.filter(classroom=ClassRoom.objects.get(id=User.objects.get(username=var).extraauth.year))
        print(z)'''
        temp_class = ClassRoom.objects.get(id=User.objects.get(username=var).extraauth.year)
        if temp_class.className == "FRA141":
            user_year = 1
        elif temp_class.className == "FRA241":
            user_year = 2
        elif temp_class.className == "FRA341":
            user_year = 3
        elif temp_class.className == "FRA441":
            user_year = 4
        context = {
            'var':User.objects.get(username=var).extraauth.year,
            'classname':ClassRoom.objects.get(id=User.objects.get(username=var).extraauth.year),
            'user_year':user_year,
            'User_objects':User.objects.all(),
            #'quiz':Quiz.objects.filter(classroom=ClassRoom.objects.get(id=User.objects.get(username=var).extraauth.year)),
        }
        return render(request,'ShowStudent.html',context)


def StudentScoreInfo(request,username):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/LogOut')
    else:
        var = request.user.username
        context = {
            'var':User.objects.get(username=var).extraauth.year,
            'classname':ClassRoom.objects.get(id=User.objects.get(username=var).extraauth.year),
            'User_objects':User.objects.all(),
        }
        return render(request,'ShowScoreStudent.html',context)


def StudentQuizInfo(request,username,quiz_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/LogOut')
    else:
        var = request.user.username
        context = {
            'var':User.objects.get(username=var).extraauth.year,
            'classname':ClassRoom.objects.get(id=User.objects.get(username=var).extraauth.year),
            'User_objects':User.objects.all(),
        }
        return render(request,'ShowQuizStudent.html',context)

def Submit(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/LogOut')
    else:
        return render(request,'SubmitRoom.html')