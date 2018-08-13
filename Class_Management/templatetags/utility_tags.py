from django import template
from ..models import *
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist
register = template.Library()

@register.filter(name='zip')
def zip_list(a, b):
  return zip(a, b)