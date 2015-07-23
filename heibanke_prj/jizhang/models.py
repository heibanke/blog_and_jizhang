#coding=utf-8
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

# Create your models here.

class Category(models.Model):
    INCOME_CHOICES = (
        (True, _(u'收入')),
        (False, _(u'支出') ),
    )
    p_category = models.ForeignKey('self', null = True, blank = True, verbose_name=_(u"父类名称"), related_name='child')
    name = models.CharField(max_length=20, verbose_name=_(u"类别名称"))
    isIncome = models.BooleanField(choices=INCOME_CHOICES, verbose_name='是否收入')
    user = models.ForeignKey(User,verbose_name='所属用户')
    def __unicode__(self):
        return self.name
    def get_absolute_url(self):
        return '%s' % (reverse('jizhang:index_category_item', args=[self.id])) 


class Item(models.Model):
	price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='金额')
	comment = models.CharField(max_length=200, blank = True, verbose_name='注释')
	pub_date = models.DateField(verbose_name='日期')
	category = models.ForeignKey(Category,verbose_name='分类')	
	def __unicode__(self):
		return str(self.price)
