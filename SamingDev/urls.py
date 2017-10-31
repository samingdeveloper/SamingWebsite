"""SamingDev URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from LogIn_Management import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^LogIn_Page/$', views.LogIn_Page),
    url(r'^LogIn_Auth/$', views.LogIn_Auth),
    url(r'^ClassRoom/', include('Class_Management.urls')),
    url(r'^Change_Password/$', views.Change_Password),
    url(r'^ClassRoom/Assignment/', include('Assign_Management.urls')),


    #logout default function
    url(r'^LogOut/$', auth_views.logout, {'next_page': '/'}, name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
