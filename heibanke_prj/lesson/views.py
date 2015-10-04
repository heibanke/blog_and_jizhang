#coding=utf-8
#django package
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render_to_response,render ,get_object_or_404

from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required

from django.views.decorators.csrf import csrf_exempt

from jizhang.views import split_page
from lesson.forms import  Crawler04Form


import random
import time
#myApp package
candidate_list=[92631, 52516, 93147, 79255, 79303, 32653, 14901, 63668, 77456, 62881, 73618, 
        53825, 36752, 64972, 33818, 30867, 44513, 53577, 48950, 69524, 43295, 48946, 13647, 
        99039, 48743, 26048, 43713, 48776, 61813, 69634, 49163, 26470, 64899, 36702, 83105, 
        25338, 19016, 13579, 43396, 39642, 96911, 30965, 67917, 22213, 72586, 48151, 53639, 
        10963, 65392, 36133, 72324, 57633, 91251, 87016, 77055, 30366, 83679, 31388, 99446, 
        69428, 34798, 16780, 36499, 21070, 96749, 71822, 48739, 62816, 80182, 68171, 45458, 
        56056, 87450, 52695, 36675, 25997, 73222, 93891, 29052, 72996, 73999, 23814, 98084, 
        51103, 39603, 34316, 55719, 53685, 77771, 69187, 89677, 71935, 98538, 79152, 70999, 
        35102, 75956, 19122, 54168, 13871]

PW_EX04_IP_MOD = 23
PW_EX03_IP_MOD = 33
PW_EX02_IP_MOD = 29
PW_EX01_IP_MOD = 30
PW_EX03_LEN = 20        
        
class PW_Item(object):
    def __init__(self, pos, val):
        self.pos = pos
        self.val = val

# simple example for loop input url
def crawler_ex00(request,pk=None):
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        ip =  request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']

    if not ip:
        content = u'页面找不到'
        return render(request,'lesson/crawler_ex00.html',{'content':content})
    else:
        ip_list = [int(i) for i in ip.split('.')]

    start_index = sum(ip_list)%50

    next_link=""
    
    if not pk:
        content = u'你需要在网址后输入数字%d'%candidate_list[start_index]
        return render(request,'lesson/crawler_ex00.html',{'content':content})

    else:    
        try:
            num = int(pk)
            if num not in candidate_list:
                content = u'%s输入不正确, 请输入正确数字'%pk
            else:
                index_num = candidate_list.index(num)
                if index_num==start_index+49:
                    content = u"恭喜你,你找到了答案.继续你的爬虫之旅吧"
                    next_link = u"/lesson/crawler_ex01"
                else:
                    if (index_num-start_index) <3:
                        str_help = u''
                    elif (index_num-start_index) < 8:
                        str_help = u'还有一大波数字马上就要到来...'
                    else:
                        str_help = u'老实告诉你吧, 这样的数字还有上百个'
                    content = u"下一个你需要输入的数字是%d. %s" % (candidate_list[index_num+1],str_help)
            
            return render(request,'lesson/crawler_ex00.html',{'content':content,'next_link':next_link})
        except:
            
            content = u'%s输入不正确, 请输入正确数字'%pk
            return render(request,'lesson/crawler_ex00.html',{'content':content,'next_link':next_link})



# form post example
@csrf_exempt
def crawler_ex01(request):
    isget = True
    next_link=""
    if request.method == 'POST':
        isget = False
        
        if request.META.has_key('HTTP_X_FORWARDED_FOR'):
            ip =  request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']

        if not ip:
            return render(request,'lesson/crawler_ex01.html',{'content':u'Your Page not found'})
        else:
            ip_list = [int(i) for i in ip.split('.')]

        password_ip = sum(ip_list)%PW_EX01_IP_MOD 
        try:
            username = request.POST['username']
            password = request.POST['password']
            if int(password)==password_ip:
                content=u'恭喜! 用户'+username+u'成功闯关, 继续你的爬虫之旅吧'
                next_link = "lesson/crawler_ex02"
            else:
                content=u'您输入的密码错误, 请重新输入'

        except:
            content=u'密码只有数字哦'
        finally:
            return render(request,'lesson/crawler_ex01.html',{'content':content,'isget':isget,'next_link':next_link})
    else:
        return render(request,'lesson/crawler_ex01.html',{'isget':isget})
         

# login example
@login_required
def crawler_ex02(request):
    isget = True
    next_link=""
    if request.method == 'POST':
        isget = False
        if request.META.has_key('HTTP_X_FORWARDED_FOR'):
            ip =  request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']

        if not ip:
            return render(request,'lesson/crawler_ex02.html',{'content':u'Your Page not found'})
        else:
            ip_list = [int(i) for i in ip.split('.')]

        password_ip = sum(ip_list)%PW_EX02_IP_MOD 
               
        try:
            username = request.POST['username']
            password = request.POST['password']
            if int(password)==password_ip:
                content=u'恭喜! 用户'+username+u'成功闯关, 继续你的爬虫之旅吧'
                next_link = "lesson/crawler_ex03"
            else:
                content=u'您输入的密码错误, 请重新输入'

        except:
            content=u'密码只有数字哦'
        finally:
            return render(request,'lesson/crawler_ex02.html',{'content':content,'isget':isget,'next_link':next_link})

    else:
        content = u'比上一关多了两层保护'
        return render(request,'lesson/crawler_ex02.html',{'content':content,'isget':isget})
        
        
@login_required
def crawler_ex03(request):
    isget = True
    next_link=""
    if request.method == 'POST':
        isget = False

        if request.META.has_key('HTTP_X_FORWARDED_FOR'):
            ip =  request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']

        if not ip:
            return render(request,'lesson/crawler_ex03.html',{'content':u'Your Page not found'})
        else:
            ip_list = [int(i) for i in ip.split('.')]

        index_ip = sum(ip_list)%PW_EX03_IP_MOD 
        
        password_list = [str(p) for p in candidate_list[index_ip:(index_ip+PW_EX03_LEN)]]
        password_ip = ''.join(password_list)
        
        print password_ip
        time.sleep(5)
        try:
            username = request.POST['username']
            password = request.POST['password']
            if password==password_ip:
                content=u'恭喜! 用户'+username+u'成功闯关, 继续你的爬虫之旅吧'
                next_link = "lesson/crawler_ex04"
            else:
                content=u'您输入的密码错误, 请重新输入'
                next_link='lesson/pw_list'

        except:
            content=u'您输入的密码格式错误'
        finally:
            return render(request,'lesson/crawler_ex03.html',{'content':content,'isget':isget,'next_link':next_link})

    else:
        content = u'密码很长, 试是试不出来的, 需要找出来的哦'
        return render(request,'lesson/crawler_ex03.html',{'content':content,'isget':isget})   


@login_required
def crawler_ex03_pw_list(request):        

    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        ip =  request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']

    if not ip:
        return HttpResponseNotFound(u'<h1>Page not found</h1>')
    else:
        ip_list = [int(i) for i in ip.split('.')]

    index_ip = sum(ip_list)%PW_EX03_IP_MOD 
    
    password_val = []
    for p in candidate_list[index_ip:(index_ip+PW_EX03_LEN)]:
        password_val.extend(list(str(p)))
    
    password_list = []
    for i in xrange(len(password_val)):
        tmp=PW_Item(i+1,password_val[i])
        password_list.append(tmp)
        
    random.shuffle(password_list)
    item_page,page_num_list = split_page(request, password_list, 8)
    
    context = {'item_list': item_page,'username':request.user.username,'page_num_list':page_num_list}
    time.sleep(15)
    return render_to_response('lesson/pw_list.html', context,context_instance=RequestContext(request))    



# login example
@login_required
def crawler_ex04(request):
    isget = True
    next_link=""
    form = Crawler04Form() 
    if request.method == 'POST':

        isget = False
        if request.META.has_key('HTTP_X_FORWARDED_FOR'):
            ip =  request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']

        if not ip:
            return render(request,'lesson/crawler_ex04.html',{'content':u'Your Page not found'})
        else:
            ip_list = [int(i) for i in ip.split('.')]

        password_ip = sum(ip_list)%PW_EX04_IP_MOD 
       
        form=Crawler04Form(request.POST)
        if form.is_valid():

            try:
                username = request.POST['username']
                password = request.POST['password']
                if int(password)==password_ip:
                    content=u'恭喜! 用户'+username+u'成功闯关, 后续关卡敬请期待'
                    return render(request,'lesson/crawler_ex04.html',{'content':content,'isget':isget,'next_link':next_link})
                else:
                    content=u'您输入的密码错误, 请重新输入'

            except:
                content=u'密码只有数字哦'
        else:
            content=u"验证码输入错误"
        
        return render(request,'lesson/crawler_ex04.html',{'form':form, 'content':content,'isget':isget,'next_link':next_link})
    else:
        content = u'加了验证码'
        return render(request,'lesson/crawler_ex04.html',{'form':form,'content':content,'isget':isget})
        
