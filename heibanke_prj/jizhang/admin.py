#coding=utf-8
from django.contrib import admin

# Register your models here.
from jizhang.models import Item, Category

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'p_category', 'isIncome', 'user')


class ItemAdmin(admin.ModelAdmin):
	list_display = ('category', 'price', 'pub_date', 'comment')
	list_filter = ['pub_date']
	date_hierarchy = 'pub_date'


admin.site.register(Category, CategoryAdmin)
admin.site.register(Item, ItemAdmin)