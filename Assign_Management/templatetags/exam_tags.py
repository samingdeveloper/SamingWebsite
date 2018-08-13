from django import template
from ..models import *
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist
register = template.Library()

@register.simple_tag
def your_exam(user, classname, picked_list):
    return Exam_Quiz.objects.filter(classroom__className=classname,title__in=picked_list)