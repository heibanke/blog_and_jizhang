#coding=utf-8
from django.conf.urls import patterns, include, url
from django.contrib import admin


from jizhang import views

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', views.items),
    url(r'^items/(p?)$', views.items, name='items'),
    url(r'^first_login/', views.first_login, name='first_login'),
    url(r'^categorys/', views.categorys, name='categorys'),
    url(r'^item/(?P<pk>\d+)/$', views.item, name='item'),
    url(r'^category/(?P<pk>\d+)/items/$', views.index_category_item, name='index_category_item'),    
    url(r'^category/(?P<pk>\d+)/$', views.category, name='category'),
    url(r'^new_item/',views.new_item,name='new_item'),
    url(r'^new_category/',views.new_category,name='new_category'),
    url(r'^find_item/',views.find_item,name='find_item'),
    url(r'^report_item/',views.report_item,name='report_item'),
    url(r'^export/items/',views.export_to_item_csv,name='export_to_item_csv'),
    url(r'^export/categorys/',views.export_to_category_csv,name='export_to_category_csv'),
    url(r'^import/items/',views.import_item_csv,name='import_item_csv'),
    url(r'^import/categorys/',views.import_category_csv,name='import_category_csv'),    
    url(r'^autocomplete_comments/',views.autocomplete_comments),    
)
