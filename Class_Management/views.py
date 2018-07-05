from django.shortcuts import render,HttpResponseRedirect,get_object_or_404
from .models import *
from Assign_Management.models import Upload
from django.core import serializers
from django.http import Http404
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
#from LogIn_Management.models import extraauth,Tracker
from Assign_Management import views
import json

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

def ClassSelect(request):
    context={
        "list_class": ClassRoom.objects.all()
    }
    return render(request, "Inside.html", context)

def Home(request,classroom):
    add_status = 0
    var = request.user.username
    action = request.POST.get("action","")
    request.session["classroom"] = classroom
    user_group = {"teacher":User.objects.filter(groups__name=classroom + '_' + "Teacher"),
                     "ta":User.objects.filter(groups__name=classroom + '_' + "TA"),
                     }
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/LogOut')

    elif request.method == "POST" and action == 'add':
        email = request.POST.get("firstemail","")
        status = classroom + '_' + request.POST["country"]
        if ClassRoom.objects.get(className=classroom).user.filter(email=email).exists() is not True and request.POST["country"] != "CSV":
            add_status = 4
            return render(request, 'Home.html', {'add_status': add_status, 'user_group': user_group,
                                                 'classname': classroom,
                                                 'classroom_creator': ClassRoom.objects.get(
                                                     className=classroom).creator.get_full_name,
                                                 'user_obj': User.objects.all(),
                                                 'user_group': user_group,
                                                 'quiz': Quiz.objects.filter(
                                                     classroom=ClassRoom.objects.get(className=classroom)),
                                                 })
        try:
            if request.POST["country"] == "CSV":
                add_status = 1
                csv_file = request.FILES.get('upload_testcase', False)
                if not csv_file.name.endswith('.csv'):
                    add_status = 2
                    return render(request, 'Home.html', {'add_status': add_status, 'user_group': user_group,
                                             'classname': classroom,
                                             'classroom_creator': ClassRoom.objects.get(className=classroom).creator.get_full_name,
                                             'user_obj': User.objects.all(),
                                             'user_group': user_group,
                                             'quiz': Quiz.objects.filter(classroom=ClassRoom.objects.get(className=classroom)),
                                             })
                elif csv_file.multiple_chunks():
                    add_status = 2
                    return render(request, 'Home.html', {'add_status': add_status, 'user_group': user_group,
                                             'classname': classroom,
                                             'classroom_creator': ClassRoom.objects.get(className=classroom).creator.get_full_name,
                                             'user_obj': User.objects.all(),
                                             'user_group': user_group,
                                             'quiz': Quiz.objects.filter(classroom=ClassRoom.objects.get(className=classroom)),
                                             })
                csv_data = csv_file.read().decode("utf-8")
                #print(csv_data)
                lines = csv_data.split("\n")
                for line in lines:
                    fields = line
                    #print(fields)
                    try:
                        ClassRoom.objects.get(className=classroom).user.add(User.objects.get(studentId=fields.rstrip()))
                    except Exception as e:
                        #print(e)
                        continue
                return render(request, 'Home.html', {'add_status': add_status, 'user_group': user_group,
                                             'classname': classroom,
                                             'classroom_creator': ClassRoom.objects.get(className=classroom).creator.get_full_name,
                                             'user_obj': User.objects.all(),
                                             'user_group': user_group,
                                             'quiz': Quiz.objects.filter(classroom=ClassRoom.objects.get(className=classroom)),
                                             })
            user_obj = User.objects.get(email=email)
            add_status = 1
            if request.POST["country"] == "Admin" and request.user.is_admin:
                user_obj.is_admin = True
                user_obj.save()
                return render(request, 'Home.html', {'add_status': add_status, 'user_group': user_group,
                                             'classname': classroom,
                                             'classroom_creator': ClassRoom.objects.get(className=classroom).creator.get_full_name,
                                             'user_obj': User.objects.all(),
                                             'user_group': user_group,
                                             'quiz': Quiz.objects.filter(classroom=ClassRoom.objects.get(className=classroom)),
                                             })
            g = Group.objects.get(name=status)
            g.user_set.add(user_obj)
            return render(request, 'Home.html', {'add_status': add_status, 'user_group': user_group,
                                             'classname': classroom,
                                             'classroom_creator': ClassRoom.objects.get(className=classroom).creator.get_full_name,
                                             'user_obj': User.objects.all(),
                                             'user_group': user_group,
                                             'quiz': Quiz.objects.filter(classroom=ClassRoom.objects.get(className=classroom)),
                                             })
        except Exception as e:
            #print(e)
            add_status = 2
            return render(request, 'Home.html', {'add_status': add_status, 'user_group': user_group,
                                             'classname': classroom,
                                             'classroom_creator': ClassRoom.objects.get(className=classroom).creator.get_full_name,
                                             'user_obj': User.objects.all(),
                                             'user_group': user_group,
                                             'quiz': Quiz.objects.filter(classroom=ClassRoom.objects.get(className=classroom)),
                                             })

    elif request.method == "POST" and action == 'delete':
        email = request.POST.get("firstemail","")
        status = classroom + '_' + request.POST["country"]
        if ClassRoom.objects.get(className=classroom).user.filter(email=email).exists() is not True and request.POST["country"] != "CSV":
            add_status = 4
            return render(request, 'Home.html', {'add_status': add_status, 'user_group': user_group,
                                                 'classname': classroom,
                                                 'classroom_creator': ClassRoom.objects.get(
                                                     className=classroom).creator.get_full_name,
                                                 'user_obj': User.objects.all(),
                                                 'user_group': user_group,
                                                 'quiz': Quiz.objects.filter(
                                                     classroom=ClassRoom.objects.get(className=classroom)),
                                                 })
        try:
            if request.POST["country"] == "CSV" and request.user.is_admin:
                add_status = 3
                csv_file = request.FILES.get('upload_testcase', False)
                if not csv_file.name.endswith('.csv'):
                    add_status = 2
                    return render(request, 'Home.html', {'add_status': add_status, 'user_group': user_group,
                                             'classname': classroom,
                                             'classroom_creator': ClassRoom.objects.get(className=classroom).creator.get_full_name,
                                             'user_obj': User.objects.all(),
                                             'user_group': user_group,
                                             'quiz': Quiz.objects.filter(classroom=ClassRoom.objects.get(className=classroom)),
                                             })
                elif csv_file.multiple_chunks():
                    add_status = 2
                    return render(request, 'Home.html', {'add_status': add_status, 'user_group': user_group,
                                             'classname': classroom,
                                             'classroom_creator': ClassRoom.objects.get(className=classroom).creator.get_full_name,
                                             'user_obj': User.objects.all(),
                                             'user_group': user_group,
                                             'quiz': Quiz.objects.filter(classroom=ClassRoom.objects.get(className=classroom)),
                                             })
                csv_data = csv_file.read().decode("utf-8")
                lines = csv_data.split("\n")
                for line in lines:
                    fields = line
                    #print(fields)
                    try:
                        if '@' in fields: ClassRoom.objects.get(className=classroom).user.remove(User.objects.get(email=fields.rstrip()))
                        else: ClassRoom.objects.get(className=classroom).user.remove(User.objects.get(studentId=fields.rstrip()))
                    except Exception as e:
                        #print(e)
                        continue
                return render(request, 'Home.html', {'add_status': add_status, 'user_group': user_group,
                                             'classname': classroom,
                                             'classroom_creator': ClassRoom.objects.get(className=classroom).creator.get_full_name,
                                             'user_obj': User.objects.all(),
                                             'user_group': user_group,
                                             'quiz': Quiz.objects.filter(classroom=ClassRoom.objects.get(className=classroom)),
                                             })
            user_obj = User.objects.get(email=email)
            add_status = 3
            if request.POST["country"] == "Admin" and request.user.is_admin:
                user_obj.is_admin = False
                user_obj.save()
                return render(request, 'Home.html', {'add_status': add_status, 'user_group': user_group,
                                             'classname': classroom,
                                             'classroom_creator': ClassRoom.objects.get(className=classroom).creator.get_full_name,
                                             'user_obj': User.objects.all(),
                                             'user_group': user_group,
                                             'quiz': Quiz.objects.filter(classroom=ClassRoom.objects.get(className=classroom)),
                                             })
            g = Group.objects.get(name=status)
            g.user_set.remove(user_obj)
            return render(request, 'Home.html', {'add_status': add_status, 'user_group': user_group,
                                             'classname': classroom,
                                             'classroom_creator': ClassRoom.objects.get(className=classroom).creator.get_full_name,
                                             'user_obj': User.objects.all(),
                                             'user_group': user_group,
                                             'quiz': Quiz.objects.filter(classroom=ClassRoom.objects.get(className=classroom)),
                                             })
        except Exception as e:
            #print(e)
            add_status = 2
            return render(request, 'Home.html', {'add_status': add_status, 'user_group': user_group,
                                             'classname': classroom,
                                             'classroom_creator': ClassRoom.objects.get(className=classroom).creator.get_full_name,
                                             'user_obj': User.objects.all(),
                                             'user_group': user_group,
                                             'quiz': Quiz.objects.filter(classroom=ClassRoom.objects.get(className=classroom)),
                                             })
        add_status = 3
        return render(request, 'Home.html', {'add_status': add_status, 'user_group': user_group,
                                             'classname': classroom,
                                             'classroom_creator': ClassRoom.objects.get(className=classroom).creator.get_full_name,
                                             'user_obj': User.objects.all(),
                                             'user_group': user_group,
                                             'quiz': Quiz.objects.filter(classroom=ClassRoom.objects.get(className=classroom)),
                                             })


    else:
        #print(Quiz.objects.filter(classroom=ClassRoom.objects.get(className=classroom)))
        x=Quiz.objects.filter(classroom=ClassRoom.objects.get(className=classroom))
        data = serializers.serialize('json',x)
        request.session["quiz"]=json.loads(data)
        context = {
            #'var':User.objects.get(username=var).studentYear,
            'classname':classroom,
            'classroom_creator':ClassRoom.objects.get(className=classroom).creator.get_full_name,
            'user_obj':User.objects.all(),
            'user_group': user_group,
            'quiz':x,
        }
        return render(request,'Home.html',context)

def About(request, classroom):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/LogOut')
    else:
        return render(request,'About.html')

def GenerateClassroom(request):
    if not request.user.is_authenticated or not request.user.is_admin:
        return HttpResponseRedirect('/LogOut')
    elif request.method == "POST" and request.user.is_admin:
        classname = request.POST["classname"]
        classroom_instance = ClassRoom.objects.create(className=classname,creator=request.user)
        classroom_instance.user.add(request.user)
        classroom_instance.save()
        return HttpResponseRedirect('/ClassRoom')
    else:
        return render(request, 'CreateClassroom.html')

def EditClassroom(request,classroom):
    if not request.user.is_authenticated or not request.user.is_admin:
        return HttpResponseRedirect('/LogOut')
    elif request.method == "POST" and request.user.is_admin:
        classroom_instance = ClassRoom.objects.get(className=classroom)
        user_group = {"teacher": User.objects.filter(groups__name=classroom + '_' + "Teacher"),
                      "ta": User.objects.filter(groups__name=classroom + '_' + "TA"),
                      }
        classname = request.POST["classname"]
        creator = request.POST["creator"]
        group = Group.objects.get(name=classroom + "_Teacher")
        Group.objects.filter(name=group.name).update(name=classname + "_Teacher")
        group = Group.objects.get(name=classroom + "_TA")
        Group.objects.filter(name=group.name).update(name=classname + "_TA")
        classroom_instance.className = classname
        classroom_instance.creator = User.objects.get(pk=creator)
        classroom_instance.save()
        return HttpResponseRedirect('/ClassRoom')
    else:
        context={
            "classname":classroom,
            "creator":User.objects.filter(is_admin=True)
        }
        return render(request, 'EditClassroom.html', context)

def DeleteClassroom(request,classroom):
    if not request.user.is_authenticated or not request.user.is_admin:
        return HttpResponseRedirect('/LogOut')
    else:
        #print(ClassRoom.objects.get(className=classroom))
        ClassRoom.objects.get(className=classroom).delete()
        return HttpResponseRedirect('/ClassRoom')

def export_score_csv(classroom):
    import csv
    from django.utils.encoding import smart_str
    from django.http import HttpResponse
    obj_quiz = Quiz.objects.filter(classroom__className=classroom).order_by("quizTitle")
    name_quiz = ["StudentId","Classroom"]
    for i in obj_quiz:
        name_quiz.append(i.quizTitle)
    name_quiz.append("MaxScore")
    obj_all = []
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Quiscore.csv'
    writer = csv.writer(response, csv.excel)
    response.write(u'\ufeff'.encode('utf8')) # BOM (optional...Excel needs it to open UTF-8 file properly)
    writer.writerow(
        name_quiz
    )
    QuizScore_list = list(QuizScore.objects.filter(classroom__className=classroom).order_by("quizId__quizTitle", "studentId__studentId"))

    for index, obj in enumerate(QuizScore_list):
        try:
            if QuizScore_list[index+1].studentId == QuizScore_list[index].studentId:
                obj_all.append(obj.passOrFail+obj.total_score)
                #print(obj_all)
                continue
            else:
                #print("end")
                obj_all.append(obj.passOrFail + obj.total_score)
                if len(obj_quiz) - len(obj_all) != 0:
                    for i in range(0, len(obj_quiz) - len(obj_all)):
                        obj_all.append(0)
                obj_all.append(sum(obj_all))
                obj_all.insert(0, obj.classroom.className)
                obj_all.insert(0, obj.studentId.studentId)
                writer.writerow(smart_str(obj_all))
                obj_all = []
                continue
        except Exception as E:
            #print(E)
            obj_all.append(obj.passOrFail + obj.total_score)
            if len(obj_quiz) - len(obj_all) != 0:
                for i in range(0, len(obj_quiz) - len(obj_all)):
                    obj_all.append(0)
            obj_all.append(sum(obj_all))
            obj_all.insert(0, obj.classroom.className)
            obj_all.insert(0, obj.studentId.studentId)
            writer.writerow(obj_all)
            obj_all = []
            continue
    return response

def StudentInfo(request,classroom):
    #var = request.user.username
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/LogOut')

    elif request.method == "POST" and 'csv' in request.POST:
        return export_score_csv(classroom)

    else:
        quiz_count = Quiz.objects.filter(classroom=ClassRoom.objects.get(className=classroom)).count()
        if quiz_count == 0:
            quiz_count = 1
        context = {
            #'var':User.objects.get(username=var).studentYear,
            'classname':ClassRoom.objects.get(className=classroom),
            'User_objects':ClassRoom.objects.get(className=classroom).user.all(),
            'quiz_count':quiz_count
        }
        return render(request,'ShowStudent.html',context)


def StudentScoreInfo(request,classroom,username):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/LogOut')
    else:
        request.session['u_id'] = [username]
        u_id = request.session['u_id']
        #var = request.user.username
        #print(u_id[0])
        try:
            #print("try")
            score = QuizScore.objects.filter(studentId=User.objects.get(username=u_id[0]), classroom=ClassRoom.objects.get(className=classroom))
            quiz = Quiz.objects.filter(classroom=ClassRoom.objects.get(className=classroom))
            x = 0
            y = 0
            for i in score:
                #print(i.total_score)
                #print(i.passOrFail)
                x += i.total_score + i.passOrFail
                y += i.max_score
            context = {
                'var': User.objects.get(username=username),
                'classname': classroom,
                'User_objects': User.objects.all(),
                'u_id': {'user_name': u_id[0]},
                'totalscore': x,
                'maxscore': y,
                'quiz': quiz,
            }
            return render(request, 'ShowScoreStudent.html', context)
        except:
            #print('noe')
            return render(request, 'ShowScoreStudent.html')

def StudentQuizListInfo(request,classroom,username,quiz_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/LogOut')
    else:
        if request.user.username == username or request.user.is_admin:
            if request.method == 'POST':
                title_list = request.POST.getlist("cb")
                #print(title_list)
                Upload.objects.filter(title__in=title_list).delete()
        file_list = Upload.objects.filter(user=User.objects.get(username=username),
                                          quiz=Quiz.objects.get(pk=quiz_id),
                                          classroom=Quiz.objects.get(pk=quiz_id).classroom
                                          )
        file_list = list(file_list)
        try:
            score_pointer = QuizScore.objects.get(quizId=Quiz.objects.get(pk=quiz_id),
                                  studentId=User.objects.get(username=username)
                                  )
            score_pointer_render = score_pointer.code.title
        except:
            score_pointer_render = None
        context = {
            'file_list': file_list,
            'username': username,
            'quiz_id': quiz_id,
            'score_pointer': score_pointer_render
        }
        return render(request,'ShowQuizListStudent.html',context)

def StudentQuizInfo(request,classroom,username,quiz_id,title):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/LogOut')

    elif request.method == 'POST' and request.user.is_admin or request.method == 'POST' and request.user.username == username:
        if username != request.user.username and not request.user.is_admin:
            return HttpResponseRedirect("/ClassRoom/"+classroom)
        score_pointer = QuizScore.objects.get(quizId=Quiz.objects.get(pk=quiz_id),
                                              studentId=User.objects.get(username=username)
                                              )
        if Quiz.objects.get(pk=quiz_id).mode == "Scoring":
            score_pointer.total_score = Upload.objects.get(title=title).score
        else:
            score_pointer.passOrFail = Upload.objects.get(title=title).score
        score_pointer.code = Upload.objects.get(title=title)
        score_pointer.save()
        return HttpResponseRedirect("/ClassRoom/"+classroom+'/StudentInfo/'+username+'/'+quiz_id)

    else:
        if username != request.user.username and not request.user.is_admin:
            return HttpResponseRedirect("/ClassRoom/"+classroom)
        file = Upload.objects.get(user=User.objects.get(username=username),
                                          quiz=Quiz.objects.get(pk=quiz_id),
                                          classroom=Quiz.objects.get(pk=quiz_id).classroom,
                                          title=title
                                          )
        quiz_to_show = Quiz.objects.get(pk=quiz_id)
        u_id = User.objects.get(username=request.session['u_id'][0]).studentId
        try:
            file.Uploadfile.open(mode="rb")
            code_to_show = file.Uploadfile.read().replace(b"\r\r\n",b"\r\n").decode()
            file.Uploadfile.close()
        except Exception as e:
            #print(e)
            code_to_show = ""
        var = request.user.username
        context = {
            'var':User.objects.get(username=username),
            'classname':ClassRoom.objects.get(className=classroom),
            'User_objects':User.objects.all(),
            'u_id': {'user_name': u_id, 'username': username},
            'quiz_id': quiz_id,
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