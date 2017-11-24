from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from django.middleware.csrf import CsrfViewMiddleware
from Class_Management.models import ClassRoom, Quiz
from Assign_Management.models import Upload
from Assign_Management.storage import OverwriteStorage
from django.contrib.auth.models import User
import unittest
import importlib
import sys
from unittest import TextTestRunner
from django.conf import settings
from django.core.files.storage import FileSystemStorage

# Create your views here.

sys.path.append('D:/Work/Django_Project/KMUTT_FIBO/241_Grading/SamingDev/media')
def CreateAssignment(request):
    var = request.session['var']
    if not request.user.is_authenticated or not request.user.is_superuser:
        return HttpResponseRedirect('/LogOut')
    else:
        return render(request,'CreateAssignment.html')


def AssignmentDetail(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/LogOut')
    return render(request, 'Home.html')



def GenerateAssign(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return HttpResponseRedirect('/LogOut')
    elif request.method == "POST" and request.FILES['upload_testcase']:
        var = request.session['var']
        Assignment = request.POST.get('Assignment', '')
        Assignment_Detail = request.POST.get('Assignment2', '')
        Deadline = request.POST.get('dateInput','')
        Hint = request.POST.get('hint','')
        dsa = 'upload_testcase' in request.POST and request.POST['upload_testcase']
        asd = request.FILES.get('upload_testcase',False)
        asdf = request.FILES.get('upload_template',False)
        dab = asd.read()
        dabb = asdf.read()
        print(dsa)
        print(dab)
        print(dabb)
        GenerateAssign_instance = Quiz.objects.create(quizTitle=Assignment, quizDetail=Assignment_Detail, deadline=Deadline,text_template_content=dabb ,text_testcase_content=dab  ,hint=Hint,classroom=ClassRoom.objects.get(id=User.objects.get(username=var).extraauth.year))
        #GenerateAssign_instance.save()
        return HttpResponseRedirect('/ClassRoom/Home')
    else:
        return render(request, 'CreateAssignment.html')


def DeleteAssign(request, quiz_id):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return HttpResponseRedirect('/LogOut')
    quiz = Quiz.objects.get(pk=quiz_id)
    quiz.delete()
    return HttpResponseRedirect('/ClassRoom/Home')


def uploadgrading(request, quiz_id):
    quiz = Quiz.objects.get(pk=quiz_id)
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/LogOut')
    elif request.method == 'POST' and 'upload_submit' in request.POST:
        if request.FILES['upload']:
            print("in_upload_submit")
            uploaded_to_file = request.FILES['upload']
            #fileName = str(request.user) + '_uploaded_' + uploaded_to_file.name + '_' + str(quiz) + '_' + 'script.py'
            fileName = uploaded_to_file.name
            OSS = OverwriteStorage()
            in_sys_file = OSS.save(fileName, uploaded_to_file)
            #myfile = open('./media/' + fileName, 'w')f
            Upload.objects.get_or_create(title=fileName, Uploadfile=in_sys_file ,user=request.user, quiz=quiz)
            #myfile.close()
            write_mode = False
            test_case_count = 0
            Out_count = 0
            # open file .txt. Address  file ???????? Now! change follow your PC
            f = open('./media/' + fileName, 'a')
            case = quiz.text_testcase_content
            f.write("\n\n")
            for case_line in case.splitlines():
                if (case_line[:11] == "# Test case"):
                    test_case_count += 1
                    Out_count += 1
                f.write(case_line + "\n")
            for i in range(test_case_count):
                i += 1
                globals()['test_case_out_%s' % i] = ""
                globals()['out_%s' % i] = ""
            f = open('./media/' + fileName, 'r')
            code = f.read()
            f.close()
            # code = code.lower()
            prob = importlib.import_module(fileName[:-3])
            for line in code.splitlines():
                print(line)
                if "# Stop" in line:
                    print("stop")
                    write_mode = False

                if write_mode:
                    if "# Out" in line:
                        globals()['out_%s' % test_case_num] = eval(line[6:])
                    elif "# Break" in line:
                        print("Break!")
                        write_mode = False
                    command = line.replace('print(', 'prob.')

                    try:
                        globals()['test_case_out_%s' % test_case_num] = eval(command[:-1])
                        # globals()['test_case_out_%s' % test_case_num] = str(globals()['test_case_out_%s' % test_case_num]) + "\n"


                    except:
                        continue

                if "# Test case" in line:
                    print("in testcase  ")
                    test_case_num = str(line[11])
                    write_mode = True

            # unittest process.
            class MyTestCase(unittest.TestCase):
                if (test_case_count > 0):
                    def test_text(self):
                        text_1 = test_case_out_1
                        mt_1 = out_1
                        self.assertEquals(text_1, mt_1)
                if (test_case_count > 1):
                    def test_text_two(self):
                        text_2 = test_case_out_2
                        mt_2 = out_2
                        self.assertEqual(text_2, mt_2)
                if (test_case_count > 2):
                    def test_text_three(self):
                        text_3 = test_case_out_3
                        mt_3 = out_3
                        self.assertEqual(text_3, mt_3)
                if (test_case_count > 3):
                    def test_text_three(self):
                        text_4 = test_case_out_4
                        mt_4 = out_4
                        self.assertEqual(text_4, mt_4)
                if (test_case_count > 4):
                    def test_text_three(self):
                        text_5 = test_case_out_5
                        mt_5 = out_5
                        self.assertEqual(text_5, mt_5)

            test_suite = unittest.TestLoader().loadTestsFromTestCase(MyTestCase)
            test_result = TextTestRunner().run(test_suite)
            x = len(test_result.failures)
            if x == 0:
                result = "PASS"
            else:
                result = "FAIL"
            print(str(test_case_count) + ' ' + str(Out_count))
            for i in range(test_case_count):
                i += 1
                globals()['test_case_out_%s' % i] = ""
                globals()['out_%s' % i] = ""
            test_case_count = 0
            Out_count = 0
        return render(request, 'Upload.html', {'quizTitle': quiz.quizTitle,
                                               'quizDetail': quiz.quizDetail,
                                               'Deadline': quiz.deadline,
                                               'Hint': quiz.hint,
                                               'display': result,})

    elif request.method == 'POST' and 'code-form-submit' in request.POST:
        code = request.POST['code-form-comment']
        print("in-code-form")
        if code == '':
            return render(request, 'Upload.html', {'quizTitle': quiz.quizTitle,
                                                    'quizDetail': quiz.quizDetail,
                                                    'Deadline': quiz.deadline,
                                                    'Hint': quiz.hint,
                                                    'code': code, })
        else:
            fileName = str(request.user) + '_' + str(quiz) + '_' + 'scrip.py'
            f = open('./media/' + fileName, 'w')
            f.write(code)
            f.close()
            Upload.objects.get_or_create(title=fileName, fileUpload='./media/' + fileName, user=request.user, quiz=quiz)
            write_mode = False
            test_case_count = 0
            Out_count = 0
            # open file .txt. Address  file ???????? Now! change follow your PC
            f = open('./media/' + fileName, 'a')
            case = quiz.text_testcase_content
            f.write("\n\n")
            for case_line in case.splitlines():
                if (case_line[:11] == "# Test case"):
                    test_case_count += 1
                    Out_count += 1
                f.write(case_line + "\n")
            f.close()
            for i in range(test_case_count):
                i += 1
                globals()['test_case_out_%s' % i] = ""
                globals()['out_%s' % i] = ""
            # code = code.lower()
            f = open('./media/' + fileName, 'r')
            code = f.read()
            f.close()
            prob = importlib.import_module(fileName[:-3])
            for line in code.splitlines():
                #print(line)
                if "# Stop" in line:
                    print("stop")
                    write_mode = False

                if write_mode:
                    if "# Out" in line:
                        print("Out")
                        globals()['out_%s' % test_case_num] = eval(line[6:])
                    elif "# Break" in line:
                        print("Break!")
                        write_mode = False
                    command = line.replace('print(', 'prob.')

                    try:
                        print("try")
                        globals()['test_case_out_%s' % test_case_num] = eval(command[:-1])
                        # globals()['test_case_out_%s' % test_case_num] = str(globals()['test_case_out_%s' % test_case_num]) + "\n"


                    except:
                        continue

                if "# Test case" in line:
                    print("in testcase  ")
                    test_case_num = str(line[11])
                    write_mode = True

            # unittest process.
            class MyTestCase(unittest.TestCase):
                if (test_case_count > 0):
                    def test_text(self):
                        text_1 = test_case_out_1
                        mt_1 = out_1
                        self.assertEquals(text_1, mt_1)
                if (test_case_count > 1):
                    def test_text_two(self):
                        text_2 = test_case_out_2
                        mt_2 = out_2
                        self.assertEqual(text_2, mt_2)
                if (test_case_count > 2):
                    def test_text_three(self):
                        text_3 = test_case_out_3
                        mt_3 = out_3
                        self.assertEqual(text_3, mt_3)
                if (test_case_count > 3):
                    def test_text_three(self):
                        text_4 = test_case_out_4
                        mt_4 = out_4
                        self.assertEqual(text_4, mt_4)
                if (test_case_count > 4):
                    def test_text_three(self):
                        text_5 = test_case_out_5
                        mt_5 = out_5
                        self.assertEqual(text_5, mt_5)

            test_suite = unittest.TestLoader().loadTestsFromTestCase(MyTestCase)
            test_result = TextTestRunner().run(test_suite)
            x = len(test_result.failures)
            if x == 0:
                result = "PASS"
            else:
                result = "FAIL"
            print(str(test_case_count) + ' ' + str(Out_count))
            for i in range(test_case_count):
                i += 1
                globals()['test_case_out_%s' % i] = ""
                globals()['out_%s' % i] = ""
            test_case_count = 0
            Out_count = 0
            f = open('./media/' + fileName, 'r')
            temp_f = f.readlines()
            f.close()
            f = open('./media/' + fileName, 'w')
            for m in temp_f:
                if "# Test case" in m:
                    break
                else:
                    f.write(m)
            f.close()
            f = open('./media/' + fileName, 'r')
            code = f.read()
            f.close()

        #sent infomations to page.
            return render(request, 'Upload.html', {
                'quizTitle': quiz.quizTitle,
                'quizDetail': quiz.quizDetail,
                'Deadline': quiz.deadline,
                'Hint': quiz.hint,
                'display': result,
                'code': code,
        })
    else:
        print("not-in-code-form")
        return render(request, 'Upload.html', {'quizTitle':quiz.quizTitle,
                                           'quizDetail':quiz.quizDetail,
                                           'Deadline':quiz.deadline,
                                           'Hint':quiz.hint,
        })


'''def code(request, quiz_id):
    quiz = Quiz.objects.get(pk=quiz_id)
    if request.method == 'POST':
        code = request.POST['code-form-comment']
        if code == '':
            return render(request, 'Upload.html', {'quizTitle': quiz.quizTitle,
                                                   'quizDetail': quiz.quizDetail,
                                                   'Deadline': quiz.deadline,
                                                   'Hint': quiz.hint,
                                                   'code': code,})
        else:
            fileName = str(request.user)+'_'+str(quiz)+'_'+'scrip.py'
            myfile = open('./media/'+fileName, 'w')
            myfile.write(code)
            myfile.close()
            Upload.objects.get_or_create(title=fileName, fileUpload='./media/'+fileName, user=request.user, quiz=quiz)

        return render(request, 'Upload.html', {'quizTitle':quiz.quizTitle,
                                           'quizDetail':quiz.quizDetail,
                                           'Deadline':quiz.deadline,
                                           'Hint':quiz.hint,
                                        'code' : code,
        })
    else:
        return render(request, 'Upload.html', {'quizTitle':quiz.quizTitle,
                                           'quizDetail':quiz.quizDetail,
                                           'Deadline':quiz.deadline,
                                           'Hint':quiz.hint,
        })'''