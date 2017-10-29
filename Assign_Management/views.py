from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect
from django.http import HttpResponse
from django.template import loader
from django.middleware.csrf import CsrfViewMiddleware
from Class_Management.models import ClassRoom,Quiz
from django.contrib.auth.models import User

# Create your views here.
def CreateAssignment(request):
    return render(request,'CreateAssignment.html')

def AssignmentDetail(request):
    return render(request,'Home.html')

def GenerateAssign(request):
    if request.method == "POST":
        var = request.session['var']
        Assignment = request.POST.get('Assignment', '')
        Assignment_Detail = request.POST.get('Assignment2', '')
        Deadline = request.POST.get('dateInput','')
        GenerateAssign_instance = Quiz.objects.create(quizTitle=Assignment, quizDetail=Assignment_Detail, deadline=Deadline, classroom=ClassRoom.objects.get(id=User.objects.get(username=var).extraauth.year)),
        #GenerateAssign_instance.save()
        return HttpResponseRedirect('/ClassRoom/Home')


