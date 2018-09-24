"""Theorem URL Configuration

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
from django.contrib import admin
# from django.urls import path, re_path
from django.conf.urls import url
from app import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('login/', views.login),
    # path('register/', views.register),
    # path('check_code.html/', views.check_code),
    # path('views/', views.views),
    # path('add_theorem/', views.add),
    # path('add_relation/', views.add_r),
    # path('logout/', views.logout),
    # path('nickname/', views.nickname),
    # path('description/', views.description),
    # path('my/', views.my),
    # re_path('views/.*/', views.detail),
    # path('users/', views.users),
    # re_path('users/.*/', views.detail),
    url('admin/', admin.site.urls),
    url('login/', views.login),
    url('register/', views.register),
    url('getpass/', views.resetPassword),
    url('check_code.html/', views.check_code),
    url('views/$', views.views),
    url('add_theorem/', views.add),
    url('my/', views.editTheorem),
    url('add_relation/', views.add_r),
    url('add_relation_operator/', views.add_r_operator),
    url('logout/', views.logout),
    url('nickname/', views.nickname),
    url('description/', views.description),
    # url('my/', views.my),
    url('views/.*/', views.detail),
    url('users/', views.users),
    url('users/.*/', views.detail),
    url(r'^active/(?P<active_code>.*)/$', views.ActiveUserView.as_view(), name="user_active"),
    url(r'^add_comment/$', views.AddCommentView.as_view(), name='add_comment'),  # draw_image
    url(r'^draw_image/$', views.draw_image),
    url(r'^relation/$', views.relation),
    # url(r'^', views.notfound)
]
