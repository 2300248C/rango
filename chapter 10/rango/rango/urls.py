"""rango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from rango1 import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'rango1'

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^rango/add_category/$', views.add_category, name='add_category'),
    url(r'^rango/category/(?P<category_name_slug>[\w\-]+)/$', views.show_category, name='show_category'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/add_page/$', views.add_page, name='add_page'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login, name='login'),
    url(r'^restricted/$', views.login, name='restricted'),
    url(r'^logout/$', views.user_logout, name='logout'),
]

static( settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
