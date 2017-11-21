from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from django.middleware.csrf import CsrfViewMiddleware
from Class_Management.models import ClassRoom, Quiz
from Assign_Management.models import Upload
from django.contrib.auth.models import User
import unittest
import importlib
from unittest import TextTestRunner
from django.conf import settings
from django.core.files.storage import FileSystemStorage

# Create your views here.


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
    elif request.method == 'POST' and request.FILES['upload']:
        myfile = request.FILES['upload']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)

        f = open('.'+str(uploaded_file_url)+".py", 'r+')
        case = quiz.text_testcase_content
        for case_line in case.splitlines():
            if (case_line=="# Test case"):
                test_case_count += 1
                Out_count += 1
            f.write(case_line+"\n")
        for i in range(test_case_count):
            i += 1
            globals()['test_case_out_%s' % i] = ""
            globals()['out_%s' % i] = ""
        code = f.read()
        code = code.lower()
        prob = importlib.import_module(uploaded_file_url)
        for line in f:
            # print(line)
            if "# Stop" in line:
                for i in range(test_case_count):
                    i+=1
                    globals()['test_case_out_%s' % i] = ""
                    globals()['out_%s' % i] = ""
                test_case_count = 0
                Out_count = 0
                write_mode = False

            if write_mode:
                if "# Out" in line:
                    globals()['out_%s' % test_case_num] = eval(line[7:-1])
                elif "# Break" in line:
                    write_mode = False
                command = line.replace('print(', 'prob.')
                #print(command)
                try:
                    globals()['test_case_out_%s' % test_case_num] = eval(command[:-2])
                    globals()['test_case_out_%s' % test_case_num] = str(globals()['test_case_out_%s' % test_case_num]) + "\n"

                except:
                    # print("Error Occur")
                    continue

            if "# Test case" in line:
                test_case_num = str(line[11])
                write_mode = True

        #unittest process.
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
                    self.assertEqual(text_2,  mt_2)
            if (test_case_count > 2):
                def test_text_three(self):
                    text_3 = test_case_out_3
                    mt_3 = out_3
                    self.assertEqual(text_3,  mt_3)

        test_suite = unittest.TestLoader().loadTestsFromTestCase(MyTestCase)
        test_result = TextTestRunner().run(test_suite)
        x = len(test_result.failures)
        if x==3:
            result = "PASS"
        else:
            result = "FAIL"

        #sent infomations to page.
        return render(request, 'Upload.html', {
            'quizTitle': quiz.quizTitle,
            'quizDetail': quiz.quizDetail,
            'Deadline': quiz.deadline,
            'Hint': quiz.hint,
            'uploaded_file_url': uploaded_file_url,
            'display': result,
        })
    else:
        return render(request, 'Upload.html', {'quizTitle':quiz.quizTitle,
                                           'quizDetail':quiz.quizDetail,
                                           'Deadline':quiz.deadline,
                                           'Hint':quiz.hint,
        })


def code(request, quiz_id):
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
        })