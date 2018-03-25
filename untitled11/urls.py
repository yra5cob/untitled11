"""untitled11 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from app import views
from django.conf.urls.static import static

from untitled11 import settings

urlpatterns = [
    path('admin/', admin.site.urls),url(r'^index', views.index, name='index'),url(r'^$', views.index, name='index'),url(r'^player', views.player, name='player'),url(r'^search', views.search, name='search'),url(r'^play_song', views.play_song, name='play_song'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)