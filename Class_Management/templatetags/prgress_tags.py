from django import template
from ..models import *
from django.core.exceptions import ObjectDoesNotExist
register = template.Library()

@register.simple_tag
def u_progress(userId, classroom):
    try:
        tracker = QuizTracker.objects.get(userId=userId, classroom__className=classroom)
        return (tracker.quizDoneCount/Quiz.objects.filter(classroom__className=classroom).count())*100
    except:
        return 0



#{{ i.quiztracker_set.all.0.quizDoneCount|div:quiz_count|mul:100 }}