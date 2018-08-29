from django import template
from ..models import *
from django.core.exceptions import ObjectDoesNotExist
register = template.Library()

@register.simple_tag
def u_score(userId, classroom, quizId, mode):
    score = 0
    if mode == "Scoring":
        try:
            score = QuizScore.objects.get(userId__userId=userId, classroom__className=classroom, quizId__pk=quizId).total_score
            max_score = Quiz.objects.get(pk=quizId).max_score
            #print(score)
            if score > max_score:
                score = max_score
            return score
        except ObjectDoesNotExist:
            return ''
    elif mode == "Max":
        try:
            max_score = Quiz.objects.get(pk=quizId).max_score
            return max_score
        except ObjectDoesNotExist:
            return ''
    elif mode == "Pass or Fail":
        try:
            score = QuizScore.objects.get(userId__userId=userId, classroom__className=classroom, quizId__pk=quizId).passOrFail
            max_score = Quiz.objects.get(pk=quizId).max_score
            if score > max_score:
                score = max_score
            return score
        except ObjectDoesNotExist:
            return ''
    elif mode == "total":
        try:
            quiz_score = QuizScore.objects.filter(userId__userId=userId, classroom__className=classroom)
            quiz_data_score = Quiz.objects.filter(classroom__className=classroom)
            score_res = 0
            for i in quiz_score:
                score_res += i.total_score + i.passOrFail
            if score_res > sum([value.max_score for value in quiz_data_score]):
                score_res = sum([value.max_score for value in quiz_data_score])
            return score_res
        except ObjectDoesNotExist:
            return ''
    elif mode == "total_max":
        try:
            quiz_data_score = Quiz.objects.filter(classroom__className=classroom)
            score_res = 0
            for i in quiz_data_score:
                score_res += i.max_score
            return score_res
        except ObjectDoesNotExist:
            return ''
    else:
        return score
