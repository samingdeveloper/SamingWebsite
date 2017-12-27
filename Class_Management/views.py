from django.shortcuts import render,HttpResponseRedirect,get_object_or_404
from .models import *
from Assign_Management.models import Upload
from django.http import Http404
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
#from LogIn_Management.models import extraauth,Tracker
from Assign_Management import views

User = get_user_model()
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
    add_status = 0
    var = request.user.username
    action = request.POST.get("action","")
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/LogOut')

    elif request.method == "POST" and action == 'add':
        email = request.POST.get("firstemail","")
        status = request.POST["country"]
        try:
            user_obj = User.objects.get(email=email)
            g = Group.objects.get(name=status)
            if status == "Admin":
                user_obj.is_admin = True
                user_obj.save()
            g.user_set.add(user_obj)
            #print(user_obj)
        except:
            add_status = 2
            return render(request, 'Home.html', {'add_status': add_status})
        #print(status)
        add_status = 1
        return render(request,'Home.html',{'add_status':add_status})

    elif request.method == "POST" and action == 'delete':
        email = request.POST.get("firstemail","")
        status = request.POST["country"]
        try:
            user_obj = User.objects.get(email=email)
            g = Group.objects.get(name=status)
            if status == "Admin":
                user_obj.is_admin = False
                user_obj.save()
            g.user_set.remove(user_obj)
            #print(user_obj)
        except:
            add_status = 2
            return render(request, 'Home.html', {'add_status': add_status})
        #print(status)
        add_status = 3
        return render(request,'Home.html',{'add_status':add_status})

    elif User.objects.get(username=var).studentYear:

        context = {
            'var':User.objects.get(username=var).studentYear,
            'classname':ClassRoom.objects.get(id=User.objects.get(username=var).studentYear),
            'user_obj':User.objects.all(),
            #'quiz':Quiz.objects.filter(classroom=ClassRoom.objects.get(id=User.objects.get(username=var).studentYear)),
        }
        return render(request,'Home.html',context)


def About(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/LogOut')
    else:
        return render(request,'About.html')

def StudentInfo(request):
    var = request.user.username
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/LogOut')
    else:
        #y = User.objects.all().values_list('year', flat=True)
        '''z = extraauth.objects.all().values_list('studentId', flat=True)
        x = User.objects.all()
        for i in x:
            if i.studentYear == 1:
                print(i.studentYear)
        #quiz = Quiz.objects.filter(classroom=ClassRoom.objects.get(id=User.objects.get(username=var).studentYear))
        print(z)'''
        temp_class = ClassRoom.objects.get(id=User.objects.get(username=var).studentYear)
        if temp_class.className == "FRA141":
            user_year = 1
        elif temp_class.className == "FRA241":
            user_year = 2
        elif temp_class.className == "FRA341":
            user_year = 3
        elif temp_class.className == "FRA441":
            user_year = 4
        quiz_count = Quiz.objects.filter(classroom=temp_class).count()
        if quiz_count == 0:
            quiz_count = 1
        context = {
            'var':User.objects.get(username=var).studentYear,
            'classname':ClassRoom.objects.get(id=User.objects.get(username=var).studentYear),
            'user_year':user_year,
            'User_objects':User.objects.all(),
            'quiz_count':quiz_count
            #'quiz':Quiz.objects.filter(classroom=ClassRoom.objects.get(id=User.objects.get(username=var).studentYear)),
        }
        return render(request,'ShowStudent.html',context)


def StudentScoreInfo(request,username):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/LogOut')
    else:
        request.session['u_id'] = [username]
        u_id = request.session['u_id']
        var = request.user.username
        context = {
            'var':User.objects.get(username=var).studentYear,
            'classname':ClassRoom.objects.get(id=User.objects.get(username=var).studentYear),
            'User_objects':User.objects.all(),
            'u_id': {'user_name':u_id[0]},
        }
        return render(request,'ShowScoreStudent.html',context)


def StudentQuizInfo(request,username,quiz_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/LogOut')
    else:
        quiz_to_show = Quiz.objects.get(pk=quiz_id)
        u_id = request.session['u_id']
        #file_to_show = str(u_id[0]) + '_' + str(quiz_to_show.quizTitle.replace(' ','_')) + quiz_id + '_' + 'script' + '.py'
        try:
            #f = open('./media/'+file_to_show, 'r')
            code_to_show = QuizScore.objects.get(quizId=quiz_id, studentId=u_id[0], classroom=quiz_to_show.classroom,
                                            ).code
            #f.close()
        except:
            code_to_show = ""
        #print(file_to_show)
        #print(code_write_to_show)
        var = request.user.username
        context = {
            'var':User.objects.get(username=var).studentYear,
            'classname':ClassRoom.objects.get(id=User.objects.get(username=var).studentYear),
            'User_objects':User.objects.all(),
            'u_id': {'user_name': u_id[0]},
            'quiz_to_show':quiz_to_show,
            "code_to_show":code_to_show,
        }
        return render(request,'ShowQuizStudent.html',context)

def Submit(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/LogOut')
    else:
        return render(request,'SubmitRoom.html')