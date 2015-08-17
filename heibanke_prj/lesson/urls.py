#coding=utf-8
from django.conf.urls import patterns, include, url
from django.contrib import admin


from lesson import views

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^crawler_ex00/$', views.crawler_ex00, name='crawler_ex00'),    
    url(r'^crawler_ex00/(?P<pk>\d+)/$', views.crawler_ex00, name='crawler_ex00'),
    url(r'^crawler_ex01/$', views.crawler_ex01, name='crawler_ex01'),
    url(r'^crawler_ex02/$', views.crawler_ex02, name='crawler_ex02'),
    url(r'^crawler_ex03/$', views.crawler_ex03, name='crawler_ex03'),
    url(r'^crawler_ex03/pw_list/$', views.crawler_ex03_pw_list, name='crawler_ex03_pw_list'),
)