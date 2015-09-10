#coding=utf-8
from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User  
from django.contrib.auth import authenticate
from django.contrib.auth.models import check_password
from django.core.urlresolvers import reverse

from jizhang.forms import ItemForm, CategoryForm, NewCategoryForm
from jizhang.models import Item, Category


PASSWORD = "test123456"

def init_data(user):
    """this is init"""
    category1 = Category(p_category=None,name="cc",isIncome=True,user=user)
    category1.save()
    item1 = Item.objects.create(price=100.00,comment="",category=category1,pub_date="2015-05-24")
    return item1,category1

# Create your tests here.
class PageTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test", email="test@123.com", password=PASSWORD)
        self.item,self.category = init_data(self.user)
        self.client = Client()
        self.client.login(username=self.user.username, password=PASSWORD)
        
    def test_list_get(self):
        # test items
        response = self.client.get(reverse('jizhang:items'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['items']), 1)
        
        # test categories
        response = self.client.get(reverse('jizhang:categories'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['categories']), 1)

    def test_new_get(self):
        # test items     
        response = self.client.get(reverse('jizhang:new_item'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'])
        
        # test categories
        response = self.client.get(reverse('jizhang:new_category'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'])     

    def test_edit_get(self):
        # test items     
        response = self.client.get(reverse('jizhang:edit_item',args=(self.item.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'])
        
        # test categories
        response = self.client.get(reverse('jizhang:edit_category',args=(self.category.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'])          

    def test_show_get(self):
        # test items     
        response = self.client.get(reverse('jizhang:show_category',args=(self.category.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['items']) 

    def test_new_post(self):
        # test items     
        response = self.client.post(reverse('jizhang:new_item'),{'price':120,'category':self.category.id,'pub_date':"2015-09-06"})
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('jizhang:items'))
        self.assertEqual(len(response.context['items']), 2)
        
        # test categories
        response = self.client.post(reverse('jizhang:new_category'),{'name':'ce','p_category':"",'isIncome':True,'user':self.user})
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('jizhang:categories'))
        self.assertEqual(len(response.context['categories']), 2)    

    def test_edit_post(self):
        # test items     
        response = self.client.post(reverse('jizhang:edit_item',args=(self.item.id,)),{'price':120,'category':self.category,'pub_date':"2015-09-06"})
        #self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('jizhang:items'))
        self.assertEqual(len(response.context['items']), 1)
        
        # test categories
        response = self.client.post(reverse('jizhang:edit_category',args=(self.category.id,)),{'name':'ce','p_category':"",'isIncome':True,'user':self.user})
        #self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('jizhang:categories'))
        self.assertEqual(len(response.context['categories']), 1)     
        

