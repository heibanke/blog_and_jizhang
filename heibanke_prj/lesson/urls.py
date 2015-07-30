#coding=utf-8
from django.conf.urls import patterns, include, url
from django.contrib import admin


from lesson import views

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^scrapy_ex00/$', views.scrapy_ex00, name='scrapy_ex00'),    
    url(r'^scrapy_ex00/(?P<pk>\d+)/$', views.scrapy_ex00, name='scrapy_ex00'),
    url(r'^scrapy_ex01/$', views.scrapy_ex01, name='scrapy_ex01'),
    url(r'^scrapy_ex02/$', views.scrapy_ex02, name='scrapy_ex02'),

)
