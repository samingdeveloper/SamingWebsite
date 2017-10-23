from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='CLASSROOM'),
    url(r'^(?P<className>[0-9]+)/$', views.inside, name='Inside'),
]