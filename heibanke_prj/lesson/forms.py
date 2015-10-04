#coding=utf-8
from django import forms
from django.utils.translation import ugettext_lazy as _
from captcha.fields import CaptchaField

# Register your models here.

class Crawler04Form(forms.Form):
    username=forms.CharField(label=_(u"昵称(可选)"),max_length=40,widget=forms.TextInput(attrs={'size': 40,'class':"form-control"}))
    password=forms.CharField(label=_(u"密码(必填)"),max_length=20,widget=forms.PasswordInput(attrs={'size': 20,'class':"form-control"}))
    captcha = CaptchaField(label=_(u"验证码(必填)"))


	