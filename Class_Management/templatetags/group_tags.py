from django import template
from ..models import *
from django.contrib.auth.models import Group

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

'''@register.filter(name='has_group')
def has_group(user, group_name):
    try:
        group =  Group.objects.get(name=group_name)
        return group in user.groups.all()
    except:
        return None'''

#request.user|has_group:request.session.classroom