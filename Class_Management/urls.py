from django.conf.urls import include, url
from . import views

app_name = 'Class_Management'
urlpatterns = [
    url(r'^$', views.Home, name='CLASSROOM'),
    url(r'^Assignment/', include('Assign_Management.urls')),
    url(r'^Home/', views.Home, name='Home'),
    url(r'^Submit/$', views.Submit, name='SubmitRoom')
]
