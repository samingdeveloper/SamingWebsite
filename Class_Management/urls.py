from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from . import views

app_name = 'Class_Management'
urlpatterns = [
    #url(r'^$', views.index, name='CLASSROOM'),
    #url(r'^(?P<className>[0-9]+)/$', views.inside, name='Inside'),
    url(r'^(?P<classroom>[\w\ .@+-]+)/Assignment/', include('Assign_Management.urls')),
    url(r'^$', views.ClassSelect, name='select_class'),
    url(r'^generate_classroom', views.GenerateClassroom, name='GenerateClassroom'),
    url(r'^edit_(?P<classroom>[\w\ .@+-]+)', views.EditClassroom, name='EditClassroom'),
    url(r'^delete_(?P<classroom>[\w\ .@+-]+)', views.DeleteClassroom, name='DeleteClassroom'),
    url(r'^(?P<classroom>[\w\ .@+-]+)/$', views.Home, name='Home'),
    #url(r'^(?P<classroom>[\w\ .@+-]+)/About/$', views.About, name='About'),
    url(r'^(?P<classroom>[\w\ .@+-]+)/Manual/$', views.Manual, name='Manual'),
    url(r'^(?P<classroom>[\w\ .@+-]+)/StudentInfo/$', views.StudentInfo, name='StudentInfo'),
    url(r'^(?P<classroom>[\w\ .@+-]+)/StudentInfo/(?P<userId>[\w.@+-]+)/$', views.StudentScoreInfo, name='StudentScoreInfo'),
    url(r'^(?P<classroom>[\w\ .@+-]+)/StudentInfo/(?P<userId>[\w.@+-]+)/(?P<quiz_id>[0-9]+)/$', views.StudentQuizListInfo, name='StudentQuizListInfo'),
    url(r'^(?P<classroom>[\w\ .@+-]+)/StudentInfo/(?P<userId>[\w.@+-]+)/(?P<quiz_id>[0-9]+)/(?P<file_id>[0-9]+)/$', views.StudentQuizInfo, name='StudentQuizInfo'),
    url(r'^Submit/$', views.Submit, name='SubmitRoom'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)