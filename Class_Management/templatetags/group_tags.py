from django import template
from ..models import *
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist
register = template.Library()

@register.filter(name='can_manage')
def can_manage(user, classname):
    try:
        if user.is_admin: return True
        elif Group.objects.get(name=classname+"_Teacher") in user.groups.all(): return True
        elif user is ClassRoom.objects.get(classname=classname).creator: return True
        else: return False
    except:
        return False

@register.simple_tag
def check_rank(user, classname, quiz):
    try:
        if can_manage(user, classname) or Rank.objects.get(userId=user, classroom__className=classname).rank >= Quiz.objects.get(pk=quiz).rank:
            return True
    except ObjectDoesNotExist:
        if can_manage(user, classname) or Rank(userId=user, classroom=ClassRoom.objects.get(classname=classname)).rank >= Quiz.objects.get(pk=quiz).rank:
            return True
    return False

'''@register.filter(name='has_group')
def has_group(user, group_name):
    try:
        group =  Group.objects.get(name=group_name)
        return group in user.groups.all()
    except:
        return None

@register.filter(name='can_do')
def can_do(user, classname):
    try:
        if can_manage(user, classname) or Rank.objects.get(userId=user, classroom__className=classname).rank >= Quiz.objects.get(pk=quiz).rank:
            return True
    except ObjectDoesNotExist:
        if can_manage(user, classname) or Rank(userId=user, classroom=ClassRoom.objects.get(classname=classname)).rank >= Quiz.objects.get(pk=quiz).rank:
            return True
    return False'''

#request.user|has_group:request.session.classroom