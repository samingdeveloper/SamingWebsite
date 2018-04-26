from django.conf.urls import include, url
from . import views

app_name = 'Class_Management'
urlpatterns = [
    url(r'^$', views.index, name='CLASSROOM'),
    url(r'^(?P<className>[0-9]+)/$', views.inside, name='Inside'),
    url(r'^Assignment/', include('Assign_Management.urls')),
    url(r'^Home/', views.Home, name='Home'),
    url(r'^About/', views.About, name='About'),
    url(r'^StudentInfo/$', views.StudentInfo, name='StudentInfo'),
    url(r'^StudentInfo/(?P<username>[\w.@+-]+)/$', views.StudentScoreInfo, name='StudentScoreInfo'),
    url(r'^StudentInfo/(?P<username>[\w.@+-]+)/(?P<quiz_id>[0-9]+)/$', views.StudentQuizListInfo, name='StudentQuizListInfo'),
    url(r'^StudentInfo/(?P<username>[\w.@+-]+)/(?P<quiz_id>[0-9]+)/(?P<title>[\w.@+-]+)/$', views.StudentQuizInfo, name='StudentQuizInfo'),
    url(r'^Submit/$', views.Submit, name='SubmitRoom'),
]