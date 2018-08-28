from django import template
from ..models import *
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist
register = template.Library()

@register.simple_tag
def your_exam(user, classname, picked_list):
    return Exam_Quiz.objects.filter(classroom__className=classname,title__in=picked_list)

@register.simple_tag
def u_exam_score(userId, classroom, exam_data_id=None, mode=None):
    score = 0
    if mode == "Max":
        try:
            return Exam_Data.objects.get(pk=exam_data_id).max_score
        except ObjectDoesNotExist:
            return ''

    elif mode == "total":
        try:
            exam_score = Exam_Score.objects.filter(user__userId=userId, quiz__classroom__className=classroom)
            exam_data_score = Exam_Data.objects.filter(classroom__className=classroom)
            score_res = 0
            for i in exam_score:
                score_res += i.total_score + i.passOrFail
            if score_res > sum([value.max_score for value in Exam_Data.objects.filter(classroom__className=classroom)]):
                score_res = sum([value.max_score for value in Exam_Data.objects.filter(classroom__className=classroom)])
            return score_res
        except ObjectDoesNotExist:
            return ''

    elif mode == "total_max":
        try:
            exam_data_score = Exam_Data.objects.filter(classroom__className=classroom)
            score_res = 0
            for i in exam_data_score:
                score_res += i.max_score
            return score_res
        except ObjectDoesNotExist:
            return ''

    else:
        try:
            exam_quizes = Exam_Tracker.objects.get(exam__pk=exam_data_id,user__userId=userId).picked
            exam_score = Exam_Score.objects.filter(quiz__title__in=exam_quizes,user__userId=userId)
            for i in exam_score:
                if i.quiz.mode == "Pass or Fail":
                    score += i.passOrFail
                else:
                    score += i.total_score
            if score > Exam_Data.objects.get(pk=exam_data_id).max_score:
                score = Exam_Data.objects.get(pk=exam_data_id).max_score
            return score
        except ObjectDoesNotExist:
            return ''

@register.simple_tag
def u_exam_quiz_score(userId, classroom, exam_quiz_id=None, mode=None):
    if mode == "Max":
        try:
            #print(userId)
            return Exam_Score.objects.get(quiz__pk=exam_quiz_id,user__userId=userId).max_score
        except ObjectDoesNotExist:
            return ''

    else:
        try:
            exam_score = Exam_Score.objects.get(quiz__pk=exam_quiz_id,user__userId=userId)
            if exam_score.quiz.mode == "Pass or Fail":
                return exam_score.passOrFail
            else:
                return exam_score.total_score
        except ObjectDoesNotExist:
            return ''
