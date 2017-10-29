from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from django.middleware.csrf import CsrfViewMiddleware
from Class_Management.models import ClassRoom,Quiz
from django.contrib.auth.models import User
import unittest
from unittest import TextTestRunner

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
        Hint = request.POST.get('hint','')
        GenerateAssign_instance = Quiz.objects.create(quizTitle=Assignment, quizDetail=Assignment_Detail, deadline=Deadline, hint=Hint,classroom=ClassRoom.objects.get(id=User.objects.get(username=var).extraauth.year)),
        #GenerateAssign_instance.save()
        return HttpResponseRedirect('/ClassRoom/Home')

def DeleteAssign(request, quiz_id):
    quiz = Quiz.objects.get(pk=quiz_id)
    quiz.delete()
    return HttpResponseRedirect('/ClassRoom/Home')

def upload(request):
    return render(request, 'Upload.html')




