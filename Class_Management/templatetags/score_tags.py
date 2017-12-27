from django import template
from ..models import *
from django.core.exceptions import ObjectDoesNotExist
register = template.Library()

@register.simple_tag
def u_score(studentId, classroom, quizId, mode):
    score = ''
    if mode == "Scoring":
        try:
            score = QuizScore.objects.get(studentId=studentId, classroom=classroom, quizId=quizId)
            return score.total_score
        except ObjectDoesNotExist:
            return ''
    elif mode == "Pass or Fail":
        try:
            score = QuizScore.objects.get(studentId=studentId, classroom=classroom, quizId=quizId)
            return score.passOrFail
        except ObjectDoesNotExist:
            return ''
    else:
        return score