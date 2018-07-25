from django.conf.urls import include,url
from Class_Management.models import ClassRoom, Quiz
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'Assign_Management'
urlpatterns = [
    url(r'^$', views.CreateAssignment, name='CreateAssignment'),
    url(r'^(?P<quiz_id>[0-9]+)/', views.DeleteAssign, name='DeleteAssign'),
    url(r'^Upload/(?P<quiz_id>[0-9]+)/', views.uploadgrading, name='Uploadfile'),
    url(r'^EditAssign/(?P<quiz_id>[0-9]+)/', views.EditAssign, name='EditAssign'),
    url(r'^AssignmentDetail/', views.AssignmentDetail, name='AssignmentDetail'),
    url(r'^generate_assign/', views.GenerateAssign, name='GenerateAssign'),
    url(r'^MOSS/(?P<quiz_id>[0-9]+)/', views.moss, name='MOSS'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)