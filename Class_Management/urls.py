from django.conf.urls import include, url
from . import views

app_name = 'Class_Management'
urlpatterns = [
    url(r'^$', views.index, name='CLASSROOM'),
    url(r'^(?P<className>[0-9]+)/$', views.inside, name='Inside'),
    url(r'^Assignment/', include('Assign_Management.urls')),
    url(r'^Home/', views.Home, name='Home'),
    url(r'^Submit/$', views.Submit, name='SubmitRoom')
]