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
    user_group = {"teacher":User.objects.filter(groups__name=ClassRoom.objects.get(id=User.objects.get(username=var).studentYear).className + '_' + "Teacher"),
             "ta":User.objects.filter(groups__name=ClassRoom.objects.get(id=User.objects.get(username=var).studentYear).className + '_' + "TA"),
             }
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/LogOut')

    elif request.method == "POST" and action == 'add':
        email = request.POST.get("firstemail","")
        status = ClassRoom.objects.get(id=User.objects.get(username=var).studentYear).className + '_' + request.POST["country"]
        try:
            user_obj = User.objects.get(email=email)
            add_status = 1
            if request.POST["country"] == "Admin" and request.user.is_admin:
                user_obj.admin = True
                user_obj.save()
                return render(request, 'Home.html', {'add_status': add_status,'user_group': user_group})
            g = Group.objects.get(name=status)
            g.user_set.add(user_obj)
            return render(request, 'Home.html', {'add_status': add_status,'user_group': user_group})
        except Exception as e:
            print(e)
            add_status = 2
            return render(request, 'Home.html', {'add_status': add_status,'user_group': user_group})

    elif request.method == "POST" and action == 'delete':
        email = request.POST.get("firstemail","")
        status = ClassRoom.objects.get(id=User.objects.get(username=var).studentYear).className + '_' + request.POST["country"]
        try:
            user_obj = User.objects.get(email=email)
            add_status = 3
            if request.POST["country"] == "Admin" and request.user.is_admin:
                user_obj.admin = False
                user_obj.save()
                return render(request, 'Home.html', {'add_status': add_status,'user_group': user_group})
            g = Group.objects.get(name=status)
            g.user_set.remove(user_obj)
            return render(request, 'Home.html', {'add_status': add_status, 'user_group': user_group})
        except Exception as e:
            print(e)
            add_status = 2
            return render(request, 'Home.html', {'add_status': add_status,'user_group': user_group})
        add_status = 3
        return render(request, 'Home.html', {'add_status': add_status, 'user_group': user_group})

    elif User.objects.get(username=var).studentYear:

        context = {
            'var':User.objects.get(username=var).studentYear,
            'classname':ClassRoom.objects.get(id=User.objects.get(username=var).studentYear),
            'user_obj':User.objects.all(),
            'user_group': user_group,
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
        if username != var and not request.user.is_admin:
            return HttpResponseRedirect("/ClassRoom/Home")
        try:
            score = QuizScore.objects.filter(studentId=u_id[0], classroom=ClassRoom.objects.get(id=User.objects.get(username=var).studentYear))
            x = 0
            y = 0
            for i in score:
                #print(i.total_score)
                #print(i.passOrFail)
                x += i.total_score + i.passOrFail
                y += i.max_score
            context = {
                'var': User.objects.get(username=var).studentYear,
                'classname': ClassRoom.objects.get(id=User.objects.get(username=var).studentYear),
                'User_objects': User.objects.all(),
                'u_id': {'user_name': u_id[0]},
                'totalscore': x,
                'maxscore': y,
            }
            return render(request, 'ShowScoreStudent.html', context)
        except:
            print('noe')
            return render(request, 'ShowScoreStudent.html')

def StudentQuizListInfo(request,username,quiz_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/LogOut')
    else:
        if request.method == 'POST':
            title_list = request.POST.getlist("cb")
            print(title_list)
            Upload.objects.filter(title__in=title_list).delete()
        file_list = Upload.objects.filter(user=User.objects.get(username=username),
                                          quiz=Quiz.objects.get(pk=quiz_id),
                                          classroom=Quiz.objects.get(pk=quiz_id).classroom
                                          )
        file_list = list(file_list)
        context = {
            'file_list': file_list,
            'username': username,
            'quiz_id': quiz_id
        }
        return render(request,'ShowQuizListStudent.html',context)

def StudentQuizInfo(request,username,quiz_id,title):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/LogOut')
    else:
        if username != request.user.username and not request.user.is_admin:
            return HttpResponseRedirect("/ClassRoom/Home")
        file = Upload.objects.get(user=User.objects.get(username=username),
                                          quiz=Quiz.objects.get(pk=quiz_id),
                                          classroom=Quiz.objects.get(pk=quiz_id).classroom,
                                          title=title
                                          )
        quiz_to_show = Quiz.objects.get(pk=quiz_id)
        u_id = User.objects.get(username=request.session['u_id'][0]).studentId
        try:
            file.Uploadfile.open(mode="r")
            code_to_show = file.Uploadfile.read()
            file.Uploadfile.close()
        except Exception as e:
            print(e)
            code_to_show = ""
        var = request.user.username
        context = {
            'var':User.objects.get(username=var).studentYear,
            'classname':ClassRoom.objects.get(id=User.objects.get(username=var).studentYear),
            'User_objects':User.objects.all(),
            'u_id': {'user_name': u_id},
            'quiz_to_show':quiz_to_show,
            "code_to_show":code_to_show,
            "upload_time":file.uploadTime,
            "title":file.title,
        }
        return render(request,'ShowQuizStudent.html',context)

def Submit(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/LogOut')
    else:
        return render(request,'SubmitRoom.html')