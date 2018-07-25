from django import template
from ..models import *
from django.core.exceptions import ObjectDoesNotExist
register = template.Library()

@register.simple_tag
def u_progress(userId, classroom):
    try:
        tracker = QuizTracker.objects.get(userId=userId, classroom__className=classroom)
        percent = (tracker.quizDoneCount/Quiz.objects.filter(classroom__className=classroom).count())*100
        return percent if percent < 100 else 100
    except:
        return 0



#{{ i.quiztracker_set.all.0.quizDoneCount|div:quiz_count|mul:100 }}