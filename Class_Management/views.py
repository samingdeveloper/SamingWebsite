from django.shortcuts import render,HttpResponseRedirect,get_object_or_404
from .models import *
from Assign_Management.models import *
from django.core import serializers
from django.http import Http404
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
#from LogIn_Management.models import extraauth,Tracker
from Assign_Management import views
import json
import re

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
    #var = request.user.userId
    action = request.POST.get("action","")
    request.session["classroom"] = classroom
    user_group = {"teacher":User.objects.filter(groups__name=classroom + "_Teacher"),
                     "ta":User.objects.filter(groups__name=classroom + "_TA"),
                     }
    if not request.user.is_authenticated or not(request.user.is_admin or request.user.groups.filter(name__in=[classroom + "_Teacher",classroom + "_TA"])):
        return HttpResponseRedirect('/LogOut')

    elif request.method == "POST" and action == 'add':
        email = request.POST.get("firstemail","")
        status = classroom + '_' + request.POST["country"]
        if not ClassRoom.objects.get(className=classroom).user.filter(email=email).exists() and request.POST["country"] != "CSV" and request.POST["country"] != "Cate":
            add_status = 4
            return render(request, 'Home.html', {'add_status': add_status, 'user_group': user_group,
                                                 'classname': classroom,
                                                 'classroom_creator': ClassRoom.objects.get(
                                                     className=classroom).creator.get_full_name,
                                                 'user_obj': User.objects.all(),
                                                 'user_group': user_group,
                                                 'quiz': Quiz.objects.filter(classroom__className=classroom),
                                                 'exam': Exam_Data.objects.filter(classroom__className=classroom),
                                                 })
        try:
            if request.POST["country"] == "Cate":
                add_status = 2
                if request.POST["category"] != '':
                    try:
                        Category.objects.get_or_create(name=request.POST["category"], slug=request.POST["category"])
                        add_status = 1
                    except ObjectDoesNotExist:
                        pass
                return render(request, 'Home.html', {'add_status': add_status, 'user_group': user_group,
                                                     'classname': classroom,
                                                     'classroom_creator': ClassRoom.objects.get(className=classroom).creator.get_full_name,
                                                     'user_obj': User.objects.all(),
                                                     'user_group': user_group,
                                                     'quiz': Quiz.objects.filter(classroom__className=classroom),
                                                     'exam': Exam_Data.objects.filter(classroom__className=classroom),
                                                     })
            elif request.POST["country"] == "CSV":
                add_status = 1
                csv_file = request.FILES.get('upload_testcase', False)
                if not csv_file.name.endswith('.csv'):
                    add_status = 2
                    return render(request, 'Home.html', {'add_status': add_status, 'user_group': user_group,
                                             'classname': classroom,
                                             'classroom_creator': ClassRoom.objects.get(className=classroom).creator.get_full_name,
                                             'user_obj': User.objects.all(),
                                             'user_group': user_group,
                                             'quiz': Quiz.objects.filter(classroom__className=classroom),
                                             'exam': Exam_Data.objects.filter(classroom__className=classroom),
                                             })
                elif csv_file.multiple_chunks():
                    add_status = 2
                    return render(request, 'Home.html', {'add_status': add_status, 'user_group': user_group,
                                             'classname': classroom,
                                             'classroom_creator': ClassRoom.objects.get(className=classroom).creator.get_full_name,
                                             'user_obj': User.objects.all(),
                                             'user_group': user_group,
                                             'quiz': Quiz.objects.filter(classroom__className=classroom),
                                             'exam': Exam_Data.objects.filter(classroom__className=classroom),
                                             })
                csv_data = csv_file.read().decode("utf-8")
                #print(csv_data)
                lines = csv_data.split("\n")
                for line in lines:
                    fields = line
                    #print(fields)
                    try:
                        try:
                            validate_email(fields)
                            ClassRoom.objects.get(className=classroom).user.add(User.objects.get(email=fields.rstrip()))
                        except:
                            ClassRoom.objects.get(className=classroom).user.add(User.objects.get(userId=fields.rstrip()))
                    except Exception as e:
                        #print(e)
                        continue
                return render(request, 'Home.html', {'add_status': add_status, 'user_group': user_group,
                                             'classname': classroom,
                                             'classroom_creator': ClassRoom.objects.get(className=classroom).creator.get_full_name,
                                             'user_obj': User.objects.all(),
                                             'user_group': user_group,
                                             'quiz': Quiz.objects.filter(classroom__className=classroom),
                                             'exam': Exam_Data.objects.filter(classroom__className=classroom),
                                             })
            elif request.POST["country"] == "Admin" and request.user.is_admin:
                add_status = 1
                user_obj.is_admin = True
                user_obj.save()
                return render(request, 'Home.html', {'add_status': add_status, 'user_group': user_group,
                                             'classname': classroom,
                                             'classroom_creator': ClassRoom.objects.get(className=classroom).creator.get_full_name,
                                             'user_obj': User.objects.all(),
                                             'user_group': user_group,
                                             'quiz': Quiz.objects.filter(classroom__className=classroom),
                                             'exam': Exam_Data.objects.filter(classroom__className=classroom),
                                             })
            add_status = 1
            g = Group.objects.get(name=status)
            g.user_set.add(User.objects.get(email=email))
            return render(request, 'Home.html', {'add_status': add_status, 'user_group': user_group,
                                             'classname': classroom,
                                             'classroom_creator': ClassRoom.objects.get(className=classroom).creator.get_full_name,
                                             'user_obj': User.objects.all(),
                                             'user_group': user_group,
                                             'quiz': Quiz.objects.filter(classroom__className=classroom),
                                             'exam': Exam_Data.objects.filter(classroom__className=classroom),
                                             })
        except Exception as e:
            print(e)
            add_status = 2
            return render(request, 'Home.html', {'add_status': add_status, 'user_group': user_group,
                                             'classname': classroom,
                                             'classroom_creator': ClassRoom.objects.get(className=classroom).creator.get_full_name,
                                             'user_obj': User.objects.all(),
                                             'user_group': user_group,
                                             'quiz': Quiz.objects.filter(classroom__className=classroom),
                                             'exam': Exam_Data.objects.filter(classroom__className=classroom),
                                             })

    elif request.method == "POST" and action == 'delete':
        email = request.POST.get("firstemail","")
        status = classroom + '_' + request.POST["country"]
        if ClassRoom.objects.get(className=classroom).user.filter(email=email).exists() is not True and (request.POST["country"] != "CSV" and request.POST["country"] != "Cate"):
            add_status = 4
            return render(request, 'Home.html', {'add_status': add_status, 'user_group': user_group,
                                                 'classname': classroom,
                                                 'classroom_creator': ClassRoom.objects.get(
                                                     className=classroom).creator.get_full_name,
                                                 'user_obj': User.objects.all(),
                                                 'user_group': user_group,
                                                 'quiz': Quiz.objects.filter(classroom__className=classroom),
                                                 'exam': Exam_Data.objects.filter(classroom__className=classroom),
                                                 })
        try:
            if request.POST["country"] == "Cate":
                add_status = 2
                if request.POST["category"] != '':
                    try:
                        Category.objects.get(name=request.POST["category"], slug=request.POST["category"]).delete()
                        add_status = 3
                    except ObjectDoesNotExist:
                        pass
                return render(request, 'Home.html', {'add_status': add_status, 'user_group': user_group,
                                                     'classname': classroom,
                                                     'classroom_creator': ClassRoom.objects.get(className=classroom).creator.get_full_name,
                                                     'user_obj': User.objects.all(),
                                                     'user_group': user_group,
                                                     'quiz': Quiz.objects.filter(classroom__className=classroom),
                                                     'exam': Exam_Data.objects.filter(classroom__className=classroom),
                                                     })
            elif request.POST["country"] == "CSV":
                add_status = 3
                csv_file = request.FILES.get('upload_testcase', False)
                if not csv_file.name.endswith('.csv'):
                    add_status = 2
                    return render(request, 'Home.html', {'add_status': add_status, 'user_group': user_group,
                                             'classname': classroom,
                                             'classroom_creator': ClassRoom.objects.get(className=classroom).creator.get_full_name,
                                             'user_obj': User.objects.all(),
                                             'user_group': user_group,
                                             'quiz': Quiz.objects.filter(classroom__className=classroom),
                                             'exam': Exam_Data.objects.filter(classroom__className=classroom),
                                             })
                elif csv_file.multiple_chunks():
                    add_status = 2
                    return render(request, 'Home.html', {'add_status': add_status, 'user_group': user_group,
                                             'classname': classroom,
                                             'classroom_creator': ClassRoom.objects.get(className=classroom).creator.get_full_name,
                                             'user_obj': User.objects.all(),
                                             'user_group': user_group,
                                             'quiz': Quiz.objects.filter(classroom__className=classroom),
                                             'exam': Exam_Data.objects.filter(classroom__className=classroom),
                                             })
                csv_data = csv_file.read().decode("utf-8")
                lines = csv_data.split("\n")
                from django.core.validators import validate_email
                for line in lines:
                    fields = line
                    #print(fields)
                    try:
                        try:
                            validate_email(fields)
                            ClassRoom.objects.get(className=classroom).user.remove(User.objects.get(email=fields.rstrip()))
                        except:
                            ClassRoom.objects.get(className=classroom).user.remove(User.objects.get(userId=fields.rstrip()))
                    except Exception as e:
                        #print(e)
                        continue
                return render(request, 'Home.html', {'add_status': add_status, 'user_group': user_group,
                                             'classname': classroom,
                                             'classroom_creator': ClassRoom.objects.get(className=classroom).creator.get_full_name,
                                             'user_obj': User.objects.all(),
                                             'user_group': user_group,
                                             'quiz': Quiz.objects.filter(classroom__className=classroom),
                                             'exam': Exam_Data.objects.filter(classroom__className=classroom),
                                             })

            if request.POST["country"] == "Admin" and request.user.is_admin:
                user_obj = User.objects.get(email=email)
                user_obj.is_admin = False
                user_obj.save()
                add_status = 3
                return render(request, 'Home.html', {'add_status': add_status, 'user_group': user_group,
                                             'classname': classroom,
                                             'classroom_creator': ClassRoom.objects.get(className=classroom).creator.get_full_name,
                                             'user_obj': User.objects.all(),
                                             'user_group': user_group,
                                             'quiz': Quiz.objects.filter(classroom__className=classroom),
                                             'exam': Exam_Data.objects.filter(classroom__className=classroom),
                                             })
            add_status = 3
            g = Group.objects.get(name=status)
            g.user_set.remove(User.objects.get(email=email))
            return render(request, 'Home.html', {'add_status': add_status, 'user_group': user_group,
                                             'classname': classroom,
                                             'classroom_creator': ClassRoom.objects.get(className=classroom).creator.get_full_name,
                                             'user_obj': User.objects.all(),
                                             'user_group': user_group,
                                             'quiz': Quiz.objects.filter(classroom__className=classroom),
                                             'exam': Exam_Data.objects.filter(classroom__className=classroom),
                                             })
        except Exception as e:
            #print(e)
            add_status = 2
            return render(request, 'Home.html', {'add_status': add_status, 'user_group': user_group,
                                             'classname': classroom,
                                             'classroom_creator': ClassRoom.objects.get(className=classroom).creator.get_full_name,
                                             'user_obj': User.objects.all(),
                                             'user_group': user_group,
                                             'quiz': Quiz.objects.filter(classroom__className=classroom),
                                             'exam': Exam_Data.objects.filter(classroom__className=classroom),
                                             })
        add_status = 3
        return render(request, 'Home.html', {'add_status': add_status, 'user_group': user_group,
                                             'classname': classroom,
                                             'classroom_creator': ClassRoom.objects.get(className=classroom).creator.get_full_name,
                                             'user_obj': User.objects.all(),
                                             'user_group': user_group,
                                             'quiz': Quiz.objects.filter(classroom__className=classroom),
                                             'exam': Exam_Data.objects.filter(classroom__className=classroom),
                                             })


    else:
        #print(Quiz.objects.filter(classroom=ClassRoom.objects.get(className=classroom)))
        if ClassRoom.objects.get(className=classroom).user.filter(email=request.user.email).exists() is True or (request.POST["country"] != "CSV" and request.POST["country"] != "Cate"):
            try:
                QuizTracker.objects.get(userId=request.user,classroom__className=classroom)
            except ObjectDoesNotExist:
                QuizTracker.objects.create(userId=request.user,classroom=ClassRoom.objects.get(className=classroom))
            except Exception as E:
                print(E)

        if request.user.is_admin or request.user.groups.filter(name__in=[classroom + "_Teacher",classroom + "_TA"]).exists():
            quiz_set = Quiz.objects.filter(classroom__className=classroom)
            exam_set = Exam_Data.objects.filter(classroom__className=classroom).order_by('name')
            exam_quiz_pool = Exam_Quiz.objects.filter(classroom__className=classroom)
        else:
            quiz_set = Quiz.objects.filter(classroom__className=classroom,available__lte=timezone.localtime(timezone.now()),deadline__gte=timezone.localtime(timezone.now()))
            exam_set = Exam_Data.objects.filter(classroom__className=classroom,available__lte=timezone.localtime(timezone.now()),deadline__gte=timezone.localtime(timezone.now())).order_by('name')
            exam_quiz_pool = ()
        data = serializers.serialize('json',quiz_set)
        request.session["quiz"]=json.loads(data)
        context = {
            #'var':User.objects.get(userId=var).studentYear,
            'classname':classroom,
            'classroom_creator':ClassRoom.objects.get(className=classroom).creator.get_full_name,
            'user_obj':User.objects.all(),
            'user_group': user_group,
            'quiz':quiz_set,
            'exam':exam_set,
            'exam_quiz_pool':exam_quiz_pool,
            'exam_picked':Exam_Tracker.objects.filter(exam__classroom__className=classroom, user=request.user).order_by('exam__name')
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
    elif request.method == "POST":
        import re
        classname = request.POST["classname"]
        if classname is not '' and bool(re.match('^[a-zA-Z0-9]+$',classname)):
            classroom_instance = ClassRoom.objects.create(className=classname,creator=request.user)
            classroom_instance.user.add(request.user)
            classroom_instance.save()
            return HttpResponseRedirect('/ClassRoom')
        else:
            messages.error(request, 'Classname is not valid!')
            return render(request, 'CreateClassroom.html')
    else:
        return render(request, 'CreateClassroom.html')

def EditClassroom(request,classroom):
    if not request.user.is_authenticated or not(request.user.is_admin or request.user.groups.filter(name__in=[classroom + "_Teacher",classroom + "_TA"])):
        return HttpResponseRedirect('/LogOut')
    elif request.method == "POST":
        classroom_instance = ClassRoom.objects.get(className=classroom)
        user_group = {"teacher": User.objects.filter(groups__name=classroom + '_' + "Teacher"),
                      "ta": User.objects.filter(groups__name=classroom + '_' + "TA"),
                      }
        classname = request.POST["classname"]
        creator = request.POST["creator"]
        if classname is not '' and bool(re.match('^[a-zA-Z0-9]+$',classname)):
            try:
                group = Group.objects.get(name=classroom + "_Teacher")
            except ObjectDoesNotExist:
                
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
            messages.error(request, 'Classname is not valid!')
            return render(request, 'EditClassroom.html', context)
    else:
        context={
            "classname":classroom,
            "creator":User.objects.filter(is_admin=True),
            "selected":ClassRoom.objects.get(className=classroom).creator.get_full_name,
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
    name_quiz = ["userId","Classroom"]
    for i in obj_quiz:
        name_quiz.append(i.quizTitle)
    name_quiz.append("TotalScore")
    obj_all = []
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Quiscore.csv'
    writer = csv.writer(response, csv.excel)
    response.write(u'\ufeff'.encode('utf8')) # BOM (optional...Excel needs it to open UTF-8 file properly)
    writer.writerow(
        name_quiz
    )
    QuizScore_list = list(QuizScore.objects.filter(classroom__className=classroom).exclude(userId__is_admin=True).order_by("quizId__quizTitle", "userId__userId"))

    for index, obj in enumerate(QuizScore_list):
        try:
            if QuizScore_list[index+1].userId == QuizScore_list[index].userId:
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
                obj_all.insert(0, obj.userId.userId)
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
            obj_all.insert(0, obj.userId.userId)
            writer.writerow(obj_all)
            obj_all = []
            continue
    return response

def Manual(request,classroom):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/LogOut')

    else:
        #return None
        return render(request, "./manual/index.html")

def StudentInfo(request,classroom):
    #var = request.user.userId
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/LogOut')

    elif request.method == "POST" and 'csv' in request.POST:
        return export_score_csv(classroom)

    else:
        quiz_count = Quiz.objects.filter(classroom__className=classroom).count()
        if quiz_count == 0:
            quiz_count = 1
        context = {
            #'var':User.objects.get(userId=var).studentYear,
            'classname':ClassRoom.objects.get(className=classroom),
            'User_objects':ClassRoom.objects.get(className=classroom).user.all().order_by('userId'),
            'quiz_count':quiz_count
        }
        return render(request,'ShowStudent.html',context)


def StudentScoreInfo(request,classroom,userId):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/LogOut')
    else:
        request.session['u_id'] = [userId]
        u_id = request.session['u_id']
        #var = request.user.userId
        #print(u_id[0])
        try:
            #print("try")
            if request.user.is_admin or request.user.groups.filter(name__in=[classroom + "_Teacher", classroom + "_TA"]).exists():
                quiz = Quiz.objects.filter(classroom__className=classroom)
                exam = Exam_Data.objects.filter(classroom__className=classroom)
            else:
                quiz = Quiz.objects.filter(classroom__className=classroom,available__lte=timezone.localtime(timezone.now()))
                exam = Exam_Data.objects.filter(classroom__className=classroom,available__lte=timezone.localtime(timezone.now()))
            context = {
                'var': User.objects.get(userId=userId),
                'classname': classroom,
                'User_objects': User.objects.all(),
                'u_id': {'user_name': u_id[0]},
                'quiz': quiz,
                'exam': exam,
            }
            return render(request, 'ShowScoreStudent.html', context)
        except Exception as E:
            #print('noe')
            print(E)
            return render(request, 'ShowScoreStudent.html')

def StudentQuizListInfo(request,classroom,userId,quiz_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/LogOut')
    elif (Quiz.objects.get(pk=quiz_id).available > timezone.localtime(timezone.now()) and not(request.user.is_admin or request.user.groups.filter(name__in=[classroom + "_Teacher",classroom + "_TA"]))):
        return HttpResponseRedirect('/ClassRoom/' + request.session["classroom"])
    else:
        if request.user.userId == userId or request.user.is_admin:
            if request.method == 'POST':
                title_list = request.POST.getlist("cb")
                #print(title_list)
                Upload.objects.filter(title__in=title_list).delete()
        file_list = Upload.objects.filter(user=User.objects.get(userId=userId),
                                          quiz=Quiz.objects.get(pk=quiz_id),
                                          classroom=Quiz.objects.get(pk=quiz_id).classroom
                                          )
        file_list = list(file_list)
        try:
            score_pointer = QuizScore.objects.get(quizId=Quiz.objects.get(pk=quiz_id),
                                  userId=User.objects.get(userId=userId)
                                  )
            score_pointer_render = score_pointer.code.title
        except:
            score_pointer_render = None
        context = {
            'file_list': file_list,
            'userId': userId,
            'quiz_id': quiz_id,
            'score_pointer': score_pointer_render
        }
        return render(request,'ShowQuizListStudent.html',context)

def StudentQuizInfo(request,classroom,userId,quiz_id,file_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/LogOut')

    elif (Quiz.objects.get(pk=quiz_id).available > timezone.localtime(timezone.now()) and not(request.user.is_admin or request.user.groups.filter(name__in=[classroom + "_Teacher",classroom + "_TA"]))):
        return HttpResponseRedirect('/ClassRoom/' + request.session["classroom"])

    elif request.method == 'POST' and (request.user.is_admin or request.user.groups.filter(name__in=[classroom + "_Teacher",classroom + "_TA"])) or request.method == 'POST' and request.user.userId == userId:
        if userId != request.user.userId and not request.user.is_admin:
            return HttpResponseRedirect("/ClassRoom/"+classroom)
        score_pointer = QuizScore.objects.get(quizId=Quiz.objects.get(pk=quiz_id),
                                              userId=User.objects.get(userId=userId)
                                              )
        if Quiz.objects.get(pk=quiz_id).mode == "Scoring":
            score_pointer.total_score = Upload.objects.get(pk=file_id).score
        else:
            score_pointer.passOrFail = Upload.objects.get(pk=file_id).score
        score_pointer.code = Upload.objects.get(pk=file_id)
        score_pointer.save()
        return HttpResponseRedirect("/ClassRoom/"+classroom+'/StudentInfo/'+userId+'/'+quiz_id)

    else:
        if userId != request.user.userId and not request.user.is_admin:
            return HttpResponseRedirect("/ClassRoom/"+classroom)
        file = Upload.objects.get(user=User.objects.get(userId=userId),
                                          quiz=Quiz.objects.get(pk=quiz_id),
                                          classroom=Quiz.objects.get(pk=quiz_id).classroom,
                                        pk=file_id
                                          )
        quiz_to_show = Quiz.objects.get(pk=quiz_id)
        u_id = User.objects.get(userId=request.session['u_id'][0]).userId
        try:
            file.Uploadfile.open(mode="rb")
            code_to_show = file.Uploadfile.read().replace(b"\r\r\n",b"\r\n").decode()
            file.Uploadfile.close()
        except Exception as e:
            #print(e)
            code_to_show = ""
        var = request.user.userId
        context = {
            'var':User.objects.get(userId=userId),
            'classname':ClassRoom.objects.get(className=classroom),
            'User_objects':User.objects.all(),
            'u_id': {'user_name': u_id, 'userId': userId},
            'quiz_id': quiz_id,
            'quiz_to_show':quiz_to_show,
            "code_to_show":code_to_show,
            "upload_time":file.uploadTime,
            "file_title":file.title,
            "file_id":file.id,
        }
        return render(request,'ShowQuizStudent.html',context)

def StudentExamQuizList(request,classroom,userId,exam_data_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/LogOut')
    elif (Exam_Data.objects.get(pk=exam_data_id).available > timezone.localtime(timezone.now()) and not(request.user.is_admin or request.user.groups.filter(name__in=[classroom + "_Teacher",classroom + "_TA"]))):
        return HttpResponseRedirect('/ClassRoom/' + request.session["classroom"])
    else:
        context = {
            'exam_quizes': Exam_Quiz.objects.filter(title__in=Exam_Tracker.objects.get(exam__pk=exam_data_id).picked,classroom__className=classroom),
            'userId': userId,
            'exam_data_id': exam_data_id
        }
        return render(request,'StudentExamQuizList.html',context)

def StudentExamQuizFiles(request,classroom,userId,exam_data_id,exam_quiz_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/LogOut')
    elif (Exam_Data.objects.get(pk=exam_data_id).available > timezone.localtime(timezone.now()) or not(request.user.userId == userId) and not(request.user.is_admin or request.user.groups.filter(name__in=[classroom + "_Teacher",classroom + "_TA"]))):
        return HttpResponseRedirect('/ClassRoom/' + request.session["classroom"])
    else:
        if request.method == 'POST':
            title_list = request.POST.getlist("cb")
            #print(title_list)
            Exam_Upload.objects.filter(title__in=title_list).delete()
        file_list = list(Exam_Upload.objects.filter(user__userId=userId,quiz__pk=exam_quiz_id))
        try:
            score_pointer = Exam_Score.objects.get(quiz__pk=exam_quiz_id, user__userId=userId)
            score_pointer_render = score_pointer.code.title
        except:
            score_pointer_render = None
        context = {
            'file_list': file_list,
            'userId': userId,
            'exam_data_id': exam_data_id,
            'exam_quiz_id': exam_quiz_id,
            'score_pointer': score_pointer_render
        }
        return render(request,'StudentExamQuizFiles.html',context)

def StudentExamQuiz(request,classroom,userId,exam_data_id,exam_quiz_id,file_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/LogOut')

    elif (Exam_Data.objects.get(pk=exam_data_id).available > timezone.localtime(timezone.now()) and not(request.user.is_admin or request.user.groups.filter(name__in=[classroom + "_Teacher",classroom + "_TA"]))):
        return HttpResponseRedirect('/ClassRoom/' + request.session["classroom"])

    elif request.method == 'POST' and (request.user.is_admin or request.user.groups.filter(name__in=[classroom + "_Teacher",classroom + "_TA"])) or request.method == 'POST' and request.user.userId == userId:
        if userId != request.user.userId and not(request.user.is_admin or request.user.groups.filter(name__in=[classroom + "_Teacher",classroom + "_TA"])):
            return HttpResponseRedirect("/ClassRoom/"+classroom)
        score_pointer = Exam_Score.objects.get(quiz__pk=exam_quiz_id)
        if Exam_Quiz.objects.get(pk=exam_quiz_id).mode == "Scoring":
            score_pointer.total_score = Exam_Upload.objects.get(pk=file_id).score
        else:
            score_pointer.passOrFail = Exam_Upload.objects.get(pk=file_id).score
        score_pointer.code = Exam_Upload.objects.get(pk=file_id)
        score_pointer.save()
        return HttpResponseRedirect("/ClassRoom/"+classroom+'/StudentInfo/'+userId+'/Examination/'+exam_data_id+'/'+exam_quiz_id+'/')

    else:
        if userId != request.user.userId and not(request.user.is_admin or request.user.groups.filter(name__in=[classroom + "_Teacher",classroom + "_TA"])):
            return HttpResponseRedirect("/ClassRoom/"+classroom)
        file = Exam_Upload.objects.get(pk=file_id)
        quiz_to_show = Exam_Quiz.objects.get(pk=exam_quiz_id)
        u_id = User.objects.get(userId=request.session['u_id'][0]).userId
        try:
            file.Uploadfile.open(mode="rb")
            code_to_show = file.Uploadfile.read().replace(b"\r\r\n",b"\r\n").decode()
            file.Uploadfile.close()
        except Exception as e:
            #print(e)
            code_to_show = ""
        context = {
            'classname':ClassRoom.objects.get(className=classroom),
            'User_objects':User.objects.all(),
            'u_id': {'user_name': u_id, 'userId': userId},
            'exam_data_id': exam_data_id,
            'exam_quiz_id': exam_quiz_id,
            'quiz_to_show':quiz_to_show,
            "code_to_show":code_to_show,
            "upload_time":file.uploadTime,
            "file_title":file.title,
            "file_id":file.id,
        }
        return render(request,'StudentExamQuiz.html',context)

def Submit(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/LogOut')
    else:
        return render(request,'SubmitRoom.html')
