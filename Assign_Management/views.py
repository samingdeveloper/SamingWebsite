from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect
from django.http import HttpResponse
from django.template import loader
from django.middleware.csrf import CsrfViewMiddleware

# Create your views here.
def CreateAssignment(request):
    return render(request,'CreateAssignment.html')

def AssignmentDetail(request):
    return render(request,'AssignmentDetail.html')
