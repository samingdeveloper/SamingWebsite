from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.CreateAssignment, name='CreateAssignment'),
    url(r'AssignmentDetail/$', views.AssignmentDetail, name='AssignmentDetail')
]