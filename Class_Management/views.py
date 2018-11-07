from django.shortcuts import render,HttpResponseRedirect,get_object_or_404
from .models import *
from Assign_Management.Lib import my_globals
from Assign_Management.models import *
from django.core import serializers
from django.http import Http404
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
#from LogIn_Management.models import extraauth,Tracker
from Assign_Management import views
import json
import re
import pytz
import datetime

User = get_user_model()
@login_required
def index(request):
    list_classroom = ClassRoom.objects.all()
    context = {
        'list_classroom': list_classroom
    }
    return render(request, 'Classroom.html', context)

@login_required
def inside(request,className):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/LogOut')
    try:
        quiz = ClassRoom.objects.get(pk=className)
    except ClassRoom.DoesNotExist:
        raise Http404("Classroom does not exist")
    return render(request, 'Inside.html', {'quiz': quiz})

@login_required
def ClassSelect(request):
    context={
        "list_class": ClassRoom.objects.all()
    }
    return render(request, "Inside.html", context)

@login_required
def Home(request,classroom):
    add_status = 0
    #var = request.user.userId
    action = request.POST.get("action","")
    request.session["classroom"] = classroom
    user_group = {"teacher":User.objects.filter(groups__name=classroom + "_Teacher"),
                     "ta":User.objects.filter(groups__name=classroom + "_TA"),
                     }
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/LogOut')

    elif request.user.is_admin or request.user.groups.filter(
            name__in=[classroom + "_Teacher", classroom + "_TA"]).exists():
        quiz_set = ClassRoom.objects.get(
            className=classroom).quizes.all()  # Quiz.objects.filter(classroom__className=classroom).order_by('quizTitle')
        exam_set = Exam_Data.objects.filter(classroom__className=classroom).order_by('name')
        exam_quiz_pool = Exam_Quiz.objects.all()
        quiz_pool_set =  Quiz.objects.all()
        exam_picked =  Exam_Tracker.objects.filter(exam__classroom__className=classroom, user=request.user).order_by('exam__name')
        current_time = datetime.datetime.now(tz=pytz.timezone('Asia/Bangkok'))
    else:
        quiz_set = Quiz.objects.filter(classroom__className=classroom,
                                       available__lte=timezone.localtime(timezone.now()),
                                       deadline__gte=timezone.localtime(timezone.now()))
        exam_set = Exam_Data.objects.filter(classroom__className=classroom,
                                            available__lte=timezone.localtime(timezone.now()),
                                            deadline__gte=timezone.localtime(timezone.now())).order_by('name')
        exam_quiz_pool = ()
        quiz_pool_set = ()
        exam_picked = Exam_Tracker.objects.filter(exam__classroom__className=classroom, user=request.user).order_by('exam__name')
        current_time = datetime.datetime.now(tz=pytz.timezone('Asia/Bangkok'))

    if request.method == "POST" and action == 'add':
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
                                                 'quiz': quiz_set,
                                                 'exam': exam_set,
                                                 'exam_quiz_pool': exam_quiz_pool,
                                                 'quiz_pool': quiz_pool_set,
                                                 'exam_picked': exam_picked,
                                                 'current_time': current_time
                                                 })
        try:
            if request.POST["country"] == "Cate":
                add_status = 2
                if request.POST["category"] != '':
                    try:
                        if re.match('^[^,]*$',request.POST["category"]) and request.POST["category"].replace(' ','') != '':
                            Category.objects.get_or_create(name=request.POST["category"], slug=request.POST["category"])
                            add_status = 1
                        else:
                            add_status = 2
                    except ObjectDoesNotExist:
                        pass
                return render(request, 'Home.html', {'add_status': add_status, 'user_group': user_group,
                                                     'classname': classroom,
                                                     'classroom_creator': ClassRoom.objects.get(className=classroom).creator.get_full_name,
                                                     'user_obj': User.objects.all(),
                                                     'user_group': user_group,
                                                     'quiz': quiz_set,
                                                     'exam': exam_set,
                                                     'exam_quiz_pool': exam_quiz_pool,
                                                     'quiz_pool': quiz_pool_set,
                                                     'exam_picked': exam_picked,
                                                     'current_time': current_time
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
                                             'quiz': quiz_set,
                                             'exam': exam_set,
                                             'exam_quiz_pool': exam_quiz_pool,
                                             'quiz_pool': quiz_pool_set,
                                             'exam_picked': exam_picked,
                                             'current_time': current_time
                                             })
                elif csv_file.multiple_chunks():
                    add_status = 2
                    return render(request, 'Home.html', {'add_status': add_status, 'user_group': user_group,
                                             'classname': classroom,
                                             'classroom_creator': ClassRoom.objects.get(className=classroom).creator.get_full_name,
                                             'user_obj': User.objects.all(),
                                             'user_group': user_group,
                                             'quiz': quiz_set,
                                             'exam': exam_set,
                                             'exam_quiz_pool': exam_quiz_pool,
                                             'quiz_pool': quiz_pool_set,
                                             'exam_picked': exam_picked,
                                             'current_time': current_time
                                             })
                csv_data = csv_file.read().decode("utf-8")
                #print(csv_data)
                lines = csv_data.split("\n")
                from django.core.validators import validate_email
                counter = 0
                total = 0
                failed_counter = -1
                failed_list = []
                for num,line in enumerate(lines):
                    fields = line.replace(',', '\t').split('\t')
                    #print(fields)
                    try:
                        if not bool(re.match('^[a-zA-Z0-9\w.@+_-]+$', str(fields[0]).rstrip())):
                            try:
                                raise ValueError(fields[0][:-1].rstrip())
                            except Exception as e:
                                print(e)
                            failed_counter += 1
                            failed_list.append(fields[0])
                            continue
                        elif len(fields)==1:
                            try:
                                validate_email(fields[0][:-1].rstrip())
                                ClassRoom.objects.get(className=classroom).user.add(User.objects.get(email=fields[0][:-1].rstrip()))
                                counter += 1
                                #print("success")
                            except ObjectDoesNotExist:
                                failed_counter += 1
                                failed_list.append(fields[0].rstrip())
                            except Exception as E:
                                #print(E)
                                try:
                                    ClassRoom.objects.get(className=classroom).user.add(User.objects.get(userId=fields[0][:-1].rstrip()))
                                    counter += 1
                                except ObjectDoesNotExist:
                                    failed_counter += 1
                                    failed_list.append(fields[0].rstrip())
                        else:
                            try:
                                validate_email(fields[0].rstrip())
                                ClassRoom.objects.get(className=classroom).user.add(User.objects.get(email=fields[0].rstrip()))
                                counter += 1
                                #print("success")
                            except ObjectDoesNotExist:
                                failed_counter += 1
                                failed_list.append(fields[0].rstrip())
                            except Exception as E:
                                #print(E)
                                try:
                                    ClassRoom.objects.get(className=classroom).user.add(User.objects.get(userId=fields[0].rstrip()))
                                    counter += 1
                                except ObjectDoesNotExist:
                                    failed_counter += 1
                                    failed_list.append(fields[0].rstrip())
                    except Exception as e:
                        print(e)
                        failed_counter += 1
                        failed_list.append(fields[0])
                        continue
                return render(request, 'Home.html', {'add_status': add_status, 'user_group': user_group,
                                             'classname': classroom,
                                             'classroom_creator': ClassRoom.objects.get(className=classroom).creator.get_full_name,
                                             'user_obj': User.objects.all(),
                                             'user_group': user_group,
                                             'quiz': quiz_set,
                                             'exam': exam_set,
                                             'exam_quiz_pool': exam_quiz_pool,
                                             'quiz_pool': quiz_pool_set,
                                             'exam_picked': exam_picked,
                                             'current_time': current_time
                                             })
            elif not (request.user.is_admin or request.user.groups.filter(name=classroom + "_Teacher")):
                add_status = 4
                return render(request, 'Home.html', {'add_status': add_status, 'user_group': user_group,
                                                     'classname': classroom,
                                                     'classroom_creator': ClassRoom.objects.get(
                                                         className=classroom).creator.get_full_name,
                                                     'user_obj': User.objects.all(),
                                                     'user_group': user_group,
                                                     'quiz': quiz_set,
                                                     'exam': exam_set,
                                                     'exam_quiz_pool': exam_quiz_pool,
                                                     'quiz_pool': quiz_pool_set,
                                                     'exam_picked': exam_picked,
                                                     'current_time': current_time
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
                                             'quiz': quiz_set,
                                             'exam': exam_set,
                                             'exam_quiz_pool': exam_quiz_pool,
                                             'quiz_pool': quiz_pool_set,
                                             'exam_picked': exam_picked,
                                             'current_time': current_time
                                             })
            add_status = 1
            g = Group.objects.get(name=status)
            g.user_set.add(User.objects.get(email=email))
            return render(request, 'Home.html', {'add_status': add_status, 'user_group': user_group,
                                             'classname': classroom,
                                             'classroom_creator': ClassRoom.objects.get(className=classroom).creator.get_full_name,
                                             'user_obj': User.objects.all(),
                                             'user_group': user_group,
                                             'quiz': quiz_set,
                                             'exam': exam_set,
                                             'exam_quiz_pool': exam_quiz_pool,
                                             'quiz_pool': quiz_pool_set,
                                             'exam_picked': exam_picked,
                                             'current_time': current_time
                                             })
        except Exception as e:
            print(e)
            add_status = 2
            return render(request, 'Home.html', {'add_status': add_status, 'user_group': user_group,
                                             'classname': classroom,
                                             'classroom_creator': ClassRoom.objects.get(className=classroom).creator.get_full_name,
                                             'user_obj': User.objects.all(),
                                             'user_group': user_group,
                                             'quiz': quiz_set,
                                             'exam': exam_set,
                                             'exam_quiz_pool': exam_quiz_pool,
                                             'quiz_pool': quiz_pool_set,
                                             'exam_picked': exam_picked,
                                             'current_time': current_time
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
                                                 'quiz': quiz_set,
                                                 'exam': exam_set,
                                                 'exam_quiz_pool': exam_quiz_pool,
                                                 'quiz_pool': quiz_pool_set,
                                                 'exam_picked': exam_picked,
                                                 'current_time': current_time
                                                 })
        try:
            if request.POST["country"] == "Cate":
                add_status = 2
                if request.POST["category"] != '':
                    try:
                        if re.match('^[^,]*$',request.POST["category"]):
                            Category.objects.get(name=request.POST["category"], slug=request.POST["category"]).delete()
                            add_status = 3
                        else:
                            add_status = 2
                    except ObjectDoesNotExist:
                        pass
                return render(request, 'Home.html', {'add_status': add_status, 'user_group': user_group,
                                                     'classname': classroom,
                                                     'classroom_creator': ClassRoom.objects.get(className=classroom).creator.get_full_name,
                                                     'user_obj': User.objects.all(),
                                                     'user_group': user_group,
                                                     'quiz': quiz_set,
                                                     'exam': exam_set,
                                                     'exam_quiz_pool': exam_quiz_pool,
                                                     'quiz_pool': quiz_pool_set,
                                                     'exam_picked': exam_picked,
                                                     'current_time': current_time
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
                                             'quiz': quiz_set,
                                             'exam': exam_set,
                                             'exam_quiz_pool': exam_quiz_pool,
                                             'quiz_pool': quiz_pool_set,
                                             'exam_picked': exam_picked,
                                             'current_time': current_time
                                             })
                elif csv_file.multiple_chunks():
                    add_status = 2
                    return render(request, 'Home.html', {'add_status': add_status, 'user_group': user_group,
                                             'classname': classroom,
                                             'classroom_creator': ClassRoom.objects.get(className=classroom).creator.get_full_name,
                                             'user_obj': User.objects.all(),
                                             'user_group': user_group,
                                             'quiz': quiz_set,
                                             'exam': exam_set,
                                             'exam_quiz_pool': exam_quiz_pool,
                                             'quiz_pool': quiz_pool_set,
                                             'exam_picked': exam_picked,
                                             'current_time': current_time
                                             })
                csv_data = csv_file.read().decode("utf-8")
                lines = csv_data.split("\n")
                from django.core.validators import validate_email
                counter = 0
                total = 0
                failed_counter = -1
                failed_list = []
                for num, line in enumerate(lines):
                    fields = line.replace(',', '\t').split('\t')
                    # print(fields)
                    try:
                        if not bool(re.match('^[a-zA-Z0-9\w.@+_-]+$', str(fields[0]).rstrip())):
                            try:
                                raise ValueError(fields[0][:-1].rstrip())
                            except Exception as e:
                                print(e)
                            failed_counter += 1
                            failed_list.append(fields[0])
                            continue
                        elif len(fields)==1:
                            try:
                                validate_email(fields[0][:-1].rstrip())
                                ClassRoom.objects.get(className=classroom).user.remove(User.objects.get(email=fields[0][:-1].rstrip()))
                                counter += 1
                                #print("success")
                            except ObjectDoesNotExist:
                                failed_counter += 1
                                failed_list.append(fields[0].rstrip())
                            except Exception as E:
                                #print(E)
                                try:
                                    ClassRoom.objects.get(className=classroom).user.remove(User.objects.get(userId=fields[0][:-1].rstrip()))
                                    counter += 1
                                except ObjectDoesNotExist:
                                    failed_counter += 1
                                    failed_list.append(fields[0].rstrip())
                        else:
                            try:
                                validate_email(fields[0].rstrip())
                                ClassRoom.objects.get(className=classroom).user.remove(User.objects.get(email=fields[0].rstrip()))
                                counter += 1
                                #print("success")
                            except ObjectDoesNotExist:
                                failed_counter += 1
                                failed_list.append(fields[0].rstrip())
                            except Exception as E:
                                #print(E)
                                try:
                                    ClassRoom.objects.get(className=classroom).user.remove(User.objects.get(userId=fields[0].rstrip()))
                                    counter += 1
                                except ObjectDoesNotExist:
                                    failed_counter += 1
                                    failed_list.append(fields[0].rstrip())
                    except Exception as e:
                        print(e)
                        failed_counter += 1
                        failed_list.append(fields[0])
                        continue
                return render(request, 'Home.html', {'add_status': add_status, 'user_group': user_group,
                                             'classname': classroom,
                                             'classroom_creator': ClassRoom.objects.get(className=classroom).creator.get_full_name,
                                             'user_obj': User.objects.all(),
                                             'user_group': user_group,
                                             'quiz': quiz_set,
                                             'exam': exam_set,
                                             'exam_quiz_pool': exam_quiz_pool,
                                             'quiz_pool': quiz_pool_set,
                                             'exam_picked': exam_picked,
                                             'current_time': current_time
                                             })
            elif not(request.user.is_admin or request.user.groups.filter(name=classroom + "_Teacher")):
                add_status = 4
                return render(request, 'Home.html', {'add_status': add_status, 'user_group': user_group,
                                                     'classname': classroom,
                                                     'classroom_creator': ClassRoom.objects.get(
                                                         className=classroom).creator.get_full_name,
                                                     'user_obj': User.objects.all(),
                                                     'user_group': user_group,
                                                     'quiz': quiz_set,
                                                     'exam': exam_set,
                                                     'exam_quiz_pool': exam_quiz_pool,
                                                     'quiz_pool': quiz_pool_set,
                                                     'exam_picked': exam_picked,
                                                     'current_time': current_time
                                                     })
            elif request.POST["country"] == "Admin" and request.user.is_admin:
                user_obj = User.objects.get(email=email)
                user_obj.is_admin = False
                user_obj.save()
                add_status = 3
                return render(request, 'Home.html', {'add_status': add_status, 'user_group': user_group,
                                             'classname': classroom,
                                             'classroom_creator': ClassRoom.objects.get(className=classroom).creator.get_full_name,
                                             'user_obj': User.objects.all(),
                                             'user_group': user_group,
                                             'quiz': quiz_set,
                                             'exam': exam_set,
                                             'exam_quiz_pool': exam_quiz_pool,
                                             'quiz_pool': quiz_pool_set,
                                             'exam_picked': exam_picked,
                                             'current_time': current_time
                                             })
            add_status = 3
            g = Group.objects.get(name=status)
            g.user_set.remove(User.objects.get(email=email))
            return render(request, 'Home.html', {'add_status': add_status, 'user_group': user_group,
                                             'classname': classroom,
                                             'classroom_creator': ClassRoom.objects.get(className=classroom).creator.get_full_name,
                                             'user_obj': User.objects.all(),
                                             'user_group': user_group,
                                             'quiz': quiz_set,
                                             'exam': exam_set,
                                             'exam_quiz_pool': exam_quiz_pool,
                                             'quiz_pool': quiz_pool_set,
                                             'exam_picked': exam_picked,
                                             'current_time': current_time
                                             })
        except Exception as e:
            #print(e)
            add_status = 2
            return render(request, 'Home.html', {'add_status': add_status, 'user_group': user_group,
                                             'classname': classroom,
                                             'classroom_creator': ClassRoom.objects.get(className=classroom).creator.get_full_name,
                                             'user_obj': User.objects.all(),
                                             'user_group': user_group,
                                             'quiz': quiz_set,
                                             'exam': exam_set,
                                             'exam_quiz_pool': exam_quiz_pool,
                                             'quiz_pool': quiz_pool_set,
                                             'exam_picked': exam_picked,
                                             'current_time': current_time
                                             })
        add_status = 3
        return render(request, 'Home.html', {'add_status': add_status, 'user_group': user_group,
                                             'classname': classroom,
                                             'classroom_creator': ClassRoom.objects.get(className=classroom).creator.get_full_name,
                                             'user_obj': User.objects.all(),
                                             'user_group': user_group,
                                             'quiz': quiz_set,
                                             'exam': exam_set,
                                             'exam_quiz_pool': exam_quiz_pool,
                                             'quiz_pool': quiz_pool_set,
                                             'exam_picked': exam_picked,
                                             'current_time': current_time
                                             })


    else:
        #print(Quiz.objects.filter(classroom=ClassRoom.objects.get(className=classroom)))
        if ClassRoom.objects.get(className=classroom).user.filter(email=request.user.email).exists() is True or (request.POST.get("country",None) != "CSV" and request.POST.get("country",None) != "Cate"):
            try:
                QuizTracker.objects.get(userId=request.user,classroom__className=classroom)
            except ObjectDoesNotExist:
                QuizTracker.objects.create(userId=request.user,classroom=ClassRoom.objects.get(className=classroom))
            except Exception as E:
                print(E)
        """
            if request.user.is_admin or request.user.groups.filter(name__in=[classroom + "_Teacher",classroom + "_TA"]).exists():
                quiz_set = ClassRoom.objects.get(className=classroom).quizes.all()#Quiz.objects.filter(classroom__className=classroom).order_by('quizTitle')
                exam_set = Exam_Data.objects.filter(classroom__className=classroom).order_by('name')
                exam_quiz_pool = Exam_Quiz.objects.all()
            else:
                quiz_set = Quiz.objects.filter(classroom__className=classroom,available__lte=timezone.localtime(timezone.now()),deadline__gte=timezone.localtime(timezone.now()))
                exam_set = Exam_Data.objects.filter(classroom__className=classroom,available__lte=timezone.localtime(timezone.now()),deadline__gte=timezone.localtime(timezone.now())).order_by('name')
                exam_quiz_pool = Exam_Quiz.objects.all()
        """
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
            'quiz_pool': quiz_pool_set,
            'exam_picked': exam_picked,
            'current_time': current_time
        }
        return render(request,'Home.html',context)

@login_required
def About(request, classroom):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/LogOut')
    else:
        return render(request,'About.html')

@login_required
def GenerateClassroom(request):
    if not request.user.is_authenticated or not request.user.is_admin:
        return HttpResponseRedirect('/LogOut')
    elif request.method == "POST":
        import re
        classname = request.POST["classname"]
        if classname is not '' and bool(re.match('^[a-zA-Z0-9\w.@+_-]+$',classname)):
            classroom_instance = ClassRoom.objects.create(className=classname,creator=request.user)
            classroom_instance.user.add(request.user)
            classroom_instance.save()
            return HttpResponseRedirect('/ClassRoom')
        else:
            messages.error(request, 'Classname is not valid!')
            return render(request, 'CreateClassroom.html')
    else:
        return render(request, 'CreateClassroom.html')

@login_required
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
        if classname is not '' and bool(re.match('^[a-zA-Z0-9\w.@+_-]+$',classname)):
            from django.db import IntegrityError
            try:
                group_teacher = Group.objects.get(name=classroom + "_Teacher")
                group_ta = Group.objects.get(name=classroom + "_TA")
            except ObjectDoesNotExist:
                classroom_instance.className = classname
                classroom_instance.creator = User.objects.get(pk=creator)
                classroom_instance.save()
                return HttpResponseRedirect('/ClassRoom')
            try:
                Group.objects.filter(name=group_teacher.name).update(name=classname + "_Teacher")
            except IntegrityError:
                Group.objects.filter(name=group_teacher.name).delete()
            try:
                Group.objects.filter(name=group_ta.name).update(name=classname + "_TA")
            except IntegrityError:
                Group.objects.filter(name=group_ta.name).delete()
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

@login_required
def DeleteClassroom(request,classroom):
    if not request.user.is_authenticated or not request.user.is_admin:
        return HttpResponseRedirect('/LogOut')
    else:
        #print(ClassRoom.objects.get(className=classroom))
        ClassRoom.objects.get(className=classroom).delete()
        return HttpResponseRedirect('/ClassRoom')

def export_score_csv(classroom):
    import csv
    import datetime
    #from django.utils.encoding import smart_str
    from django.utils import timezone
    from django.http import HttpResponse

    timezone.make_aware(datetime.datetime.now(), timezone.get_default_timezone())
    t = timezone.localtime(timezone.now())  # offset-awared datetime
    t.astimezone(timezone.utc).replace(tzinfo=None)
    obj_quiz = Quiz.objects.filter(classroom__className=classroom, available__lte=t).order_by("quizTitle")
    obj_exam = Exam_Data.objects.filter(classroom__className=classroom, available__lte=t).order_by("name")
    name_quiz = ["userId","Classroom"]
    max_all = 0
    for i in obj_quiz:
        name_quiz.append(i.quizTitle)
        max_all += i.max_score
    for i in obj_exam:
        name_quiz.append(i.name)
        max_all += i.max_score
    name_quiz.append("TotalScore")
    name_quiz.append("MaxScore")
    obj_all = []
    #count = -1
    #start = 0
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Quiscore.csv'
    writer = csv.writer(response, csv.excel)
    response.write(u'\ufeff'.encode('utf8')) # BOM (optional...Excel needs it to open UTF-8 file properly)
    writer.writerow(
        name_quiz
    )
    #QuizScore_list = list(QuizScore.objects.filter(classroom__className=classroom).order_by("quizId__quizTitle", "userId__userId"))#.exclude(userId__is_admin=True, userId__groups__name__in=[classroom+"_Teacher", classroom+"_TA"]).order_by("quizId__quizTitle", "userId__userId"))
    #ExamScore_list = list(Exam_Score.objects.filter(exam__classroom__className=classroom).order_by("exam__name", "user__userId"))#.exclude(user__is_admin=True, user__groups__name__in=[classroom+"_Teacher", classroom+"_TA"]).order_by("exam__name", "user__userId"))
    for class_user in ClassRoom.objects.get(className=classroom).user.all().order_by("userId").exclude(is_admin=True).exclude(groups__name__in=[classroom+"_Teacher", classroom+"_TA"]):
        for title in name_quiz[2:-2]:
            try:
                Quiz_Score = QuizScore.objects.get(quizId__quizTitle=title,userId__userId=class_user)
                Quiz_Inst = Quiz.objects.get(quizTitle=title,classroom__className=classroom)
                if Quiz_Score.passOrFail+Quiz_Score.total_score > Quiz_Inst.max_score:
                    obj_all.append(Quiz_Inst.max_score)
                else:
                    obj_all.append(Quiz_Score.passOrFail+Quiz_Score.total_score)
            except ObjectDoesNotExist:
                try:
                    ExamScore = Exam_Score.objects.get(exam__name=title,user__userId=class_user)
                    ExamInst = Exam_Data.objects.get(name=title, classroom__className=classroom)
                    if ExamScore.passOrFail+ExamScore.total_score > ExamInst.max_score:
                        obj_all.append(ExamInst.max_score)
                    else:
                        obj_all.append(ExamScore.passOrFail+ExamScore.total_score)
                except ObjectDoesNotExist:
                    obj_all.append(0)
        obj_all.append(sum(obj_all))
        obj_all.append(max_all)
        obj_all.insert(0, classroom)
        obj_all.insert(0, class_user)
        writer.writerow(obj_all)
        obj_all = []
    return response
    #for index, obj in enumerate(QuizScore_list):
    #    count+=1
    #    try:
    #        if QuizScore_list[index+1].userId == QuizScore_list[index].userId:
    #            if obj.quizId.quizTitle != name_quiz[2+count]:
    #                obj_all.append(0)
    #                for i in name_quiz[3+count:-2]:
    #                    if obj.quizId.quizTitle == i:
    #                        obj_all.append(obj.passOrFail + obj.total_score)
    #                        break
    #                    obj_all.append(0)
    #                    #continue
    #            else:
    #                obj_all.append(obj.passOrFail+obj.total_score)
    #                #print(obj_all)
    #                #continue
    #        else:
    #            #print("end")
    #            if obj.quizId.quizTitle != name_quiz[2+count]:
    #                for i in name_quiz[3+count:-2]:
    #                    if obj.quizId.quizTitle == i:
    #                        obj_all.append(obj.passOrFail + obj.total_score)
    #                        break
    #                    obj_all.append(0)
    #                    #continue
    #            else:
    #                obj_all.append(obj.passOrFail+obj.total_score)
    #            if len(obj_quiz) - len(obj_all) != 0:
    #                for i in range(0, len(obj_quiz) - len(obj_all)):
    #                    obj_all.append(0)
    #            try:
    #                res = my_globals.exam_score(ExamScore_list[start:],count,name_quiz,obj_exam,start)
    #                obj_all.append(res["obj_all"])
    #                start = res["start"]
    #            except TypeError:
    #                obj_all.append(0)
    #            #raise ValueError(obj_all,start)
    #            obj_all.append(sum(obj_all))
    #            obj_all.append(max_all)
    #            obj_all.insert(0, obj.classroom.className)
    #            obj_all.insert(0, obj.userId.userId)
    #            writer.writerow(obj_all)
    #            obj_all = []
    #            count = -1
    #            #continue
    #    except IndexError:
    #        if obj.quizId.quizTitle != name_quiz[2 + count]:
    #            #obj_all.append(0)
    #            for i in name_quiz[3+count:-2]:
    #                if obj.quizId.quizTitle == i:
    #                    obj_all.append(obj.passOrFail + obj.total_score)
    #                    break
    #                obj_all.append(0)
    #                #continue
    #        else:
    #            obj_all.append(obj.passOrFail + obj.total_score)
    #            # print(obj_all)
    #            #continue
    #        if len(obj_quiz) - len(obj_all) != 0:
    #            for i in range(0, len(obj_quiz) - len(obj_all)):
    #                obj_all.append(0)
    #        try:
    #            res = my_globals.exam_score(ExamScore_list[start:], count, name_quiz, obj_exam, start)
    #            obj_all.append(res["obj_all"])
    #            start = res["start"]
    #        except TypeError:
    #            obj_all.append(0)
    #        #raise ValueError(obj_all, start)
    #        obj_all.append(sum(obj_all))
    #        obj_all.append(max_all)
    #        obj_all.insert(0, obj.classroom.className)
    #        obj_all.insert(0, obj.userId.userId)
    #        writer.writerow(obj_all)
    #        obj_all = []
    #        count = -1
    #        #continue
    #return response

@login_required
def Manual(request,classroom):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/LogOut')

    elif not(request.user.is_admin or request.user.groups.filter(name__in=[classroom + "_Teacher",classroom + "_TA"])):
        return HttpResponseRedirect('/ClassRoom/' + request.session["classroom"])

    else:
        #return None
        return render(request, "./manual/index.html")

@login_required
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

@login_required
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

@login_required
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

@login_required
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

@login_required
def StudentExamQuizList(request,classroom,userId,exam_data_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/LogOut')
    elif (Exam_Data.objects.get(pk=exam_data_id).available > timezone.localtime(timezone.now()) and not(request.user.is_admin or request.user.groups.filter(name__in=[classroom + "_Teacher",classroom + "_TA"]))):
        return HttpResponseRedirect('/ClassRoom/' + request.session["classroom"])
    else:
        context = {
            'exam_quizes': Exam_Quiz.objects.filter(title__in=Exam_Tracker.objects.get(exam__pk=exam_data_id,user__userId=request.user).picked),#,classroom__className=classroom),
            'userId': userId,
            'exam_data_id': exam_data_id
        }
        return render(request,'StudentExamQuizList.html',context)

@login_required
def StudentExamQuizFiles(request,classroom,userId,exam_data_id,exam_quiz_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/LogOut')
    elif (((Exam_Data.objects.get(pk=exam_data_id).available > timezone.localtime(timezone.now())) or not(request.user.userId == userId)) and not(request.user.is_admin or request.user.groups.filter(name__in=[classroom + "_Teacher",classroom + "_TA"]))):
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

@login_required
def StudentExamQuiz(request,classroom,userId,exam_data_id,exam_quiz_id,file_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/LogOut')

    elif (Exam_Data.objects.get(pk=exam_data_id).available > timezone.localtime(timezone.now()) and not(request.user.is_admin or request.user.groups.filter(name__in=[classroom + "_Teacher",classroom + "_TA"]))):
        return HttpResponseRedirect('/ClassRoom/' + request.session["classroom"])

    elif request.method == 'POST' and (request.user.is_admin or request.user.groups.filter(name__in=[classroom + "_Teacher",classroom + "_TA"])) or request.method == 'POST' and request.user.userId == userId:
        if userId != request.user.userId and not(request.user.is_admin or request.user.groups.filter(name__in=[classroom + "_Teacher",classroom + "_TA"])):
            return HttpResponseRedirect("/ClassRoom/"+classroom)
        score_pointer = Exam_Score.objects.get(quiz__pk=exam_quiz_id,user__userId=userId)
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
