from django.conf.urls import include,url
from Class_Management.models import ClassRoom, Quiz
from . import views

app_name = 'Assign_Management'
urlpatterns = [
    url(r'^$', views.CreateAssignment, name='CreateAssignment'),
    url(r'^(?P<quiz_id>[0-9]+)/', views.DeleteAssign, name='DeleteAssign'),
    url(r'^Upload/$', views.upload, name='Upload'),
    url(r'AssignmentDetail/', views.AssignmentDetail, name='AssignmentDetail'),
    url(r'^generate_assign/$', views.GenerateAssign, name='GenerateAssign')
]