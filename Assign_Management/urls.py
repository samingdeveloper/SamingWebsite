from django.conf.urls import include,url
from Class_Management.models import ClassRoom, Quiz
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'Assign_Management'
urlpatterns = [
    url(r'^$', views.CreateAssignment, name='CreateAssignment'),
    url(r'^delete/(?P<quiz_id>[0-9]+)/', views.DeleteAssign, name='DeleteAssign'),
    url(r'^deleteExam/(?P<exam_data_id>[0-9]+)/', views.DeleteExam, name='DeleteExam'),
    url(r'^deleteExamQuiz/(?P<exam_quiz_id>[0-9]+)/', views.DeleteExamQuiz, name='DeleteExamQuiz'),
    url(r'^Upload/(?P<quiz_id>[0-9]+)/', views.uploadgrading, name='Uploadfile'),
    url(r'^UploadExam/(?P<exam_data_id>[0-9]+)/$', views.exam_quiz, name='ExamQuiz'),
    url(r'^UploadExam/(?P<exam_data_id>[0-9]+)/(?P<exam_quiz_id>[0-9]+)/', views.exam_grader, name='UploadfileExam'),
    url(r'^EditAssign/(?P<quiz_id>[0-9]+)/', views.EditAssign, name='EditAssign'),
    url(r'^AssignmentDetail/', views.AssignmentDetail, name='AssignmentDetail'),
    url(r'^generate_assign/', views.GenerateAssign, name='GenerateAssign'),
    url(r'^generate_exam/', views.GenerateExam, name='GenerateExam'),
    url(r'^generate_exam_quiz/', views.GenerateExamQuiz, name='GenerateExamQuiz'),
    url(r'^edit_exam/(?P<exam_data_id>[0-9]+)/', views.EditExam, name='EditExam'),
    url(r'^edit_exam_quiz/(?P<exam_quiz_id>[0-9]+)/', views.EditExamQuiz, name='EditExamQuiz'),
    url(r'^MOSS/(?P<quiz_id>[0-9]+)/(?P<mode>[0-9]+)/$', views.moss, name='MOSS'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)