"""iframe URL Configuration

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
from django.conf.urls import url, include
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^$', views.ThreadListCreateView.as_view(), name='list'),
    url(r'^(?P<slug>[-\w]+)/threads/$', views.ThreadListCreateView.as_view(), name='detail-list'),
    url(r'^thread/(?P<slug>[-\w]+)/$', views.ThreadDetailView.as_view(), name='detail'),
    url(r'^api/post/(?P<id>[-\w]+)/like/$', views.PostLikeAPIToggle.as_view(), name='like-api'),
    url(r'^api/post/(?P<pk>[-\w]+)/update/$', views.UpdatePost.as_view(), name='update-api'),
    url(r'^api/post/(?P<pk>[-\w]+)/delete/$', views.DeletePost.as_view(), name='delete-api'),

]
