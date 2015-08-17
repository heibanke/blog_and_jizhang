#coding=utf-8
#django package
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render_to_response,render ,get_object_or_404

from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required

from django.views.decorators.csrf import csrf_exempt

from jizhang.views import split_page

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

PW_EX03_IP_MOD = 33
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
        return HttpResponseNotFound(u'<h1>页面找不到</h1>')
    else:
        ip_list = [int(i) for i in ip.split('.')]

    start_index = sum(ip_list)%50


    if not pk:
        return HttpResponseNotFound(u'<h1>你需要在网址后输入数字<strong>%d</strong></h1>'%candidate_list[start_index])

    else:    
        try:
            num = int(pk)
            if num not in candidate_list:
                return HttpResponseNotFound(u'<h1>%s输入不正确, 请输入正确数字</h1>'%pk)
            else:
                index_num = candidate_list.index(num)
                if index_num==start_index+49:
                    html = u"<html><body><h1>恭喜你,你找到了答案.输入网址/crawler_ex01继续你的爬虫之旅吧</h1></body></html>"
                else:
                    if index_num <2:
                        str_help = u''
                    elif index_num < 8:
                        str_help = u'还有一大波数字马上就要到来...'
                    else:
                        str_help = u'老实告诉你吧, 这样的数字还有上百个'
                    html = u"<html><body><h1>下一个你需要输入的数字是<strong>%d</strong>. %s</h1></body></html>" % (candidate_list[index_num+1],str_help)
                return HttpResponse(html)            
        except:

            return HttpResponseNotFound(u'<h1>%s输入不正确, 请输入正确数字</h1>'%pk)


# form post example
@csrf_exempt
def crawler_ex01(request):
    
    if request.method == 'POST':
        if request.META.has_key('HTTP_X_FORWARDED_FOR'):
            ip =  request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']

        if not ip:
            return HttpResponseNotFound(u'<h1>Page not found</h1>')
        else:
            ip_list = [int(i) for i in ip.split('.')]

        password_ip = sum(ip_list)%30 
               
        try:
            username = request.POST['username']
            password = request.POST['password']
            if int(password)==password_ip:
                html=u'<h1>恭喜! 用户'+username+u'成功闯关, 输入网址/crawler_ex02继续你的爬虫之旅吧</h1>'
            else:
                html=u'<h1>您输入的密码错误, 请重新输入</h1>'

        except:
            html=u'<h1>密码只有数字哦</h1>'
        finally:
            return HttpResponse(u'<!DOCTYPE html><html lang="zh-CN" >\
                   <meta name="viewport" content="width=device-width, initial-scale=1">\
                   <meta http-equiv="Content-Type" content="text/html; charset=utf-8" >\
                   <body>%s</body></html>'%(html))
    else:
        return render_to_response('lesson/crawler_ex01.html',RequestContext(request))
         

# login example
@login_required
def crawler_ex02(request):
    
    if request.method == 'POST':
        if request.META.has_key('HTTP_X_FORWARDED_FOR'):
            ip =  request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']

        if not ip:
            return HttpResponseNotFound(u'<h1>Page not found</h1>')
        else:
            ip_list = [int(i) for i in ip.split('.')]

        password_ip = sum(ip_list)%30 
               
        try:
            username = request.POST['username']
            password = request.POST['password']
            if int(password)==password_ip:
                html=u'<h1>恭喜! 用户'+username+u'成功闯关, 输入网址/crawler_ex03/继续你的爬虫之旅吧</h1>'
            else:
                html=u'<h1>您输入的密码错误, 请重新输入</h1>'

        except:
            html=u'<h1>密码只有数字哦</h1>'
        finally:
            return HttpResponse(u'<!DOCTYPE html><html lang="zh-CN" >\
                   <meta name="viewport" content="width=device-width, initial-scale=1">\
                   <meta http-equiv="Content-Type" content="text/html; charset=utf-8" >\
                   <body>%s</body></html>'%(html))
    else:
        return render_to_response('lesson/crawler_ex02.html',RequestContext(request))
        
        
@login_required
def crawler_ex03(request):
    
    if request.method == 'POST':
        if request.META.has_key('HTTP_X_FORWARDED_FOR'):
            ip =  request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']

        if not ip:
            return HttpResponseNotFound(u'<h1>Page not found</h1>')
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
                html=u'<h1>恭喜用户'+username+u'成功闯关, 后续关卡敬请期待</h1>'
            else:
                html=u'<h1>您输入的密码错误, 请重新输入</h1><p>偷偷告诉你, 密码可以从<a href="/lesson/crawler_03/pw_list/">下面这个网页里</a>获得</p>'

        except:
            html=u'<h1>您输入的密码格式错误</h1>'
        finally:
            return HttpResponse(u'<!DOCTYPE html><html lang="zh-CN" >\
                   <meta name="viewport" content="width=device-width, initial-scale=1">\
                   <meta http-equiv="Content-Type" content="text/html; charset=utf-8" >\
                   <body>%s</body></html>'%(html))
    else:
        return render_to_response('lesson/crawler_ex03.html',RequestContext(request))   


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