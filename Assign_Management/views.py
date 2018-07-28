from django.shortcuts import render, HttpResponseRedirect, redirect
#from django.http import HttpResponse
#from django.template import loader
#from django.middleware.csrf import CsrfViewMiddleware
from Class_Management.models import *
from Assign_Management.models import Upload
from Assign_Management.storage import OverwriteStorage
from django.contrib.auth import get_user_model
import sys,os,datetime,importlib,unittest,timeout_decorator,mosspy,contextlib
from io import StringIO
#from RestrictedPython import compile_restricted,utility_builtins,limited_builtins
#from RestrictedPython.Guards import safe_builtins
from unittest import TextTestRunner
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.exceptions import ObjectDoesNotExist
from . import my_globals
User = get_user_model()
# Create your views here.

sys.path.append(os.getcwd()+"/media")

####################### Utility #######################
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
####################### url #######################

def CreateAssignment(request):
    if not request.user.is_authenticated or not request.user.is_admin:
        return HttpResponseRedirect('/LogOut')
    else:
        return render(request,'CreateAssignment.html')


def AssignmentDetail(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/LogOut')
    return render(request, 'Home.html')



def GenerateAssign(request,classroom):
    if not request.user.is_authenticated or not request.user.is_admin:
        return HttpResponseRedirect('/LogOut')
    elif request.method == "POST": #and request.FILES['upload_testcase']:
        try:
            if request.POST['asname'] == '':
                raise ValueError("Assignment must have a name!")
            OSS = OverwriteStorage()
            var = request.user.userId
            Assignment = request.POST.get('asname', '')
            Assignment_Detail = request.POST.get('asdetail', '')
            Deadline = request.POST.get('dateInput','')
            Hint = request.POST.get('hint','')
            Timer = request.POST.get('timer','')
            #dsa = 'upload_testcase' in request.POST and request.POST['upload_testcase']
            test_case = request.POST.get('upload_testcase','')
            code_template = request.POST.get('upload_template','')
            mode = request.POST.get('mode','')
            GenerateAssign_instance = Quiz.objects.create(quizTitle=Assignment, quizDetail=Assignment_Detail, deadline=Deadline,text_template_content=code_template ,text_testcase_content=test_case  ,hint=Hint, mode=mode, classroom=ClassRoom.objects.get(className=classroom))
            GenerateAssign_instance_temp = Quiz.objects.get(quizTitle=Assignment, quizDetail=Assignment_Detail, deadline=Deadline,text_template_content=code_template ,text_testcase_content=test_case  ,hint=Hint, mode=mode, classroom=ClassRoom.objects.get(className=classroom))
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
            return render(request,"CreateAssignment.html")
    else:
        return render(request, 'CreateAssignment.html')


def DeleteAssign(request, classroom, quiz_id):
    if not request.user.is_authenticated or not request.user.is_admin:
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

def regen(require_regen):
    test_temp = Quiz.objects.create(
        quizTitle=require_regen["quizTitle"],
        quizDetail=require_regen["quizDetail"],
        deadline=require_regen["deadline"],
        hint=require_regen["hint"],
        text_testcase_content=require_regen["text_testcase_content"],
        text_template_content=require_regen["text_template_content"],
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

def EditAssign(request, classroom, quiz_id):
    if not request.user.is_authenticated or not request.user.is_admin:
        return HttpResponseRedirect('/LogOut')
    elif request.method == "POST":
        try:
            if request.POST['asname'] == '':
                raise ValueError("Assignment must have a name!")
            quiz = Quiz.objects.get(pk=quiz_id)
            OSS = OverwriteStorage()
            var = request.user.userId
            Assignment = request.POST.get('asname', '')
            Assignment_Detail = request.POST.get('asdetail', '')
            Deadline = request.POST.get('dateInput', '')
            Hint = request.POST.get('hint', '')
            Timer = request.POST.get('timer', '')
            asd = request.FILES.get('upload_testcase', False)
            asdf = request.FILES.get('upload_template', False)
            mode = request.POST.get('mode', '')
            redo = request.POST.get('redo', '')
            test_case = request.POST.get('upload_testcase', False)
            code_template = request.POST.get('upload_template', False)
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
                                 "hint":Hint,
                                 "text_testcase_content":test_case,
                                 "text_template_content":code_template,
                                 "mode":mode,
                                 "classroom":quiz.classroom,
                                 "Timer":Timer,
                                 })
                #print("ppl=sh!t")

            else:
                get_tracker = QuizTracker.objects.filter(
                    classroom=quiz.classroom)  # reference at QuizTracker
                quiz.quizTitle = Assignment
                quiz.quizDetail = Assignment_Detail
                quiz.deadline = Deadline
                quiz.hint = Hint
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
                        timer = QuizTimer.objects.get(quizId=quiz_id,
                                                      userId=j.userId,
                                                      classroom=quiz.classroom,
                                                      )
                        return None
                        if timer.start:
                            timer.timer = x
                            timer.timer_stop = timezone.now() + timezone.timedelta(seconds=timer.timer)
                        else:
                            timer.timer = x
                            timer.timer_stop = None
                        timer.save(update_fields=["timer", "timer_stop"])
            return HttpResponseRedirect('/ClassRoom/'+request.session["classroom"])
        except Exception as E:
            from django.contrib import messages
            messages.error(request, E)
            return HttpResponseRedirect('/ClassRoom/' + request.session["classroom"] + '/Assignment/EditAssign/' + quiz_id)


    else:
        quiz = Quiz.objects.get(pk=quiz_id)
        try:
            quizTimer = QuizTimer.objects.get(quizId=quiz)
        except:
            quizTimer = ''
        context = {'quizedit': quiz,
                   'quiztedit': quizTimer,
                   'quizdedit': quiz.deadline,
                  }
        return render(request, 'EditAssignment.html', context)

#@timeout_decorator.timeout(10, use_signals=False)
def uploadgrading(request, classroom, quiz_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/LogOut')

    elif ClassRoom.objects.get(className=classroom).user.filter(userId=request.user.userId).exists() != True and not request.user.is_admin:
        return HttpResponseRedirect('/ClassRoom/' + request.session["classroom"])

    global deadline, timer_stop, name
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
        if t >= deadline or t >= timer_stop:
            return HttpResponseRedirect('/ClassRoom/'+request.session["classroom"])
    elif Timer is None:
        #print("Timer is None.")
        deadline =  timezone.localtime(quiz.deadline)
        deadline.astimezone(timezone.utc).replace(tzinfo=None)
        #print(t)
        #print(deadline)
        if t >= deadline:
            return HttpResponseRedirect('/ClassRoom/'+request.session["classroom"])

    try:
        code_temp = quiz.text_template_content
        if request.method == "POST" and 'time_left' in request.POST:
            #print("this?")
            time_left = request.POST.get("time_left",'')
            #print(time_left)
            try:
                timer = QuizTimer.objects.get(
                    quizId=quiz,
                    userId=User.objects.get(userId=request.user.userId),
                    classroom=quiz.classroom, )
                timer.timer = time_left
                timer.save(update_fields=["timer"])
            except ObjectDoesNotExist:
                pass
            return HttpResponseRedirect('/ClassRoom/' + request.session["classroom"])

        elif request.method == 'POST' and 'upload_submit' in request.POST:
            if request.FILES['upload']:
                #print("in_upload_submit")
                uploaded_to_file = request.FILES['upload']
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
                fileName = str(request.user.userId) + '_uploaded_' + str(quiz.quizTitle) + '_' + str(quiz.classroom.className)+ uploaded_to_file.name[-3:]
                #OSS = OverwriteStorage()
                #in_sys_file = OSS.save(fileName, uploaded_to_file)
                fuck_sake = Quiz.objects.get(id=quiz_id)
                in_sys_file_location = os.getcwd()+"/media/"#+fuck_sake.classroom.className+'/'+request.user.userId+'/'+fuck_sake.quizTitle+'/'
                temp_test = fuck_sake.classroom.className+'/'+request.user.userId+'/'+fuck_sake.quizTitle+'/'
                sys.path.append(in_sys_file_location)
                FSS = FileSystemStorage()#(location=in_sys_file_location,
                                        #base_url=os.path.join(temp_test))
                in_sys_file = FSS.save(fileName, uploaded_to_file)
                in_sys_file_url = FSS.url(in_sys_file)
                #print(FSS.path(in_sys_file))
                Upload.objects.get_or_create(title=in_sys_file, Uploadfile=in_sys_file ,user=request.user, quiz=quiz, classroom=quiz.classroom)
                # global dict variable for each user
                name = request.user.userId
                result = {
                    'max_score': 0,
                    'score': 0,
                    'case': [],
                }
                globals()[name] = result
                ####################################
                # open file .txt. Address  file ???????? Now! change follow your PC
                with open(in_sys_file_location + in_sys_file, 'r+') as f:
                    code = code_origin = f.read()
                    restricted_globals = dict(__builtins__=my_globals.mgb())
                    eval(compile(code, filename=in_sys_file_location + in_sys_file, mode='exec'), restricted_globals, {})
                    f.seek(0, 0)
                    if "# lib" in quiz.text_testcase_content.splitlines()[0]:
                        f.write("import ".rstrip('\r\n') + quiz.text_testcase_content.splitlines()[0][6:].rstrip(
                            '\r\n') + '\n' + code)
                        # libs = quiz.text_testcase_content.splitlines()[0][6:].split(" ")
                        # print(libs)
                    # else:
                    # libs = []

                if in_sys_file[:-3] in sys.modules:
                    del sys.modules[in_sys_file[:-3]]
                    #importlib.invalidate_caches()
                    prob = importlib.import_module(in_sys_file[:-3])
                    #importlib.reload(prob)
                else:
                    prob = importlib.import_module(in_sys_file[:-3])
                    #importlib.reload(prob)
                #print(prob)
                #setattr(module, 'prob', prob)
                with open(in_sys_file_location + in_sys_file, 'a') as f:
                    case = quiz.text_testcase_content
                    f.write('\n')
                    for case_line in case.splitlines():
                        f.write(case_line + "\n")
                with open(in_sys_file_location + in_sys_file, 'r') as f:
                    code = f.read()

                # unittest process.
                class MyTestCase(unittest.TestCase):
                    pass

                def assert_equal(actual, expected, points, hidden=False):
                    rand_string = get_random_string(length=7)
                    string = "def test_{0}(self):\n" \
                             "    self.actual = {1}\n" \
                             "    self.expected = {2}\n" \
                             "    self.points = {3}\n" \
                             "    self.hidden = {4}\n" \
                             "    globals()[name]['max_score'] += self.points\n" \
                             "    try:\n" \
                             "        self.assertEquals(self.actual, self.expected)\n" \
                             "        if self.hidden != True:\n" \
                             "            globals()[name]['case'].append('PASS')\n" \
                             "        globals()[name]['score'] += self.points\n" \
                             "    except:\n" \
                             "        if self.hidden != True:\n" \
                             "            globals()[name]['case'].append('FAIL')\n" \
                             "        raise\n".format(rand_string, actual, expected, points, hidden)
                    # print(locals())
                    with stdoutIO() as s:
                        eval(compile(string, 'defstr', 'exec'), globals(), locals())
                    # print(str(actual)+str(expected)+str(points)+str(hidden))
                    # print(string)
                    # print(globals())
                    # print(globals()[name]['params'])
                    # print(str_to_class('test_{0}'.format(rand_string)))
                    setattr(MyTestCase, "test_{0}".format(rand_string), locals()['test_{0}'.format(rand_string)])
                    # setattr(MyTestCase, "test_{0}".format(rand_string), str_to_class('test_{0}'.format(rand_string)))
                    # method_list = [func for func in dir(MyTestCase) if callable(getattr(MyTestCase, func)) and not func.startswith("__")]
                    # print(method_list)

                # Exec
                with stdoutIO() as gradingstr:
                    eval(compile(code,'gradingstr', 'exec'))
                gradingstr_out = gradingstr.getvalue()#.split('\n')
                # return None
                test_suite = unittest.TestLoader().loadTestsFromTestCase(MyTestCase)
                test_result = TextTestRunner().run(test_suite)
                # fail = len(test_result.failures)
                result = globals()[name]
                print(result)
                del globals()[name]
                del name
                if quiz.mode == "Pass or Fail" and test_result.wasSuccessful():
                    result['status'] = "PASS"
                elif quiz.mode == "Pass or Fail" and test_result.wasSuccessful() == False:
                    result['status'] = "FAIL"
                    result['score'] = 0
                elif quiz.mode == "Scoring" and any(result['case']) == True:
                    result['status'] = "PASS"
                else:
                    result['status'] = "FAIL"
                # print(case)
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
                with open(in_sys_file_location + in_sys_file, 'w') as f:
                    f.write(code_origin)
                with open(in_sys_file_location + in_sys_file, 'a') as f:
                    f.write('\n\n')
                    for c, i in enumerate(result['case']):
                        f.write("CASE {0}: ".format(c + 1) + i + '\n')
                    f.write("RESULT: %s" % result['status'])
                f = open(in_sys_file_location + in_sys_file, 'r')
                try:
                    quiz_score = QuizScore.objects.get(quizId=quiz,
                                                       userId=User.objects.get(userId=request.user.userId),
                                                       classroom=quiz.classroom)
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
                f.close()
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
                with open('./media/' + fileName, 'w') as f:
                    for debug_line in code:
                        #print(debug_line)
                        f.write(debug_line)
                Upload.objects.get_or_create(title=fileName, Uploadfile=fileName, user=request.user, quiz=quiz, classroom=quiz.classroom)
                # global dict variable for each user
                name = request.user.userId
                result = {
                            'max_score':0,
                            'score':0,
                            'case':[],
                          }
                globals()[name] = result
                ####################################
                # open file .txt. Address  file ???????? Now! change follow your PC
                with open('./media/' + fileName, 'r+') as f:
                    code = f.read()
                    restricted_globals = dict(__builtins__=my_globals.mgb()) # pass libs as parameters
                    eval(compile(code, filename='./media/' + fileName, mode='exec'), restricted_globals, {})
                    f.seek(0, 0)
                    if "# lib" in quiz.text_testcase_content.splitlines()[0]:
                        f.write("import ".rstrip('\r\n') + quiz.text_testcase_content.splitlines()[0][6:].rstrip('\r\n') + '\n' + code)
                        # libs = quiz.text_testcase_content.splitlines()[0][6:].split(" ")
                        # print(libs)
                    #else:
                        #libs = []

                if fileName[:-3] in sys.modules:
                    del sys.modules[fileName[:-3]]
                    # importlib.invalidate_caches()
                    prob = importlib.import_module(fileName[:-3])
                    # importlib.reload(prob)
                else:
                    prob = importlib.import_module(fileName[:-3])
                    # importlib.reload(prob)
                    # print(prob)
                #setattr(module, 'prob', prob)
                #return None
                with open('./media/' + fileName, 'a') as f:
                    case = quiz.text_testcase_content
                    f.write('\n')
                    for case_line in case.splitlines():
                        f.write(case_line + "\n")
                with open('./media/' + fileName, 'r') as f:
                    code = f.read()

                # unittest process.
                class MyTestCase(unittest.TestCase): pass
                def assert_equal(actual, expected, points, hidden=False):
                    rand_string = get_random_string(length=7)
                    string = "def test_{0}(self):\n" \
                             "    self.actual = {1}\n" \
                             "    self.expected = {2}\n" \
                             "    self.points = {3}\n" \
                             "    self.hidden = {4}\n" \
                             "    globals()[name]['max_score'] += self.points\n" \
                             "    try:\n" \
                             "        self.assertEquals(self.actual, self.expected)\n" \
                             "        if self.hidden != True:\n" \
                             "            globals()[name]['case'].append('PASS')\n" \
                             "        globals()[name]['score'] += self.points\n" \
                             "    except:\n" \
                             "        if self.hidden != True:\n" \
                             "            globals()[name]['case'].append('FAIL')\n" \
                             "        raise\n".format(rand_string,actual,expected,points,hidden)
                    #print(locals())
                    eval(compile(string, 'defstr', 'exec'), globals(), locals())
                    #print(str(actual)+str(expected)+str(points)+str(hidden))
                    #print(string)
                    #print(globals())
                    #print(globals()[name]['params'])
                    #print(str_to_class('test_{0}'.format(rand_string)))
                    setattr(MyTestCase, "test_{0}".format(rand_string),locals()['test_{0}'.format(rand_string)])
                    #setattr(MyTestCase, "test_{0}".format(rand_string), str_to_class('test_{0}'.format(rand_string)))
                    #method_list = [func for func in dir(MyTestCase) if callable(getattr(MyTestCase, func)) and not func.startswith("__")]
                    #print(method_list)
                # Exec
                with stdoutIO() as gradingstr:
                    eval(compile(code,'gradingstr', 'exec'))
                gradingstr_out = gradingstr.getvalue()#.split('\n')
                #print(gradingstr_out)
                #return None
                test_suite = unittest.TestLoader().loadTestsFromTestCase(MyTestCase)
                test_result = TextTestRunner().run(test_suite)
                #fail = len(test_result.failures)
                result = globals()[name]
                print(result)
                del globals()[name]
                del name
                if quiz.mode == "Pass or Fail" and test_result.wasSuccessful():
                    result['status'] = "PASS"
                elif quiz.mode == "Pass or Fail" and test_result.wasSuccessful() == False:
                    result['status'] = "FAIL"
                    result['score'] = 0
                elif quiz.mode == "Scoring" and any(result['case']) == True:
                    result['status'] = "PASS"
                else:
                    result['status'] = "FAIL"
                #print(case)
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
                with open('./media/' + fileName, 'a') as f:
                    f.write('\n\n')
                    for c,i in enumerate(result['case']):
                        f.write("CASE {0}: ".format(c+1) + i + '\n')
                    f.write("RESULT: %s" % result['status'])
                f = open('./media/' + fileName, 'r')
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
                f.close()
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

def moss(request, classroom, quiz_id):
    if request.user.is_admin:
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
    else:
        return HttpResponseRedirect("/ClassRoom/"+classroom)
