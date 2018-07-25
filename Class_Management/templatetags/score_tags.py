from django import template
from ..models import *
from django.core.exceptions import ObjectDoesNotExist
register = template.Library()

@register.simple_tag
def u_score(userId, classroom, quizId, mode):
    score = 0
    if mode == "Scoring":
        try:
            score = QuizScore.objects.get(userId=userId, classroom=classroom, quizId=quizId)
            print(score)
            return score.total_score
        except ObjectDoesNotExist:
            return ''
    elif mode == "Max":
        try:
            score = QuizScore.objects.get(userId=userId, classroom=classroom, quizId=quizId)
            print(score)
            return score.max_score
        except ObjectDoesNotExist:
            return ''
    elif mode == "Pass or Fail":
        try:
            score = QuizScore.objects.get(userId=userId, classroom=classroom, quizId=quizId)
            print(score)
            return score.passOrFail
        except ObjectDoesNotExist:
            return ''
    else:
        return score


