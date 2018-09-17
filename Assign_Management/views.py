from django.shortcuts import render, HttpResponseRedirect, redirect
from django.contrib.auth.decorators import login_required
#from django.http import HttpResponse
#from django.template import loader
#from django.middleware.csrf import CsrfViewMiddleware
from Class_Management.models import *
from Assign_Management.models import *
from Assign_Management.storage import OverwriteStorage
from django.contrib.auth import get_user_model
import sys,os,datetime,importlib,unittest,timeout_decorator,mosspy,contextlib
from io import StringIO
#from RestrictedPython import compile_restricted,utility_builtins,limited_builtins
#from RestrictedPython.Guards import safe_builtins
from unittest import TextTestRunner
from django.utils import timezone
from django.utils.crypto import get_random_string
#from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.exceptions import ObjectDoesNotExist
from .Lib import my_globals

User = get_user_model()
# Create your views here.

sys.path.append(os.getcwd()+"/media")

#################################################### Utility ####################################################
def str_to_class(str):
    return getattr(sys.modules[__name__], str)

@contextlib.contextmanager
def stdoutIO(stdout=None): # Get exec print output.
    old = sys.stdout
    if stdout is None:
        stdout = StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old

#################################################### Create Assignment ####################################################
def CreateAssignment(request):
    if not request.user.is_authenticated or not request.user.is_admin:
        return HttpResponseRedirect('/LogOut')
    else:
        return render(request,'CreateAssignment.html')


def AssignmentDetail(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/LogOut')
    return render(request, 'Home.html')


@login_required
def GenerateAssign(request,classroom):
    if not request.user.is_authenticated or not(request.user.is_admin or request.user.groups.filter(name__in=[classroom + "_Teacher",classroom + "_TA"])):
        return HttpResponseRedirect('/LogOut')
    elif request.method == "POST": #and request.FILES['upload_testcase']:
        try:
            if request.POST['asname'] == '':
                raise ValueError("Assignment must have a name!")
            elif request.POST['test_code'] == '' or request.POST['upload_testcase'] == '':
                raise ValueError("Test code and Test case must not blank!")
            elif request.POST['dateAvailable'] == '':
                raise ValueError("Please specific available date.")
            elif request.POST['dateInput'] == '':
                raise ValueError("Please specific deadline.")
            code_template = request.POST.get('upload_template', '')

#################################################### Check Testcase ####################################################
            test_code = request.POST.get('test_code', '')
            test_case = request.POST.get('upload_testcase', '')
            class case: num = 0
            def assert_equal(actual, expected, points=0, level=0):
                case.num += 1
                eval(compile(my_globals.string(case.num, actual, expected, points, level), 'defstr', 'exec'))
            # Exec
            libs=None
            for case_line in test_case.splitlines():
                if case_line.startswith('#lib') and len(case_line[5:]) != 0:
                    libs = case_line[5:].split(',')
            restricted_globals = dict(__builtins__=my_globals.mgb(globals(), libs))
            eval(compile(test_code+'\n'+test_case, 'gradingstr', 'exec'), restricted_globals, locals())
########################################################################################################################

            OSS = OverwriteStorage()
            var = request.user.userId
            Assignment = request.POST.get('asname', '')
            Assignment_Detail = request.POST.get('asdetail', '')
            Deadline = request.POST.get('dateInput', '')
            Available = request.POST.get('dateAvailable', '')
            Hint = request.POST.get('hint','')
            Cate = request.POST.get('quiz_category', '')
            Timer = request.POST.get('timer','')
            MaxScore = float(request.POST.get('quiz_max_score', ''))
            #dsa = 'upload_testcase' in request.POST and request.POST['upload_testcase']
            mode = request.POST.get('mode','')
            GenerateAssign_instance = Quiz.objects.create(quizTitle=Assignment, quizDetail=Assignment_Detail, deadline=Deadline, available=Available, max_score=MaxScore, category=Category.objects.get(name=Cate), text_template_content=code_template, text_testcode_content=test_code, text_testcase_content=test_case  ,hint=Hint, mode=mode, classroom=ClassRoom.objects.get(className=classroom))
            GenerateAssign_instance_temp = Quiz.objects.get(quizTitle=Assignment, quizDetail=Assignment_Detail, deadline=Deadline ,available=Available, max_score=MaxScore, category=Category.objects.get(name=Cate), text_template_content=code_template, text_testcode_content=test_code, text_testcase_content=test_case  ,hint=Hint, mode=mode, classroom=ClassRoom.objects.get(className=classroom))
            get_tracker = QuizTracker.objects.filter(classroom=GenerateAssign_instance_temp.classroom) #reference at QuizTracker
            for k in get_tracker:
                QuizStatus.objects.update_or_create(quizId=GenerateAssign_instance_temp,
                                                    userId=k.userId,
                                                    classroom=GenerateAssign_instance_temp.classroom,
                                                    status=False,
                                                    )
            if Timer != '':
                #print("timeryes")
                Timer_temp = ''
                for i in Timer:
                    if i == ' ':
                        pass
                    else:
                        Timer_temp += i
                Timer = Timer_temp
                o = Timer.split(':')
                x = int(o[0]) * 3600 + int(o[1]) * 60 + int(o[2])
                for j in get_tracker:
                    QuizTimer.objects.update_or_create(quizId=GenerateAssign_instance_temp,
                                             userId=j.userId,
                                             classroom=GenerateAssign_instance_temp.classroom,
                                             timer=x,
                                             )

            return HttpResponseRedirect('/ClassRoom/'+request.session["classroom"])
        except Exception as E:
            from django.contrib import messages
            messages.error(request, E)
            return render(request,"CreateAssignment.html", {"categories": Category.objects.all()})
    else:
        return render(request, 'CreateAssignment.html', {"categories": Category.objects.all()})

@login_required
def DeleteAssign(request, classroom, quiz_id):
    if not request.user.is_authenticated or not(request.user.is_admin or request.user.groups.filter(name__in=[classroom + "_Teacher",classroom + "_TA"])):
        return HttpResponseRedirect('/LogOut')
    quiz = Quiz.objects.get(pk=quiz_id)
    quizStatus = QuizStatus.objects.filter(quizId=quiz, classroom=quiz.classroom, )
    for j in quizStatus:
        if j.status:
            quizDoneCount = QuizTracker.objects.get(
                            userId=j.userId,
                            classroom=quiz.classroom, )
            #print(quizDoneCount)
            if quizDoneCount.quizDoneCount != 0:
                try:
                    quizDoneCount.quizDoneCount -= 1
                    quizDoneCount.save(update_fields=["quizDoneCount"])
                except quizDoneCount.DoesNotExist:
                    pass
        elif j.status is not True:
            pass
    quiz.delete()
    return HttpResponseRedirect('/ClassRoom/'+request.session["classroom"])

def regen(require_regen,mode=None):
    if mode == None:
        test_temp = Quiz.objects.create(
            quizTitle=require_regen["quizTitle"],
            quizDetail=require_regen["quizDetail"],
            deadline=require_regen["deadline"],
            available=require_regen["available"],
            category=Category.objects.get(name=require_regen["category"]),
            hint=require_regen["hint"],
            text_testcode_content=require_regen["text_testcode_content"],
            text_testcase_content=require_regen["text_testcase_content"],
            text_template_content=require_regen["text_template_content"],
            max_score=require_regen["MaxScore"],
            mode=require_regen["mode"],
            classroom=require_regen["classroom"]
        )
        GenerateAssign_instance_temp = test_temp
        get_tracker = QuizTracker.objects.filter(
            classroom=GenerateAssign_instance_temp.classroom)  # reference at QuizTracker
        for k in get_tracker:
            QuizStatus.objects.update_or_create(quizId=GenerateAssign_instance_temp,
                                                userId=k.userId,
                                                classroom=GenerateAssign_instance_temp.classroom,
                                                status=False,
                                                )
        #print("k1 has passed")
        try:
            for k in get_tracker:
                tracker = QuizTracker.objects.get(userId=k.userId,
                                                  classroom=GenerateAssign_instance_temp.classroom,
                                                  )
                if tracker.quizDoneCount > 0:
                    tracker.quizDoneCount -= 1
                tracker.save(update_fields=["quizDoneCount"])

            if require_regen["Timer"] != '':
                #print("timeryes")
                Timer_temp = ''
                for i in require_regen["Timer"]:
                    if i == ' ':
                        pass
                    else:
                        Timer_temp += i
                require_regen["Timer"] = Timer_temp
                o = require_regen["Timer"].split(':')
                x = int(o[0]) * 3600 + int(o[1]) * 60 + int(o[2])
                for j in get_tracker:
                    QuizTimer.objects.update_or_create(quizId=GenerateAssign_instance_temp,
                                                       userId=j.userId,
                                                       classroom=GenerateAssign_instance_temp.classroom,
                                                       timer=x,
                                                       )
            #print("k2 has passed")
        except Exception as e:
            #print("k2 has failed")
            #print(e)
            pass
        return test_temp
    elif mode == "exam_quiz":
        test_temp = Exam_Quiz.objects.create(
            title=require_regen["title"],
            detail=require_regen["detail"],
            category=Category.objects.get(name=require_regen["category"]),
            text_testcode_content=require_regen["text_testcode_content"],
            text_testcase_content=require_regen["text_testcase_content"],
            text_template_content=require_regen["text_template_content"],
            mode=require_regen["mode"],
            classroom=require_regen["classroom"]
        )
        return test_temp

@login_required
def EditAssign(request, classroom, quiz_id):
    if not request.user.is_authenticated or not(request.user.is_admin or request.user.groups.filter(name__in=[classroom + "_Teacher",classroom + "_TA"])):
        return HttpResponseRedirect('/LogOut')
    elif request.method == "POST":
        try:
            if request.POST['asname'] == '':
                raise ValueError("Assignment must have a name!")
            elif request.POST['test_code'] == '' or request.POST['upload_testcase'] == '':
                raise ValueError("Test code and Test case must not blank!")
            elif request.POST['dateAvailable'] == '':
                raise ValueError("Please specific available date.")
            elif request.POST['dateInput'] == '':
                raise ValueError("Please specific deadline.")
            code_template = request.POST.get('upload_template', '')

#################################################### Check Testcase ####################################################
            test_code = request.POST.get('test_code', '')
            test_case = request.POST.get('upload_testcase', '')
            class case:num = 0
            def assert_equal(actual, expected, points=0, level=0):
                case.num += 1
                eval(compile(my_globals.string(case.num, actual, expected, points, level), 'defstr', 'exec'))
            libs = None
            for case_line in test_case.splitlines():
                if case_line.startswith('#lib') and len(case_line[5:]) != 0:
                    libs = case_line[5:].split(',')
            restricted_globals = dict(__builtins__=my_globals.mgb(globals(), libs))
            eval(compile(test_code + '\n' + test_case, 'gradingstr', 'exec'), restricted_globals, locals())
########################################################################################################################

            quiz = Quiz.objects.get(pk=quiz_id)
            OSS = OverwriteStorage()
            var = request.user.userId
            Assignment = request.POST.get('asname', '')
            Assignment_Detail = request.POST.get('asdetail', '')
            Deadline = request.POST.get('dateInput', '')
            Available = request.POST.get('dateAvailable', '')
            Hint = request.POST.get('hint', '')
            Cate = request.POST.get('quiz_category', '')
            Timer = request.POST.get('timer', '')
            MaxScore = float(request.POST.get('quiz_max_score', ''))
            asd = request.FILES.get('upload_testcase', False)
            asdf = request.FILES.get('upload_template', False)
            mode = request.POST.get('mode', '')
            redo = request.POST.get('redo', '')
            ### Define Section ###
            #if (Assignment != quiz.quizTitle or dab != quiz.text_testcase_content:
            #quiz_old = {
            #"title":quiz.quizTitle,
            #"testcase":quiz.text_testcase_content,
            #}
            if (redo == "Yes"): #or quiz_old["title"] != Assignment or quiz_old["testcase"] != dab):
                quiz.delete()
                regen({"quizTitle":Assignment,
                                 "quizDetail":Assignment_Detail,
                                 "deadline":Deadline,
                                 "available":Available,
                                 "category":Cate,
                                 "hint":Hint,
                                 "text_testcode_content":test_code,
                                 "text_testcase_content":test_case,
                                 "text_template_content":code_template,
                                 "mode":mode,
                                 "classroom":quiz.classroom,
                                 "Timer":Timer,
                                 "MaxScore":MaxScore,
                                 })
                #print("ppl=sh!t")

            else:
                get_tracker = QuizTracker.objects.filter(classroom=quiz.classroom)  # reference at QuizTracker
                quiz.quizTitle = Assignment
                quiz.quizDetail = Assignment_Detail
                quiz.deadline = Deadline
                quiz.available = Available
                quiz.category = Category.objects.get(name=Cate)
                quiz.hint = Hint
                quiz.text_testcode_content = test_code
                quiz.text_testcase_content = test_case
                quiz.text_template_content = code_template
                quiz.mode = mode
                quiz.save()
                if Timer != '':
                    # print("timeryes")
                    Timer_temp = ''
                    for i in Timer:
                        if i == ' ':
                            pass
                        else:
                            Timer_temp += i
                    Timer = Timer_temp
                    o = Timer.split(':')
                    x = int(o[0]) * 3600 + int(o[1]) * 60 + int(o[2])
                    for j in get_tracker:
                        try:
                            timer = QuizTimer.objects.get(quizId=quiz,
                                                          userId=j.userId,
                                                          classroom=quiz.classroom,
                                                          )
                            if timer.start:
                                timer.timer = x
                                timer.timer_stop = timezone.now() + timezone.timedelta(seconds=timer.timer)
                            else:
                                timer.timer = x
                                timer.timer_stop = None
                            timer.save(update_fields=["timer", "timer_stop"])
                        except ObjectDoesNotExist:
                            timer = QuizTimer.objects.create(quizId=quiz,
                                                          userId=j.userId,
                                                          classroom=quiz.classroom,
                                                          )
                            if timer.start:
                                timer.timer = x
                                timer.timer_stop = timezone.now() + timezone.timedelta(seconds=timer.timer)
                            else:
                                timer.timer = x
                                timer.timer_stop = None
                            timer.save(update_fields=["timer", "timer_stop"])
                        except Exception as e:
                            #print(e)
                            continue
            return HttpResponseRedirect('/ClassRoom/'+request.session["classroom"])
        except Exception as E:
            from django.contrib import messages
            messages.error(request, E)
            return HttpResponseRedirect('/ClassRoom/' + request.session["classroom"] + '/Assignment/EditAssign/' + quiz_id, {"categories": Category.objects.all()})


    else:
        quiz = Quiz.objects.get(pk=quiz_id)
        try:
            quizTimer = QuizTimer.objects.get(quizId=quiz)
        except:
            quizTimer = ''
        context = {'quizedit': quiz,
                   'quiztedit': quizTimer,
                   'quizdedit': quiz.deadline,
                   'quizaedit': quiz.available,
                   'categories': Category.objects.all(),
                  }
        return render(request, 'EditAssignment.html', context)

#################################################### Examination Section ####################################################
@login_required
def GenerateExam(request,classroom):
    if not request.user.is_authenticated or not(request.user.is_admin or request.user.groups.filter(name__in=[classroom + "_Teacher",classroom + "_TA"])):
        return HttpResponseRedirect('/LogOut')
    elif request.method == "POST": #and request.FILES['upload_testcase']:
        try:
            if request.POST['exam_name'] == '':
                raise ValueError("Exam must have a name!")
            elif request.POST['dateAvailable'] == '':
                raise ValueError("Please specific available date.")
            elif request.POST['dateInput'] == '':
                raise ValueError("Please specific deadline.")
            import random
            Exam = request.POST.get('exam_name', '')
            Detail = request.POST.get('exam_detail', '')
            Deadline = request.POST.get('dateInput', '')
            Available = request.POST.get('dateAvailable', '')
            MaxScore = float(request.POST.get('exam_max_score', ''))
            GenerateExam_instance = Exam_Data.objects.create(name=Exam, detail=Detail, deadline=Deadline, available=Available, max_score=MaxScore, classroom=ClassRoom.objects.get(className=classroom))
            GenerateExam_instance.save()

#################################################### Random examination for each user from pool. ####################################################
            import time
            import asyncio
            Cate = Category.objects.all()
            Target = ClassRoom.objects.get(className=classroom).user.all()
            # planned for asynchronous.
            #async def generate_tracker():
                #t0 = time.time()
                #for user in ClassRoom.objects.get(className=classroom).user.all():
                #    Exam_Tracker.objects.create(exam=GenerateExam_instance, user=user)
                #    #await asyncio.sleep(0.25)
                #t1 = time.time()
                #print(1000 * (t1 - t0))
            for user in ClassRoom.objects.get(className=classroom).user.all():
                Exam_Tracker.objects.create(exam=GenerateExam_instance, user=user)
            async def random_exam_quiz():
                #t0 = time.time()
                for user in Target:
                    picked_list, picked_this = [picked for picked in Exam_Tracker.objects.filter(user=user) if
                                                isinstance(picked.picked, list) for picked in picked.picked], []
                    # print(picked_list)
                    for category, amount in zip(Cate, request.POST.getlist("pick_amount")):
                        exam_quiz = list(
                            Exam_Quiz.objects.filter(classroom__className=classroom, category=category).exclude(
                                title__in=picked_list))
                        # print(exam_quiz)
                        amount = int(amount) if amount != '' else 0
                        for num in range(amount):
                            picked_num = None if len(exam_quiz) == 0 else random.randint(0, len(exam_quiz) - 1)
                            if picked_num == None: break
                            picked_this.append(exam_quiz[picked_num].title)
                            exam_quiz.pop(picked_num)
                    # print(picked_this)
                    Exam_tracker = Exam_Tracker.objects.get(exam=GenerateExam_instance, user=user)
                    Exam_tracker.picked = picked_this
                    Exam_tracker.save()
                    await asyncio.sleep(0.1)
                #t1 = time.time()
                #print(1000 * (t1 - t0))
            async def run_random():
                t0 = time.time()
                await asyncio.wait([random_exam_quiz()])
                t1 = time.time()
                print("Took %.3f" % (1000 * (t1 - t0)))
            loop = asyncio.get_event_loop()
            loop.run_until_complete(run_random())
#####################################################################################################################################################

            return HttpResponseRedirect('/ClassRoom/'+request.session["classroom"])
        except Exception as E:
            print(E)
            from django.contrib import messages
            messages.error(request, E)
            return render(request,"Exam/CreateExam.html", {"categories": Category.objects.all()})
    else:
        return render(request, 'Exam/CreateExam.html', {"categories": Category.objects.all()})

@login_required
def EditExam(request, classroom, exam_data_id):
    if not request.user.is_authenticated or not(request.user.is_admin or request.user.groups.filter(name__in=[classroom + "_Teacher",classroom + "_TA"])):
        return HttpResponseRedirect('/LogOut')
    elif request.method == "POST":
        try:
            if request.POST['exam_name'] == '':
                raise ValueError("Exam must have a name!")
            elif request.POST['dateAvailable'] == '':
                raise ValueError("Please specific available date.")
            elif request.POST['dateInput'] == '':
                raise ValueError("Please specific deadline.")
            import random
            Exam = request.POST.get('exam_name', '')
            Detail = request.POST.get('exam_detail', '')
            Deadline = request.POST.get('dateInput', '')
            Available = request.POST.get('dateAvailable', '')
            MaxScore = float(request.POST.get('exam_max_score', ''))

            if request.POST['redo'] == "Yes":
                Exam_Data.objects.get(pk=exam_data_id).delete()
                GenerateExam_instance = Exam_Data.objects.create(name=Exam, detail=Detail, deadline=Deadline,available=Available,classroom=ClassRoom.objects.get(className=classroom),max_score=MaxScore)
                GenerateExam_instance.save()

                #################################################### Random examination for each user from pool. ####################################################
                import time
                import asyncio
                Cate = Category.objects.all()
                Target = ClassRoom.objects.get(className=classroom).user.all()
                for user in ClassRoom.objects.get(className=classroom).user.all():
                    Exam_Tracker.objects.create(exam=GenerateExam_instance, user=user)
                # planned for asynchronous.
                async def random_exam_quiz():
                    for user in Target:
                        picked_list, picked_this = [picked for picked in Exam_Tracker.objects.filter(user=user) if isinstance(picked.picked, list) for picked in picked.picked], []
                        # print(picked_list)
                        for category, amount in zip(Cate, request.POST.getlist("pick_amount")):
                            exam_quiz = list(
                                Exam_Quiz.objects.filter(classroom__className=classroom, category=category).exclude(title__in=picked_list))
                            # print(exam_quiz)
                            amount = int(amount) if amount != '' else 0
                            for num in range(amount):
                                picked_num = None if len(exam_quiz) == 0 else random.randint(0, len(exam_quiz) - 1)
                                if picked_num == None: break
                                picked_this.append(exam_quiz[picked_num].title)
                                exam_quiz.pop(picked_num)
                        # print(picked_this)
                        Exam_tracker = Exam_Tracker.objects.get(exam=GenerateExam_instance, user=user)
                        Exam_tracker.picked = picked_this
                        Exam_tracker.save()
                        await asyncio.sleep(0.1)
                async def run_random():
                    t0 = time.time()
                    await asyncio.wait([random_exam_quiz()])
                    t1 = time.time()
                    print("Took %.3f" % (1000 * (t1 - t0)))
                loop = asyncio.get_event_loop()
                loop.run_until_complete(run_random())
                #####################################################################################################################################################
            else:
                exam_data = Exam_Data.objects.get(pk=exam_data_id)
                exam_data.name = Exam
                exam_data.detail = Detail
                exam_data.deadline = Deadline
                exam_data.available = Available
                exam_data.classroom = ClassRoom.objects.get(className=classroom)
                exam_data.max_score = MaxScore
                exam_data.save()
            return HttpResponseRedirect('/ClassRoom/' + request.session["classroom"])
        except Exception as E:
            from django.contrib import messages
            messages.error(request, E)
            return HttpResponseRedirect('/ClassRoom/' + request.session["classroom"] + '/Assignment/EditExam/' + exam_data_id, {"exam": exam, "categories": Category.objects.all()})
    else:
        exam = Exam_Data.objects.get(pk=exam_data_id, classroom__className=classroom)
        context = {'exam': exam,
                   'categories': Category.objects.all(),
                   }
        return render(request, 'Exam/EditExam.html', context)

@login_required
def DeleteExam(request, classroom, exam_data_id):
    if not request.user.is_authenticated or not(request.user.is_admin or request.user.groups.filter(name__in=[classroom + "_Teacher",classroom + "_TA"])):
        return HttpResponseRedirect('/LogOut')
    Exam_Data.objects.get(pk=exam_data_id).delete()
    return HttpResponseRedirect('/ClassRoom/'+request.session["classroom"])

@login_required
def GenerateExamQuiz(request,classroom):
    if not request.user.is_authenticated or not(request.user.is_admin or request.user.groups.filter(name__in=[classroom + "_Teacher",classroom + "_TA"])):
        return HttpResponseRedirect('/LogOut')
    elif request.method == "POST": #and request.FILES['upload_testcase']:
        try:
            if request.POST['exam_name'] == '':
                raise ValueError("Exam must have a name!")
            elif request.POST['test_code'] == '' or request.POST['upload_testcase'] == '':
                raise ValueError("Test code and Test case must not blank!")
            code_template = request.POST.get('upload_template', '')

#################################################### Check Testcase ####################################################
            test_code = request.POST.get('test_code', '')
            test_case = request.POST.get('upload_testcase', '')
            class case: num = 0
            def assert_equal(actual, expected, points=0, level=0):
                case.num += 1
                eval(compile(my_globals.string(case.num, actual, expected, points, level), 'defstr', 'exec'))
            # Exec
            libs=None
            for case_line in test_case.splitlines():
                if case_line.startswith('#lib') and len(case_line[5:]) != 0:
                    libs = case_line[5:].split(',')
            restricted_globals = dict(__builtins__=my_globals.mgb(globals(), libs))
            eval(compile(test_code+'\n'+test_case, 'gradingstr', 'exec'), restricted_globals, locals())
########################################################################################################################

            Examination = request.POST.get('exam_name', '')
            Examination_Detail = request.POST.get('exam_detail', '')
            Cate = Category.objects.get(name=request.POST.get('quiz_category', ''))
            mode = request.POST.get('mode','')
            Exam_Quiz.objects.create(title=Examination, detail=Examination_Detail, category=Cate, text_template_content=code_template, text_testcode_content=test_code, text_testcase_content=test_case, mode=mode, classroom=ClassRoom.objects.get(className=classroom))
            return HttpResponseRedirect('/ClassRoom/'+request.session["classroom"])
        except Exception as E:
            print(E)
            from django.contrib import messages
            messages.error(request, E)
            return render(request,"CreateAssignment.html", {"categories": Category.objects.all()})
    else:
        return render(request, 'Exam/CreateExamQuiz.html', {"categories": Category.objects.all()})

@login_required
def EditExamQuiz(request, classroom, exam_quiz_id):
    if not request.user.is_authenticated or not(request.user.is_admin or request.user.groups.filter(name__in=[classroom + "_Teacher",classroom + "_TA"])):
        return HttpResponseRedirect('/LogOut')
    elif request.method == "POST":
        try:
            if request.POST['exam_name'] == '':
                raise ValueError("Exam must have a name!")
            elif request.POST['test_code'] == '' or request.POST['upload_testcase'] == '':
                raise ValueError("Test code and Test case must not blank!")
            code_template = request.POST.get('upload_template', '')

#################################################### Check Testcase ####################################################
            test_code = request.POST.get('test_code', '')
            test_case = request.POST.get('upload_testcase', '')
            class case:num = 0
            def assert_equal(actual, expected, points=0, level=0):
                case.num += 1
                eval(compile(my_globals.string(case.num, actual, expected, points, level), 'defstr', 'exec'))
            libs = None
            for case_line in test_case.splitlines():
                if case_line.startswith('#lib') and len(case_line[5:]) != 0:
                    libs = case_line[5:].split(',')
            restricted_globals = dict(__builtins__=my_globals.mgb(globals(), libs))
            eval(compile(test_code + '\n' + test_case, 'gradingstr', 'exec'), restricted_globals, locals())
########################################################################################################################

            exam_quiz = Exam_Quiz.objects.get(pk=exam_quiz_id)
            exam_name = request.POST.get('exam_name', '')
            exam_detail = request.POST.get('exam_detail', '')
            Cate = request.POST.get('quiz_category', '')
            mode = request.POST.get('mode', '')
            redo = request.POST.get('redo', '')
            ### Define Section ###
            if (redo == "Yes"):
                exam_quiz.delete()
                regen({"title":exam_name,
                                 "detail":exam_detail,
                                 "category":Cate,
                                 "text_testcode_content": test_code,
                                 "text_testcase_content":test_case,
                                 "text_template_content":code_template,
                                 "mode":mode,
                                 "classroom":exam_quiz.classroom,
                                 },"exam_quiz")

            else:
                exam_quiz.title = exam_name
                exam_quiz.detail = exam_detail
                exam_quiz.category = Category.objects.get(name=Cate)
                exam_quiz.text_testcode_content = test_code
                exam_quiz.text_testcase_content = test_case
                exam_quiz.text_template_content = code_template
                exam_quiz.mode = mode
                exam_quiz.save()
            return HttpResponseRedirect('/ClassRoom/'+request.session["classroom"])
        except Exception as E:
            from django.contrib import messages
            messages.error(request, E)
            return HttpResponseRedirect('/ClassRoom/' + request.session["classroom"] + '/Assignment/edit_exam_quiz/' + exam_quiz_id, {"categories": Category.objects.all()})


    else:
        exam_quiz = Exam_Quiz.objects.get(pk=exam_quiz_id)
        context = {'exam_quiz': exam_quiz,
                   'categories': Category.objects.all(),
                  }
        return render(request, 'Exam/EditExamQuiz.html', context)

@login_required
def DeleteExamQuiz(request, classroom, exam_quiz_id):
    if not request.user.is_authenticated or not(request.user.is_admin or request.user.groups.filter(name__in=[classroom + "_Teacher",classroom + "_TA"])):
        return HttpResponseRedirect('/LogOut')
    exam_quiz = Exam_Quiz.objects.get(pk=exam_quiz_id)
    try:
        for tracker in Exam_Tracker.objects.filter(picked__contains='{'+exam_quiz.title+'}'):
            try:
                tracker.picked.remove(exam_quiz.title)
            except Exception as E:
                print(E)
                tracker.picked = []
            tracker.save()
    except Exception as E:
        print(E)
    exam_quiz.delete()
    return HttpResponseRedirect('/ClassRoom/'+request.session["classroom"])

#################################################### AutoGrader Section ####################################################
@login_required
@timeout_decorator.timeout(6, use_signals=False)
def uploadgrading(request, classroom, quiz_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/LogOut')

    elif (ClassRoom.objects.get(className=classroom).user.filter(userId=request.user.userId).exists() != True) and not(request.user.is_admin or request.user.groups.filter(name__in=[classroom + "_Teacher",classroom + "_TA"])):
        return HttpResponseRedirect('/ClassRoom/' + request.session["classroom"])

    #elif (ClassRoom.objects.get(className=classroom).user.filter(userId=request.user.userId).exists() != True or Rank.objects.get(userId=request.user, classroom__className=classroom).rank < Quiz.objects.get(pk=quiz_id).rank)and not(request.user.is_admin or request.user.groups.filter(name__in=[classroom + "_Teacher",classroom + "_TA"])):
    #    return HttpResponseRedirect('/ClassRoom/' + request.session["classroom"])

    global deadline, timer_stop
    timezone.make_aware(datetime.datetime.now(), timezone.get_default_timezone())
    t = timezone.localtime(timezone.now())  # offset-awared datetime
    t.astimezone(timezone.utc).replace(tzinfo=None)
    quiz = Quiz.objects.get(pk=quiz_id)
    try:
        Timer = QuizTimer.objects.get(quizId=quiz,
                                        userId=User.objects.get(userId=request.user.userId),
                                        classroom=quiz.classroom,
                                        ).timer_stop
    except ObjectDoesNotExist:
        Timer = None
    #set utc+7 check setting file 'Asia/Bangkok'
    if Timer is not None:
        #print("Timer is not None.")
        deadline, timer_stop = timezone.localtime(quiz.deadline),timezone.localtime(Timer)
        deadline.astimezone(timezone.utc).replace(tzinfo=None)
        timer_stop.astimezone(timezone.utc).replace(tzinfo=None)
        if (t >= deadline or t >= timer_stop or t <= quiz.available) and not (request.user.is_admin or request.user.groups.filter(name__in=[classroom + "_Teacher",classroom + "_TA"])):
            return HttpResponseRedirect('/ClassRoom/'+request.session["classroom"])
    elif Timer is None:
        #print("Timer is None.")
        deadline =  timezone.localtime(quiz.deadline)
        deadline.astimezone(timezone.utc).replace(tzinfo=None)
        #print(t)
        #print(deadline)
        if ((t >= deadline or t <= quiz.available) and not(request.user.is_admin or request.user.groups.filter(name__in=[classroom + "_Teacher",classroom + "_TA"]))):
            return HttpResponseRedirect('/ClassRoom/'+request.session["classroom"])

#################################################### Upload Section ####################################################
    try:
        code_temp = quiz.text_template_content
        libs = None
        my_globals.limit_grader()
        if request.method == "POST" and 'time_left' in request.POST:
            #print("this?")
            time_left = request.POST.get("time_left",'')
            #print(time_left)
            try:
                timer = QuizTimer.objects.get(quizId=quiz,userId=User.objects.get(userId=request.user.userId),classroom=quiz.classroom, )
                timer.timer = time_left
                timer.save(update_fields=["timer"])
            except ObjectDoesNotExist:
                pass
            return HttpResponseRedirect('/ClassRoom/' + request.session["classroom"])

        elif request.method == 'POST' and 'upload_submit' in request.POST:
            if request.FILES['upload']:
                #print("in_upload_submit")
                uploaded_to_file = request.FILES['upload']
                code = uploaded_to_file.read().decode("utf-8")
                temp_code = code
                if uploaded_to_file._size > 1048576 or not uploaded_to_file.name.endswith(".py"):
                    return render(request, 'Upload.html', {'quizTitle': quiz.quizTitle,
                                                           'quizDetail': quiz.quizDetail,
                                                           'Deadline': quiz.deadline,
                                                           'Hint': quiz.hint,
                                                           'Timer': False,
                                                           'message': True,
                                                           'code': code_temp,
                                                           'Deadtimestamp': deadline.timestamp() * 1000,
                                                           })
                #print(FSS.path(in_sys_file))
                #Upload.objects.get_or_create(title=in_sys_file, Uploadfile=in_sys_file ,user=request.user, quiz=quiz, classroom=quiz.classroom)
                ####################################
                # open file .txt. Address  file ???????? Now! change follow your PC
                #with open(in_sys_file_location + in_sys_file, 'r+') as f:
                #    code = code_origin = f.read()
                    #restricted_globals = dict(__builtins__=my_globals.mgb())
                    #sandboxe = eval(compile(code, filename='./media/' + fileName, mode='exec'), restricted_globals, {})
                    #del sandboxe
                    #f.seek(0, 0)
                    #if "# lib" in quiz.text_testcase_content.splitlines()[0]:
                        #f.write("import ".rstrip('\r\n') + quiz.text_testcase_content.splitlines()[0][6:].rstrip('\r\n') + '\n' + code)
                        # libs = quiz.text_testcase_content.splitlines()[0][6:].split(" ")
                        # print(libs)
                    # else:
                    # libs = []
                #if in_sys_file[:-3] in sys.modules:
                    #del sys.modules[in_sys_file[:-3]]
                    #importlib.invalidate_caches()
                    #prob = importlib.import_module(in_sys_file[:-3])
                    #importlib.reload(prob)
                #else:
                    #prob = importlib.import_module(in_sys_file[:-3])
                    #importlib.reload(prob)
                #print(prob)
                #setattr(module, 'prob', prob)
                #with open(in_sys_file_location + in_sys_file, 'a') as f:
                #    case = quiz.text_testcase_content
                #    f.write('\n')
                #    for case_line in case.splitlines():
                #        f.write(case_line + "\n")
                #with open(in_sys_file_location + in_sys_file, 'r') as f:
                #    code = f.read()
                code += '\n'
                for case_line in quiz.text_testcase_content.splitlines():
                    if case_line.startswith('#lib') and len(case_line[5:]) != 0:
                        libs = case_line[5:].split(',')
                    code += case_line + "\n"
#################################################### Unittest Process. ####################################################
                class MyTestCase(unittest.TestCase):
                    num = 0
                    result = {
                        'max_score': 0,
                        'score': 0,
                        'case': {},
                    }
                def assert_equal(actual, expected, points=0, level=0):
                    #rand_string = get_random_string(length=7)
                    MyTestCase.num += 1
                    #print(locals())
                    #print(MyTestCase.num)
                    eval(compile(my_globals.string(MyTestCase.num, actual, expected, points, level), 'defstr', 'exec'))
                    #print(str(actual)+str(expected)+str(points)+str(hidden))
                    #print(string)
                    #print(globals())
                    #print(globals()[name]['params'])
                    #print(str_to_class('test_{0}'.format(rand_string)))
                    setattr(MyTestCase, "test_{0}".format(MyTestCase.num),locals()['test_{0}'.format(MyTestCase.num)])
                    #setattr(MyTestCase, "test_{0}".format(rand_string), str_to_class('test_{0}'.format(rand_string)))
                    #method_list = [func for func in dir(MyTestCase) if callable(getattr(MyTestCase, func)) and not func.startswith("__")]
                    #print(method_list)

                # Exec
                with stdoutIO() as gradingstr:
                    restricted_globals = dict(__builtins__=my_globals.mgb(globals(),libs))
                    eval(compile(code,'gradingstr', 'exec'),restricted_globals,locals())
                gradingstr_out = gradingstr.getvalue()#.split('\n')
                # return None
                test_suite = unittest.TestLoader().loadTestsFromTestCase(MyTestCase)
                test_result = TextTestRunner().run(test_suite)
                # fail = len(test_result.failures)
#################################################### Result Section ####################################################
                result = MyTestCase.result
                if quiz.mode == "Pass or Fail" and test_result.wasSuccessful():
                    result['status'] = "PASS"
                elif quiz.mode == "Pass or Fail" and test_result.wasSuccessful() == False:
                    result['status'] = "FAIL"
                    result['score'] = 0
                elif quiz.mode == "Scoring" and my_globals.scr(result['case']) is True:
                    result['status'] = "PASS"
                else:
                    result['status'] = "FAIL"
                # print(case)

#################################################### Query Section ####################################################
                try:
                    if QuizStatus.objects.get(quizId=quiz, userId=User.objects.get(userId=request.user.userId),classroom=quiz.classroom).status == False:
                        QuizTracker.objects.update_or_create(userId=User.objects.get(userId=request.user.userId),classroom=quiz.classroom,
                        )
                        quizDoneCount = QuizTracker.objects.get(userId=User.objects.get(userId=request.user.userId),classroom=quiz.classroom, )
                        quizDoneCount.quizDoneCount += 1
                        quizDoneCount.save()
                        quizStatus = QuizStatus.objects.get(quizId=quiz,userId=User.objects.get(userId=request.user.userId),classroom=quiz.classroom,)
                        quizStatus.status = True
                        quizStatus.save()
                except:
                    QuizStatus.objects.create(quizId=quiz, userId=User.objects.get(userId=request.user.userId), classroom=quiz.classroom, status=True)
                    QuizTracker.objects.update_or_create(userId=User.objects.get(userId=request.user.userId),classroom=quiz.classroom,)
                    quizDoneCount = QuizTracker.objects.get(userId=User.objects.get(userId=request.user.userId),classroom=quiz.classroom, )
                    quizDoneCount.quizDoneCount += 1
                    quizDoneCount.save()
                # print(str(test_case_count) + ' ' + str(Out_count))

                fileName = str(request.user.userId) + '_uploaded_' + str(quiz.quizTitle) + '_' + str(quiz.classroom.className) + request.FILES['upload'].name[-3:]
                quiz_name = Quiz.objects.get(id=quiz_id)
                in_sys_file_location = os.getcwd() + "/media/"  # +fuck_sake.classroom.className+'/'+request.user.userId+'/'+fuck_sake.quizTitle+'/'
                temp_test = quiz_name.classroom.className + '/' + request.user.userId + '/' + quiz_name.quizTitle + '/'
                sys.path.append(in_sys_file_location)
                # FSS = FileSystemStorage()#(location=in_sys_file_location,#base_url=os.path.join(temp_test))
                in_sys_file = FileSystemStorage().save(fileName, uploaded_to_file)
                in_sys_file_url = FileSystemStorage().url(in_sys_file)
                with open(in_sys_file_location + in_sys_file, 'w') as f:
                    f.write(temp_code)
                    Upload.objects.get_or_create(title=in_sys_file, Uploadfile=in_sys_file, user=request.user, quiz=quiz, classroom=quiz.classroom)
                with open(in_sys_file_location + in_sys_file, 'a') as f:
                    f.write('\n\n')
                    for c,i in enumerate(result['case'].values()):
                        print(i)
                        f.write("CASE {0}: ".format(c+1) + i + '\n')
                    f.write("RESULT: %s" % result['status'])
                with open(in_sys_file_location + in_sys_file, 'r') as f:
                    try:
                        quiz_score = QuizScore.objects.get(quizId=quiz,userId=User.objects.get(userId=request.user.userId),classroom=quiz.classroom)
                        if quiz.mode == "Scoring":
                            if result['score'] >= quiz_score.total_score:
                                # print(str(quiz_score.total_score) + ":" + str(quiz_score.passOrFail))
                                # print(str(score_total)+":"+str(result_model))
                                # print(fileName)
                                # return None
                                quiz_score.total_score = result['score']
                                quiz_score.passOrFail = 0
                                quiz_score.max_score = result['max_score']
                                quiz_score.code = Upload.objects.get(title=in_sys_file)  # f.read()
                                quiz_score.save()
                        else:
                            if result['score'] >= quiz_score.passOrFail:
                                quiz_score.total_score = 0
                                quiz_score.passOrFail = result['score']
                                quiz_score.max_score = result['max_score']
                                quiz_score.code = Upload.objects.get(title=in_sys_file)  # f.read()
                                quiz_score.save()
                    except ObjectDoesNotExist:
                        if quiz.mode == "Scoring":
                            x = (1,0)
                        else:
                            x = (0,1)
                        quiz_score = QuizScore.objects.create(quizId=quiz,
                                                              userId=User.objects.get(
                                                              userId=request.user.userId),
                                                              classroom=quiz.classroom,
                                                              total_score=result['score']*x[0],
                                                              passOrFail=result['score']*x[1],
                                                              max_score=result['max_score'],
                                                              code=Upload.objects.get(title=in_sys_file)  # f.read(),
                                                              )
                    upload_instance = Upload.objects.get(title=in_sys_file, Uploadfile=in_sys_file, user=request.user,
                                                         quiz=quiz, classroom=quiz.classroom)
                    if quiz.mode == "Scoring":
                        if quiz_score.total_score == None:
                            result['score'] = 0
                        upload_instance.score = result['score']
                    elif quiz.mode == "Pass or Fail":
                        if quiz_score.passOrFail == None:
                            result['score'] = 0
                        upload_instance.score = result['score']
                    upload_instance.save(update_fields=["score"])
                    # print(eval('dir()'))
            try:
                return render(request, 'Upload.html', {'quizTitle': quiz.quizTitle,
                                                       'quizDetail': quiz.quizDetail,
                                                       'Deadline': quiz.deadline,
                                                       'Hint': quiz.hint,
                                                       'display': result,
                                                       'Case_Count': test_result.testsRun,
                                                       'mode': quiz.mode,
                                                       'code': code_temp,
                                                       'prints': gradingstr_out,
                                                       'Timer': timer_stop.timestamp() * 1000,
                                                       'Deadtimestamp': deadline.timestamp() * 1000, })
            except Exception as e:
                # print(e)
                return render(request, 'Upload.html', {'quizTitle': quiz.quizTitle,
                                                       'quizDetail': quiz.quizDetail,
                                                       'Deadline': quiz.deadline,
                                                       'Hint': quiz.hint,
                                                       'display': result,
                                                       'Case_Count': test_result.testsRun,
                                                       'mode': quiz.mode,
                                                       'Timer': False,
                                                       'code': code_temp,
                                                       'prints': gradingstr_out,
                                                       'Deadtimestamp': deadline.timestamp() * 1000, })

#################################################### Editor Section ####################################################
        elif request.method == 'POST' and 'code-form-submit' in request.POST:
            code = request.POST['code-form-comment']
            code_temp = code
            #print("in-code-form")
            if code == '':
                return render(request, 'Upload.html', {'quizTitle': quiz.quizTitle,
                                                        'quizDetail': quiz.quizDetail,
                                                        'Deadline': quiz.deadline,
                                                        'Hint': quiz.hint,
                                                        'code': code,
                                                       'Timer':timer_stop.timestamp()*1000,
                                                   'Deadtimestamp':deadline.timestamp()*1000,
                                                       })
            else:
                rs = get_random_string(length=7)
                fileName = str(request.user.userId) + '_coded_' + str(quiz.quizTitle) + '_' + str(quiz.classroom.className) + '_' + rs +'.py'
                #Upload.objects.get_or_create(title=fileName, Uploadfile=fileName, user=request.user, quiz=quiz, classroom=quiz.classroom)
                #with open('./media/' + fileName, 'w') as f:
                #    for debug_line in code:
                #        #print(debug_line)
                #        f.write(debug_line)
                ####################################
                # open file .txt. Address  file ???????? Now! change follow your PC
                #with open('./media/' + fileName, 'r+') as f:
                #    code = f.read()
                    #restricted_globals = dict(__builtins__=my_globals.mgb(name, globals())) # pass libs as parameters
                    #eval(compile(code, filename='./media/' + fileName, mode='exec'), restricted_globals, {})
                    #f.seek(0, 0)
                    #if "# lib" in quiz.text_testcase_content.splitlines()[0]:
                        #f.write("import ".rstrip('\r\n') + quiz.text_testcase_content.splitlines()[0][6:].rstrip('\r\n') + '\n' + code)
                        # libs = quiz.text_testcase_content.splitlines()[0][6:].split(" ")
                        # print(libs)
                    #else:
                        #libs = []

                #if fileName[:-3] in sys.modules:
                    #del sys.modules[fileName[:-3]]
                    # importlib.invalidate_caches()
                    #prob = importlib.import_module(fileName[:-3])
                    # importlib.reload(prob)
                #else:
                    #prob = importlib.import_module(fileName[:-3])
                    # importlib.reload(prob)
                    # print(prob)
                #with open('./media/' + fileName, 'a') as f:
                #    case = quiz.text_testcase_content
                #    f.write('\n')
                #    for case_line in case.splitlines():
                #        f.write(case_line + "\n")
                #with open('./media/' + fileName, 'r') as f:
                #    code = f.read()
                code += '\n'
                for case_line in quiz.text_testcase_content.splitlines():
                    if case_line.startswith('#lib') and len(case_line[5:]) != 0:
                        libs = case_line[5:].split(',')
                    code += case_line + "\n"

#################################################### Unittest Process. ####################################################
                class MyTestCase(unittest.TestCase):
                    num = 0
                    result = {
                        'max_score': 0,
                        'score': 0,
                        'case': {},
                    }
                def assert_equal(actual, expected, points=0, level=0):
                    #rand_string = get_random_string(length=7)
                    MyTestCase.num += 1
                    #print(locals())
                    #print(MyTestCase.num)
                    eval(compile(my_globals.string(MyTestCase.num, actual, expected, points, level), 'defstr', 'exec'))
                    #print(str(actual)+str(expected)+str(points)+str(hidden))
                    #print(string)
                    #print(globals())
                    #print(globals()[name]['params'])
                    #print(str_to_class('test_{0}'.format(rand_string)))
                    setattr(MyTestCase, "test_{0}".format(MyTestCase.num),locals()['test_{0}'.format(MyTestCase.num)])
                    #setattr(MyTestCase, "test_{0}".format(rand_string), str_to_class('test_{0}'.format(rand_string)))
                    #method_list = [func for func in dir(MyTestCase) if callable(getattr(MyTestCase, func)) and not func.startswith("__")]
                    #print(method_list)

                # Exec
                with stdoutIO() as gradingstr:
                    restricted_globals = dict(__builtins__=my_globals.mgb(globals(),libs))
                    eval(compile(code,'gradingstr', 'exec'),restricted_globals,locals())
                    #eval(compile(quiz.text_testcase_content, 'gradingstr', 'exec'), globals(), locals())
                gradingstr_out = gradingstr.getvalue()#.split('\n')
                #print(gradingstr_out)
                #return None
                test_suite = unittest.TestLoader().loadTestsFromTestCase(MyTestCase)
                test_result = TextTestRunner().run(test_suite)
                #fail = len(test_result.failures)
#################################################### Result Section ####################################################
                result = MyTestCase.result
                #print(result)
                #print(my_globals.scr(result['case']))
                #return None
                if quiz.mode == "Pass or Fail" and test_result.wasSuccessful():
                    result['status'] = "PASS"
                elif quiz.mode == "Pass or Fail" and test_result.wasSuccessful() is False:
                    result['status'] = "FAIL"
                    result['score'] = 0
                elif quiz.mode == "Scoring" and my_globals.scr(result['case']) is True:
                    result['status'] = "PASS"
                else:
                    result['status'] = "FAIL"
                #print(case)

#################################################### Query Section ####################################################
                try:
                    if QuizStatus.objects.get(quizId=quiz, userId=User.objects.get(userId=request.user.userId),classroom=quiz.classroom).status == False:
                        QuizTracker.objects.update_or_create(userId=User.objects.get(userId=request.user.userId),classroom=quiz.classroom,)
                        quizDoneCount = QuizTracker.objects.get(userId=User.objects.get(userId=request.user.userId),classroom=quiz.classroom, )
                        quizDoneCount.quizDoneCount += 1
                        quizDoneCount.save()
                        quizStatus = QuizStatus.objects.get(quizId=quiz,userId=User.objects.get(userId=request.user.userId),classroom=quiz.classroom,)
                        quizStatus.status = True
                        quizStatus.save()
                except:
                    QuizStatus.objects.create(quizId=quiz, userId=User.objects.get(userId=request.user.userId), classroom=quiz.classroom, status=True)
                    QuizTracker.objects.update_or_create(userId=User.objects.get(userId=request.user.userId),classroom=quiz.classroom,)
                    quizDoneCount = QuizTracker.objects.get(userId=User.objects.get(userId=request.user.userId),classroom=quiz.classroom, )
                    quizDoneCount.quizDoneCount += 1
                    quizDoneCount.save()
                #print(str(test_case_count) + ' ' + str(Out_count))
                with open('./media/' + fileName, 'w') as f:
                    f.write(code_temp)
                    Upload.objects.get_or_create(title=fileName, Uploadfile=fileName, user=request.user, quiz=quiz, classroom=quiz.classroom)
                with open('./media/' + fileName, 'a') as f:
                    f.write('\n\n')
                    for c,i in enumerate(result['case'].values()):
                        #print(i)
                        f.write("CASE {0}: ".format(c+1) + i + '\n')
                    f.write("RESULT: %s" % result['status'])
                with open('./media/' + fileName, 'r') as f:
                    try:
                        quiz_score = QuizScore.objects.get(quizId=quiz,userId=User.objects.get(userId=request.user.userId),classroom=quiz.classroom)
                        if quiz.mode == "Scoring":
                            if result['score'] >= quiz_score.total_score:
                                #print(str(quiz_score.total_score) + ":" + str(quiz_score.passOrFail))
                                #print(str(score_total)+":"+str(result_model))
                                #print(fileName)
                                #return None
                                quiz_score.total_score = result['score']
                                quiz_score.passOrFail = 0
                                quiz_score.max_score = result['max_score']
                                quiz_score.code =  Upload.objects.get(title=fileName) #f.read()
                                quiz_score.save()
                        else:
                            if result['score'] >= quiz_score.passOrFail:
                                quiz_score.total_score = 0
                                quiz_score.passOrFail = result['score']
                                quiz_score.max_score = result['max_score']
                                quiz_score.code = Upload.objects.get(title=fileName)  # f.read()
                                quiz_score.save()
                    except ObjectDoesNotExist:
                        if quiz.mode == "Scoring":
                            x = (1,0)
                        else:
                            x = (0,1)
                        quiz_score = QuizScore.objects.create(quizId=quiz,
                                                              userId=User.objects.get(
                                                                  userId=request.user.userId),
                                                              classroom=quiz.classroom,
                                                              total_score=result['score']*x[0],
                                                              passOrFail=result['score']*x[1],
                                                              max_score=result['max_score'],
                                                              code=Upload.objects.get(title=fileName)  # f.read(),
                                                              )
                    upload_instance = Upload.objects.get(title=fileName, Uploadfile=fileName ,user=request.user, quiz=quiz, classroom=quiz.classroom)
                    if quiz.mode == "Scoring":
                        if quiz_score.total_score == None:
                            result['score'] = 0
                        upload_instance.score = result['score']
                    elif quiz.mode == "Pass or Fail":
                        if quiz_score.passOrFail == None:
                            result['score'] = 0
                        upload_instance.score = result['score']
                    upload_instance.save(update_fields=["score"])
                    #print(eval('dir()'))
            try:
                return render(request, 'Upload.html', {'quizTitle': quiz.quizTitle,
                                                       'quizDetail': quiz.quizDetail,
                                                       'Deadline': quiz.deadline,
                                                       'Hint': quiz.hint,
                                                       'display': result,
                                                       'Case_Count': test_result.testsRun,
                                                       'mode': quiz.mode,
                                                       'code': code_temp,
                                                       'prints': gradingstr_out,
                                                       'Timer':timer_stop.timestamp()*1000,
                                                       'Deadtimestamp':deadline.timestamp()*1000,})
            except Exception as e:
                #print(e)
                return render(request, 'Upload.html', {'quizTitle': quiz.quizTitle,
                                                       'quizDetail': quiz.quizDetail,
                                                       'Deadline': quiz.deadline,
                                                       'Hint': quiz.hint,
                                                       'display': result,
                                                       'Case_Count': test_result.testsRun,
                                                       'mode': quiz.mode,
                                                       'code': code_temp,
                                                       'prints': gradingstr_out,
                                                       'Timer': False,
                                                       'Deadtimestamp': deadline.timestamp() * 1000, })
        else:
            #print("not-in-code-form")
            try:
                Timer = QuizTimer.objects.get(quizId=quiz, userId=User.objects.get(userId=request.user.userId),
                                              classroom=quiz.classroom, )
                if Timer.timer:
                    if not Timer.start:
                        Timer.timer_stop = timezone.now() + timezone.timedelta(seconds=Timer.timer)
                    Timer.start = True
                    Timer.save(update_fields=["timer_stop","start"])
                    return render(request, 'Upload.html', {'quizTitle': quiz.quizTitle,
                                                           'quizDetail': quiz.quizDetail,
                                                           'Deadline': quiz.deadline,
                                                           'Hint': quiz.hint,
                                                           'Timer': Timer.timer_stop.timestamp() * 1000,
                                                           'code': code_temp,
                                                           'Deadtimestamp': deadline.timestamp() * 1000,
                                                           })

            except ObjectDoesNotExist:
                return render(request, 'Upload.html', {'quizTitle':quiz.quizTitle,
                                                   'quizDetail':quiz.quizDetail,
                                                   'Deadline':quiz.deadline,
                                                   'Hint':quiz.hint,
                                                    'Timer':False,
                                                    'code': code_temp,
                                                    'Deadtimestamp':deadline.timestamp()*1000,
                })
    except Exception as e:
        #print(e)
        return render(request, 'Upload.html',{'quizTitle':quiz.quizTitle,
                                                'quizDetail':quiz.quizDetail,
                                                'Deadline':quiz.deadline,
                                                'Hint':quiz.hint,
                                                'Timer':False,
                                                'exception':e,
                                                'code':code_temp,
                                                'Deadtimestamp':deadline.timestamp()*1000,
                                            })

@login_required
def exam_quiz(request, classroom, exam_data_id):
    request.session["classroom"] = classroom
    user_group = {"teacher": User.objects.filter(groups__name=classroom + "_Teacher"),
                  "ta": User.objects.filter(groups__name=classroom + "_TA"),
                  }
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/LogOut')

    elif request.user.is_admin or request.user.groups.filter(name__in=[classroom + "_Teacher", classroom + "_TA"]).exists():
        exam_set = Exam_Data.objects.filter(classroom__className=classroom)

    else:
        exam_set = Exam_Data.objects.filter(classroom__className=classroom,
                                            available__lte=timezone.localtime(timezone.now()),
                                            deadline__gte=timezone.localtime(timezone.now()))
    context = {
        'classname': classroom,
        'classroom_creator': ClassRoom.objects.get(className=classroom).creator.get_full_name,
        'user_obj': User.objects.all(),
        'user_group': user_group,
        'exam': exam_set
    }
    return render(request, 'Home.html', context)

@login_required
@timeout_decorator.timeout(6, use_signals=False)
def exam_grader(request, classroom, exam_data_id, exam_quiz_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/LogOut')

    elif (ClassRoom.objects.get(className=classroom).user.filter(userId=request.user.userId).exists() != True) and not (request.user.is_admin or request.user.groups.filter(name__in=[classroom + "_Teacher", classroom + "_TA"])):
        return HttpResponseRedirect('/ClassRoom/' + request.session["classroom"])
    #elif (ClassRoom.objects.get(className=classroom).user.filter(userId=request.user.userId).exists() != True or Rank.objects.get(userId=request.user,classroom__className=classroom).rank < Quiz.objects.get(pk=quiz_id).rank) and not (request.user.is_admin or request.user.groups.filter(name__in=[classroom + "_Teacher", classroom + "_TA"])):
    #    return HttpResponseRedirect('/ClassRoom/' + request.session["classroom"])

    global deadline
    timezone.make_aware(datetime.datetime.now(), timezone.get_default_timezone())
    t = timezone.localtime(timezone.now())  # offset-awared datetime
    t.astimezone(timezone.utc).replace(tzinfo=None)
    exam_data = Exam_Data.objects.get(pk=exam_data_id)
    exam_quiz = Exam_Quiz.objects.get(pk=exam_quiz_id)
    exam_tracker = Exam_Tracker.objects.get(exam=exam_data,user=request.user)
    #set utc+7 check setting file 'Asia/Bangkok'
    deadline = timezone.localtime(exam_data.deadline)
    deadline.astimezone(timezone.utc).replace(tzinfo=None)
    if ((t >= deadline or t <= exam_data.available or exam_quiz.title not in exam_tracker.picked) and not(request.user.is_admin or request.user.groups.filter(name__in=[classroom + "_Teacher",classroom + "_TA"]))):
        return HttpResponseRedirect('/ClassRoom/'+request.session["classroom"])

#################################################### Upload Section ####################################################
    try:
        code_temp = exam_quiz.text_template_content
        libs = None
        my_globals.limit_grader()
        if request.method == 'POST' and 'upload_submit' in request.POST:
            if request.FILES['upload']:
                uploaded_to_file = request.FILES['upload']
                code = uploaded_to_file.read().decode("utf-8")
                temp_code = code
                if uploaded_to_file._size > 1048576 or not uploaded_to_file.name.endswith(".py"):
                    return render(request, 'Exam/ExamGrader.html', {'title': exam_quiz.title,
                                                           'detail': exam_quiz.detail,
                                                           'message': True,
                                                           'code': code_temp,
                                                           'Deadtimestamp': deadline.timestamp() * 1000,
                                                           })
                code += '\n'
                for case_line in exam_quiz.text_testcase_content.splitlines():
                    if case_line.startswith('#lib') and len(case_line[5:]) != 0:
                        libs = case_line[5:].split(',')
                    code += case_line + "\n"
#################################################### Unittest Process. ####################################################
                class MyTestCase(unittest.TestCase):
                    num = 0
                    result = {
                        'max_score': 0,
                        'score': 0,
                        'case': {},
                    }
                def assert_equal(actual, expected, points=0, level=0):
                    MyTestCase.num += 1
                    eval(compile(my_globals.string(MyTestCase.num, actual, expected, points, level), 'defstr', 'exec'))
                    setattr(MyTestCase, "test_{0}".format(MyTestCase.num),locals()['test_{0}'.format(MyTestCase.num)])

                # Exec
                with stdoutIO() as gradingstr:
                    restricted_globals = dict(__builtins__=my_globals.mgb(globals(),libs))
                    eval(compile(code,'gradingstr', 'exec'),restricted_globals,locals())
                gradingstr_out = gradingstr.getvalue()
                test_suite = unittest.TestLoader().loadTestsFromTestCase(MyTestCase)
                test_result = TextTestRunner().run(test_suite)
#################################################### Result Section ####################################################
                result = MyTestCase.result
                if exam_quiz.mode == "Pass or Fail" and test_result.wasSuccessful():
                    result['status'] = "PASS"
                elif exam_quiz.mode == "Pass or Fail" and test_result.wasSuccessful() == False:
                    result['status'] = "FAIL"
                    result['score'] = 0
                elif exam_quiz.mode == "Scoring" and my_globals.scr(result['case']) is True:
                    result['status'] = "PASS"
                else:
                    result['status'] = "FAIL"

#################################################### Query Section ####################################################
                fileName = str(request.user.userId) + '_uploaded_' + str(exam_quiz.title) + '_' + str(exam_quiz.classroom.className) + request.FILES['upload'].name[-3:]
                in_sys_file_location = os.getcwd() + "/media/"
                temp_test = exam_quiz.classroom.className + '/' + request.user.userId + '/' + exam_quiz.title + '/'
                sys.path.append(in_sys_file_location)
                in_sys_file = FileSystemStorage().save(fileName, uploaded_to_file)
                in_sys_file_url = FileSystemStorage().url(in_sys_file)
                with open(in_sys_file_location + in_sys_file, 'w') as f:
                    f.write(temp_code)
                    Exam_Upload.objects.get_or_create(title=in_sys_file, exam=exam_data, Uploadfile=in_sys_file, user=request.user, quiz=exam_quiz)
                with open(in_sys_file_location + in_sys_file, 'a') as f:
                    f.write('\n\n')
                    for c,i in enumerate(result['case'].values()):
                        print(i)
                        f.write("CASE {0}: ".format(c+1) + i + '\n')
                    f.write("RESULT: %s" % result['status'])
                with open(in_sys_file_location + in_sys_file, 'r') as f:
                    try:
                        exam_quiz_score = Exam_Score.objects.get(exam=exam_data, quiz=exam_quiz, user=request.user)
                        if exam_quiz.mode == "Scoring":
                            if result['score'] >= exam_quiz_score.total_score:
                                exam_quiz_score.total_score = result['score']
                                exam_quiz_score.passOrFail = 0
                                exam_quiz_score.max_score = result['max_score']
                                exam_quiz_score.code = Exam_Upload.objects.get(title=in_sys_file)  # f.read()
                                exam_quiz_score.save()
                        else:
                            if result['score'] >= exam_quiz_score.passOrFail:
                                exam_quiz_score.total_score = 0
                                exam_quiz_score.passOrFail = result['score']
                                exam_quiz_score.max_score = result['max_score']
                                exam_quiz_score.code = Exam_Upload.objects.get(title=in_sys_file)  # f.read()
                                exam_quiz_score.save()
                    except ObjectDoesNotExist:
                        if exam_quiz.mode == "Scoring":
                            x = (1,0)
                        else:
                            x = (0,1)
                        exam_quiz_score = Exam_Score.objects.create(exam=exam_data,
                                                              quiz=exam_quiz,
                                                              user=request.user,
                                                              total_score=result['score']*x[0],
                                                              passOrFail=result['score']*x[1],
                                                              max_score=result['max_score'],
                                                              code=Exam_Upload.objects.get(title=in_sys_file)  # f.read(),
                                                              )
                    upload_instance = Exam_Upload.objects.get(title=in_sys_file, exam=exam_data, Uploadfile=in_sys_file, user=request.user,
                                                              quiz=exam_quiz)
                    if exam_quiz.mode == "Scoring":
                        if exam_quiz_score.total_score == None:
                            result['score'] = 0
                        upload_instance.score = result['score']
                    elif exam_quiz.mode == "Pass or Fail":
                        if exam_quiz_score.passOrFail == None:
                            result['score'] = 0
                        upload_instance.score = result['score']
                    upload_instance.save(update_fields=["score"])
                    # print(eval('dir()'))
            try:
                return render(request, 'Exam/ExamGrader.html', {'title': exam_quiz.title,
                                                       'detail': exam_quiz.detail,
                                                       'display': result,
                                                       'Case_Count': test_result.testsRun,
                                                       'mode': exam_quiz.mode,
                                                       'code': code_temp,
                                                       'prints': gradingstr_out,
                                                       'Deadtimestamp': deadline.timestamp() * 1000, })
            except Exception as e:
                # print(e)
                return render(request, 'Exam/ExamGrader.html', {'title': exam_quiz.title,
                                                       'detail': exam_quiz.detail,
                                                       'display': result,
                                                       'Case_Count': test_result.testsRun,
                                                       'mode': quiz.mode,
                                                       'code': code_temp,
                                                       'prints': gradingstr_out,
                                                       'Deadtimestamp': deadline.timestamp() * 1000, })

#################################################### Editor Section ####################################################
        elif request.method == 'POST' and 'code-form-submit' in request.POST:
            code = request.POST['code-form-comment']
            code_temp = code
            if code == '':
                return render(request, 'Exam/ExamGrader.html', {'title': exam_quiz.title,
                                                        'detail': exam_quiz.detail,
                                                        'Deadline': exam_data.deadline,
                                                        'code': code,
                                                   'Deadtimestamp':deadline.timestamp()*1000,
                                                       })
            else:
                rs = get_random_string(length=7)
                fileName = str(request.user.userId) + '_coded_' + str(exam_quiz.title) + '_' + str(exam_data.classroom.className) + '_' + rs +'.py'
                code += '\n'
                for case_line in exam_quiz.text_testcase_content.splitlines():
                    if case_line.startswith('#lib') and len(case_line[5:]) != 0:
                        libs = case_line[5:].split(',')
                    code += case_line + "\n"

#################################################### Unittest Process. ####################################################
                class MyTestCase(unittest.TestCase):
                    num = 0
                    result = {
                        'max_score': 0,
                        'score': 0,
                        'case': {},
                    }
                def assert_equal(actual, expected, points=0, level=0):
                    MyTestCase.num += 1
                    eval(compile(my_globals.string(MyTestCase.num, actual, expected, points, level), 'defstr', 'exec'))
                    setattr(MyTestCase, "test_{0}".format(MyTestCase.num),locals()['test_{0}'.format(MyTestCase.num)])

                # Exec
                with stdoutIO() as gradingstr:
                    restricted_globals = dict(__builtins__=my_globals.mgb(globals(),libs))
                    eval(compile(code,'gradingstr', 'exec'),restricted_globals,locals())
                    #eval(compile(quiz.text_testcase_content, 'gradingstr', 'exec'), globals(), locals())
                gradingstr_out = gradingstr.getvalue()#.split('\n')
                test_suite = unittest.TestLoader().loadTestsFromTestCase(MyTestCase)
                test_result = TextTestRunner().run(test_suite)
#################################################### Result Section ####################################################
                result = MyTestCase.result
                if exam_quiz.mode == "Pass or Fail" and test_result.wasSuccessful():
                    result['status'] = "PASS"
                elif exam_quiz.mode == "Pass or Fail" and test_result.wasSuccessful() is False:
                    result['status'] = "FAIL"
                    result['score'] = 0
                elif exam_quiz.mode == "Scoring" and my_globals.scr(result['case']) is True:
                    result['status'] = "PASS"
                else:
                    result['status'] = "FAIL"

#################################################### Query Section ####################################################
                with open('./media/' + fileName, 'w') as f:
                    f.write(code_temp)
                    Exam_Upload.objects.get_or_create(title=fileName, exam=exam_data, Uploadfile=fileName, user=request.user, quiz=exam_quiz)
                with open('./media/' + fileName, 'a') as f:
                    f.write('\n\n')
                    for c,i in enumerate(result['case'].values()):
                        f.write("CASE {0}: ".format(c+1) + i + '\n')
                    f.write("RESULT: %s" % result['status'])
                with open('./media/' + fileName, 'r') as f:
                    try:
                        exam_quiz_score = Exam_Score.objects.get(exam=exam_data, quiz=exam_quiz, user=request.user)
                        if exam_quiz.mode == "Scoring":
                            if result['score'] >= exam_quiz_score.total_score:
                                exam_quiz_score.total_score = result['score']
                                exam_quiz_score.passOrFail = 0
                                exam_quiz_score.max_score = result['max_score']
                                exam_quiz_score.code = Exam_Upload.objects.get(title=fileName) #f.read()
                                exam_quiz_score.save()
                        else:
                            if result['score'] >= exam_quiz_score.passOrFail:
                                exam_quiz_score.total_score = 0
                                exam_quiz_score.passOrFail = result['score']
                                exam_quiz_score.max_score = result['max_score']
                                exam_quiz_score.code = Exam_Upload.objects.get(title=fileName)  # f.read()
                                exam_quiz_score.save()
                        print(exam_quiz_score)
                    except ObjectDoesNotExist:
                        if exam_quiz.mode == "Scoring":
                            x = (1,0)
                        else:
                            x = (0,1)
                        exam_quiz_score = Exam_Score.objects.create(exam=exam_data,
                                                                    quiz=exam_quiz,
                                                                    user=request.user,
                                                                    total_score=result['score'] * x[0],
                                                                    passOrFail=result['score'] * x[1],
                                                                    max_score=result['max_score'],
                                                                    code=Exam_Upload.objects.get(title=fileName) # f.read(),
                                                                    )
                    upload_instance = Exam_Upload.objects.get(title=fileName, exam=exam_data, Uploadfile=fileName, user=request.user, quiz=exam_quiz)
                    if exam_quiz.mode == "Scoring":
                        if exam_quiz_score.total_score == None:
                            result['score'] = 0
                        upload_instance.score = result['score']
                    elif exam_quiz.mode == "Pass or Fail":
                        if exam_quiz_score.passOrFail == None:
                            result['score'] = 0
                        upload_instance.score = result['score']
                    upload_instance.save(update_fields=["score"])
                    #print(eval('dir()'))
            try:
                return render(request, 'Exam/ExamGrader.html', {'title': exam_quiz.title,
                                                       'detail': exam_quiz.detail,
                                                       'display': result,
                                                       'Case_Count': test_result.testsRun,
                                                       'mode': exam_quiz.mode,
                                                       'code': code_temp,
                                                       'prints': gradingstr_out,
                                                       'Deadtimestamp':deadline.timestamp()*1000,})
            except Exception as e:
                return render(request, 'Exam/ExamGrader.html', {'title': exam_quiz.title,
                                                                'detail': exam_quiz.detail,
                                                                'display': result,
                                                                'Case_Count': test_result.testsRun,
                                                                'mode': exam_quiz.mode,
                                                                'code': code_temp,
                                                                'prints': gradingstr_out,
                                                                'Deadtimestamp': deadline.timestamp() * 1000, })
        else:
            try:
                return render(request, 'Exam/ExamGrader.html', {'title': exam_quiz.title,
                                                           'detail': exam_quiz.detail,
                                                           'Deadline': exam_data.deadline,
                                                           'code': code_temp,
                                                           'Deadtimestamp': deadline.timestamp() * 1000,
                                                           })

            except ObjectDoesNotExist:
                return render(request, 'Exam/ExamGrader.html', {'title': exam_quiz.title,
                                                    'detail': exam_quiz.detail,
                                                    'Deadline': exam_data.deadline,
                                                    'code': code_temp,
                                                    'Deadtimestamp': deadline.timestamp()*1000,
                })
    except Exception as e:
        return render(request, 'Exam/ExamGrader.html',{'title': exam_quiz.title,
                                                'detail': exam_quiz.detail,
                                                'Deadline':exam_data.deadline,
                                                'exception':e,
                                                'code':code_temp,
                                                'Deadtimestamp':deadline.timestamp()*1000,
                                            })


#################################################### Measurement Of Software Similarity ####################################################
@login_required
def moss(request, classroom, quiz_id, mode):
    if (request.user.is_admin or request.user.groups.filter(name__in=[classroom + "_Teacher", classroom + "_TA"])) and mode is '0':
        userid = 367349587
        m = mosspy.Moss(userid, "python")
        for i in QuizScore.objects.filter(quizId__pk=quiz_id):
            try:
                m.addFile(i.code.Uploadfile.path)
            except Exception as E:
                #print(E)
                continue
        url = m.send()  # Submission Report URL
        #print("Report Url: " + url)
        return redirect(url)
    elif (request.user.is_admin or request.user.groups.filter(name__in=[classroom + "_Teacher", classroom + "_TA"])) and mode == '1':
        userid = 367349587
        m = mosspy.Moss(userid, "python")
        for i in Exam_Score.objects.filter(quiz__pk=quiz_id):
            try:
                m.addFile(i.code.Uploadfile.path)
            except Exception as E:
                # print(E)
                continue
        url = m.send()  # Submission Report URL
        # print("Report Url: " + url)
        return redirect(url)
    else:
        return HttpResponseRedirect("/ClassRoom/"+classroom)
