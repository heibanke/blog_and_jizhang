#coding=utf-8
#django package
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.models import User  
from django.contrib import messages
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login ,logout as auth_logout

#myApp package
from accounts.forms import  RegisterForm, LoginForm


def register(request):
    '''注册视图'''
    template_var={}
    form = RegisterForm()    
    if request.method=="POST":
        form=RegisterForm(request.POST.copy())
        if form.is_valid():
            username=form.cleaned_data["username"]
            email=form.cleaned_data["email"]
            password=form.cleaned_data["password"]
            user=User.objects.create_user(username,email,password)
            user.save()
            _login(request,username,password)#注册完毕 直接登陆
            return HttpResponseRedirect("/jizhang/first_login")    
    template_var["form"]=form        
    return render_to_response("accounts/register.html",template_var,context_instance=RequestContext(request))

	
def login(request):
    '''登陆视图'''
    template_var={}
    form = LoginForm()    
    if request.method == 'POST':
        form=LoginForm(request.POST.copy())
        if form.is_valid():
            _login(request,form.cleaned_data["username"],form.cleaned_data["password"])
            
            try:
                tmp = request.GET['next']
                return HttpResponseRedirect(tmp)
            except:
                return HttpResponseRedirect("/jizhang")
                
    template_var["form"]=form        
    return render_to_response("accounts/login.html",template_var,context_instance=RequestContext(request))
    
	
def _login(request,username,password):
    '''登陆核心方法'''
    ret=False
    user=authenticate(username=username,password=password)
    if user is not None:
        if user.is_active:
            auth_login(request,user)
            ret=True
        else:
            messages.add_message(request, messages.INFO, (u'用户没有激活'))
    else:
        messages.add_message(request, messages.INFO, (u'用户不存在'))
    return ret	
	
	
	
	
def logout(request):
	auth_logout(request)
	return render_to_response('accounts/logout.html',RequestContext(request,{'hello2you':'Thanks for your visit!'}))	
	
