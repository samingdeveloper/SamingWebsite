from django.conf.urls import include,url
from . import views

app_name = 'Assign_Management'
urlpatterns = [
    url(r'^$', views.CreateAssignment, name='CreateAssignment'),
    url(r'AssignmentDetail/', views.AssignmentDetail, name='AssignmentDetail'),
    url(r'^generate_assign/$', views.GenerateAssign, name='GenerateAssign')
]