#coding=utf-8
#django package
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render_to_response,render ,get_object_or_404

from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required

import csv, json

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


# simple example for loop input url
def scrapy_ex00(request,pk=None):
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
        return HttpResponseNotFound(u'<h1>你需要在网址后输入数字%d</h1>'%candidate_list[start_index])

    else:    
        try:
            num = int(pk)
            if num not in candidate_list:
                return HttpResponseNotFound(u'<h1>%s输入不正确, 请输入正确数字</h1>'%pk)
            else:
                index_num = candidate_list.index(num)
                if index_num==start_index+49:
                    html = u"<html><body><h1>恭喜你,你找到了答案.输入网址/scrapy_ex01继续你的爬虫之旅吧</h1></body></html>"
                else:
                    if index_num <2:
                        str_help = u''
                    elif index_num < 8:
                        str_help = u'还有一大波数字马上就要到来...'
                    else:
                        str_help = u'老实告诉你吧, 这样的数字还有上百个'
                    html = u"<html><body><h1>下一个你需要输入的数字是%d. %s</h1></body></html>" % (candidate_list[index_num+1],str_help)
                return HttpResponse(html)            
        except:

            return HttpResponseNotFound(u'<h1>%s输入不正确, 请输入正确数字</h1>'%pk)


# form post example
def scrapy_ex01(request):
    
    if request.method == 'POST':
        try:
            username = request.POST['username']
            email = request.POST['email']
            html=u'<html><body>用户名'+username+u'注册的邮箱是'+email+u'</body></html>'
        except:
            html=u'<h1>页面找不到</h1>'
        finally:
            return HttpResponse(html)
    else:
        return render_to_response('lesson/scrapy_ex01.html',RequestContext(request))
         

# login example
@login_required
def scrapy_ex02(request):
    if request.method == 'POST':
        try:
            username = request.POST['username']
            email = request.POST['email']
            html=u'<html><body>用户名'+username+u'注册的邮箱是'+email+u'</body></html>'
        except:
            html=u'<h1>页面找不到</h1>'
        finally:
            return HttpResponse(html)
    else:
        return render_to_response('lesson/scrapy_ex01.html',RequestContext(request))
                  
