#coding=utf-8
#django package
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response,render ,get_object_or_404
from django.contrib.auth.models import User  
from django.contrib import messages
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
import datetime
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import csv, json
from django.db.models import Sum, Count, Q
from django.db import connection

#myApp package
from jizhang.models import Item, Category
from jizhang.forms import ItemForm, CategoryForm, NewCategoryForm, FindItemForm, UpLoadFileForm, ReportForm
from jizhang.data_format_func import sort_category, check_parent_category

P_CATEGORY_NULL_NAME = '------'
PAGE_ITEM_NUM = 15
    
def split_page(request, data, page_item_num):
    side_show_page_num = 4
    
    p = Paginator(data , page_item_num)
    page = request.GET.get('page') # Get page
    try:
        item_page = p.page(page)
    except PageNotAnInteger:
        item_page = p.page(1)
    except EmptyPage:
        item_page = p.page(p.num_pages)     
    
    page_list = [-1]*len(p.page_range)
    
    for i in p.page_range:
        if i==1 or i==p.num_pages or (i<=item_page.number+side_show_page_num and i>=item_page.number-side_show_page_num):
            page_list[i-1]=i
        elif i==item_page.number+side_show_page_num+1 or i==item_page.number-side_show_page_num-1:
            page_list[i-1]=0
    
    return item_page, page_list  
    
# item list view
@login_required
def items(request, price_order=False):

    if request.method == 'POST':
        del_id = request.POST.getlist('del_id')
        for item_id in del_id:
            del_item = get_object_or_404(Item, id=item_id)
            del_item.delete()

    if not price_order:
        item_list = Item.objects.filter(category__user__username=request.user.username).order_by('-pub_date')
    else:
        item_list = Item.objects.filter(category__user__username=request.user.username).order_by('price')
    item_page,page_num_list = split_page(request, item_list, PAGE_ITEM_NUM)

    context = {'item_list': item_page,'username':request.user.username,'page_num_list':page_num_list}
    return render_to_response('jizhang/items.html', context,context_instance=RequestContext(request))

	
@login_required
def index_category_item(request,pk):

    if request.method == 'POST':
        del_id = request.POST.getlist('del_id')
        for item_id in del_id:
            del_item = get_object_or_404(Item, id=item_id)
            del_item.delete()
   
    item_list = Item.objects.filter(category__user__username=request.user.username).filter(category__id=pk).order_by('price')
    item_page,page_num_list = split_page(request, item_list, PAGE_ITEM_NUM)

    context = {'item_list': item_page,'username':request.user.username,'page_num_list':page_num_list}
    return render_to_response('jizhang/items.html', context,context_instance=RequestContext(request))
    

def get_category(category_list, new_list, level):
    for category in category_list:
        new_list.append({'category':category,'level':'----'*level})
        level=level+1
        new_list,level = get_category(category.child.all(),new_list,level)
        level=level-1
    return new_list,level
    
# category list view
@login_required
def categorys(request):

    if request.method == 'POST':
        del_id = request.POST.getlist('del_id')
        for category_id in del_id:
            del_category = Category.objects.filter(id=int(category_id))
            if del_category:
                del_category.delete()

    category_list = Category.objects.filter(user__username=request.user.username).filter(p_category__isnull=True)
    new_list = []
    new_list,level=get_category(category_list,new_list,0)
    context = {'category_list': new_list,'username':request.user.username}
    return render_to_response('jizhang/categorys.html', RequestContext(request,context))	

# first login auto generate category
@login_required
def first_login(request):
        
    category_list = Category.objects.filter(user__username=request.user.username).order_by('p_category')
    
    if not category_list:
        first_login_category(request.user.id)
        category_list = Category.objects.filter(user__username=request.user.username).order_by('p_category')
    
    return HttpResponseRedirect("/jizhang/categorys")	

# new item view	
@login_required	
def new_item(request):
    last_save_item=""    
    if request.method == 'POST':
        return_list=request.POST.get('return_list')
        add_another=request.POST.get('add_another')
        form = ItemForm(request,data=request.POST)
        if form.is_valid():
            new_item = form.save()
            new_item.save()
            if not return_list:
                #继续新建
                form = ItemForm(request,initial={'pub_date':timezone.now().date()})
                if new_item.category.isIncome:
                    isIncome=u"收入"
                else:
                    isIncome=u"支出"
                last_save_item=u'您刚提交的"'+new_item.category.name+u'"分类下"'+str(new_item.price)+u'"元"'+isIncome+u"已保存"
            else:
                #返回列表
                return HttpResponseRedirect("/jizhang")
    else:
        form = ItemForm(request,initial={'pub_date':timezone.now().date()})

    most_used_categorys = Category.objects.filter(user__username=request.user.username).annotate(num_items=Count('item')).filter(num_items__gt=0).order_by('-num_items')[:8]
    context = {'last_save_item':last_save_item,'form':form,'username':request.user.username,'most_used_categorys':most_used_categorys}
    return render_to_response('jizhang/new_item.html',RequestContext(request,context))

	
# new category view		
@login_required	
def new_category(request):
    if request.method == 'POST':
        form = NewCategoryForm(request,data=request.POST)
        if form.is_valid():
            new_category = form.save(request)
            new_category.save()
            return HttpResponseRedirect("/jizhang/categorys")
    else:
        form = NewCategoryForm(request)
    context = {'form':form,'username':request.user.username}
    return render_to_response('jizhang/new_category.html',RequestContext(request,context))

	
@login_required	
def item(request,pk):
    if request.method == 'POST':

        form = ItemForm(request,data=request.POST)
        if form.is_valid():
            new_item = form.save()
            new_item.id=pk
            new_item.save()
            return HttpResponseRedirect("/jizhang")
    else:
        item_list = get_object_or_404(Item, id=pk)
        form = ItemForm(request,instance=item_list)

    most_used_categorys = Category.objects.filter(user__username=request.user.username).annotate(num_items=Count('item')).filter(num_items__gt=0).order_by('-num_items')[:6]
    context = {'form':form,'username':request.user.username,'most_used_categorys':most_used_categorys}
    return render_to_response('jizhang/new_item.html',RequestContext(request,context))

	
@login_required	
def category(request,pk):
    out_errors = []
    if request.method == 'POST':
        form = CategoryForm(request,data=request.POST)
        if form.is_valid():
            if not form.cleaned_data['p_category']:
                pid=0
            else:
                pid = form.cleaned_data['p_category'].id
            
            if check_parent_category(int(pk),pid,form.fields['p_category'].choices):
                new_category = form.save(request)
                new_category.id=int(pk)
                new_category.save()
                return HttpResponseRedirect("/jizhang/categorys")
            else:
                out_errors = "父类别不能和子类别重复!"
    else:
        category_list = get_object_or_404(Category, id=pk) 
        form = CategoryForm(request,instance=category_list)
    context = {'form':form,'username':request.user.username,'out_errors':out_errors}
    return render_to_response('jizhang/new_category.html',RequestContext(request,context))


def config_qset(query):
    qset = (
            Q(comment__icontains=query)
        )
    return qset

def config_category_qset(id):
    qset = ()
    ff = get_object_or_404(Category, id=id)
    for child in ff.child.all():
        if not qset:
            qset = config_category_qset(child.id)
        else:
            qset = qset | config_category_qset(child.id)

    if not qset:
        qset = (Q(category__id=ff.id))
    else:
        qset = qset | (Q(category__id=ff.id))

    return qset

@login_required 
def find_item(request):
    if request.method == 'POST':
        del_id = request.POST.getlist('del_id')
        
        if del_id:
            for item_id in del_id:
                del_item = get_object_or_404(Item, id=item_id)
                del_item.delete()
            return HttpResponseRedirect("/jizhang")
                
        else:    

            form = FindItemForm(request,data=request.POST)
            if form.is_valid():
                if not form.cleaned_data['start_date']:
                    item_list = Item.objects.filter(category__user__username=request.user.username).all()
                else:
                    item_list = Item.objects.filter(category__user__username=request.user.username).filter(pub_date__range=(form.cleaned_data['start_date'],form.cleaned_data['end_date']))

                category_id = form.cleaned_data['category']
                if not category_id:
                    item_category = item_list
                else:
                    category_qset=config_category_qset(category_id)
                    item_category = item_list.filter(category_qset).distinct()

                query = form.cleaned_data['query']
                if not query:   
                    results = item_category.order_by('-pub_date')
                else:                
                    query_list = query.strip().split(' ')
                    qset =()
                    for every_query in query_list:
                        if not qset:
                            qset = config_qset(every_query)
                        else:
                            qset = qset|config_qset(every_query)

                    results = item_category.filter(qset).distinct().order_by('-pub_date')


                p = Paginator(results , PAGE_ITEM_NUM)
                item_pages = []
                for i in p.page_range:
                    item_pages.append(p.page(i))

                return render_to_response('jizhang/find_item_result.html', RequestContext(request,{'username':request.user.username,'item_pages': item_pages}))
    else:
        form = FindItemForm(request,initial={'start_date':None,'end_date':timezone.now().date()})
    context = {'form':form,'username':request.user.username}
    return render_to_response('jizhang/find_item.html',RequestContext(request,context))


def table_report_data_format(report_data, isIncome, total=False):
    exist_categorys=[]
    table_data = []
    i=0
    j=0
    #1. find the exist categorys, sort with isIncome
    for datas in report_data:
        if datas:
            for data in datas:
                if data.name in exist_categorys or (total==False and data.isIncome<>isIncome):
                    pass
                else:
                    exist_categorys.append(data.name)
                    
    #3. generate the table data
    for datas in report_data:
        #generate the null data
        null_data = [0]*len(exist_categorys)
        sum_category = 0
        if datas:
            for data in datas:
                if (total==True or data.isIncome==isIncome):
                    null_data[exist_categorys.index(data.name)] = int(data.item__price__sum)
                    sum_category = sum_category+int(data.item__price__sum)
        null_data.append(sum_category)
        table_data.append(null_data)
    #4. format
    format_data=[]
    exist_categorys.append(u'总和')
    for category in exist_categorys:
        data = []
        sum_data = 0
        for i in range(0,len(table_data)):
            data.append(table_data[i][j])
            sum_data=sum_data+table_data[i][j]
        data.append(sum_data)
        format_data.append({'name':category,'data':data})
        j=j+1
    return format_data


@login_required
def report_item(request):
    table_data_shouru={}
    table_data_zhichu={}
    report_month = []
    
    if request.method == 'POST':
        form = ReportForm(data=request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            if form.cleaned_data['report_range']=='0':
                date_step = datetime.timedelta(days=30) 
                data_len = 6
            else:
                date_step = datetime.timedelta(days=365)
                data_len = 3
            
            #first filter username
            report_query_user = Category.objects.filter(user__username=request.user.username)

            #second filter start and end date
            #third annotate sum
            report_query_date = []
            
            for i in range(0,data_len):
                report_month.append(start_date.strftime("%Y-%m"))
                end_date = start_date+date_step
                report_query_date.append(report_query_user.filter(item__pub_date__range=(start_date,end_date)).annotate(Sum('item__price')))
                start_date = end_date+datetime.timedelta(days=1) 
                
            
            #fouth data process to show
            if form.cleaned_data['report_type']=='1':
                table_data_shouru = table_report_data_format(report_query_date, True, False)
                table_data_zhichu = table_report_data_format(report_query_date, False, False)
            else:
                table_data_shouru = table_report_data_format(report_query_date, True, True)

            
    else:
        tmp_date = timezone.now()-datetime.timedelta(days=30*6)
        form = ReportForm(initial={'start_date':tmp_date.date()})
    
    context = {'form':form,'username':request.user.username,'report_month':report_month,
        'table_data_shouru':table_data_shouru,'table_data_zhichu':table_data_zhichu}
    return render_to_response('jizhang/report_item.html',RequestContext(request,context))       
    
    
    
def gb_encode(val):
    return (val.encode('gb2312'))
def gb_decode(val):
    return (val.decode('gb2312').encode('utf-8'))
    
import zipfile

@login_required
def export_to_item_csv(request):

    #response = HttpResponse(content_type='text/csv')
    #filename = 'export_item_'+datetime.datetime.now().strftime("%Y-%m-%d")+'.csv'
    #response['Content-Disposition'] = 'attachment; filename="'+filename+'"'
    #writer = csv.writer(response)

    filename = "export_item_%s_%s.csv"%(request.user.username,datetime.datetime.now().strftime("%Y-%m-%d"))
    with open(filename, 'wb') as csvfile:
        writer = csv.writer(csvfile,dialect='excel')

        writer.writerow((gb_encode(u'日期'),gb_encode(u'价格'),gb_encode(u'分类'),gb_encode(u'备注')))
        items = Item.objects.filter(category__user__username=request.user.username).order_by('pub_date')
        if not items:
            pass
        else:
            for item in items:
                writer.writerow((item.pub_date.strftime("%m/%d/%Y"), item.price, gb_encode(item.category.name), gb_encode(item.comment)))

    zip_name = 'export_item_'+str(request.user.username)+'.zip'
    f = zipfile.ZipFile(zip_name, 'w' ,zipfile.ZIP_DEFLATED) 
    f.write(filename) 
    f.close()

    wrapper = FileWrapper(file(zip_name))
    response = HttpResponse(wrapper, content_type='application/zip')  
    response['Content-Disposition'] = 'attachment; filename='+zip_name  

    return response

    
@login_required
def export_to_category_csv(request):

    response = HttpResponse(content_type='text/csv')
    filename = 'export_category_'+datetime.datetime.now().strftime("%Y-%m-%d")+'.csv'

    response['Content-Disposition'] = 'attachment; filename="'+filename+'"'
    writer = csv.writer(response)


    writer.writerow((gb_encode(u'父类名称'),gb_encode(u'类别名称'),gb_encode(u'是否收入')))
    """
    categorys = Category.objects.filter(user__username=request.user.username).order_by('p_category')
    if not categorys:
        pass
    else:
        for category in categorys:
            if not category.p_category:
                writer.writerow((P_CATEGORY_NULL_NAME, gb_encode(category.name), category.isIncome))
            else:
                writer.writerow((gb_encode(category.p_category.name), gb_encode(category.name), category.isIncome))
    """

    category_list = Category.objects.filter(user__username=request.user.username).filter(p_category__isnull=True)
    new_list = []
    new_list,level=get_category(category_list,new_list,0)

    if not new_list:
        pass
    else:
        for obj in new_list:
            category = obj['category']
            if not category.p_category:
                writer.writerow((P_CATEGORY_NULL_NAME, gb_encode(category.name), category.isIncome))
            else:
                writer.writerow((gb_encode(category.p_category.name), gb_encode(category.name), category.isIncome))
 

    return response
    
    
def handle_uploaded_file_item(f, request):
    destination = open('upload/csv/name.csv','wb')
    for chunk in f.chunks(): 
        destination.write(chunk)
    destination.close()
    
    csv_file = open('upload/csv/name.csv','rU')
    reader = csv.reader(csv_file, dialect='excel')
    i=0
    for line in reader:
        if i>0:
            category = Category.objects.filter(user__username=request.user.username).filter(name=gb_decode(line[2]))
            if not category:
                pass
            else:
                data=Item(pub_date=datetime.datetime.strptime(line[0],"%m/%d/%Y"),
                    price=line[1], 
                    category = category[0], 
                    comment = gb_decode(line[3]))
                data.save()
        i=i+1
    csv_file.close()

    destination = open('upload/csv/name.csv','w')
    destination.close()

    
def handle_uploaded_file_category(f, request):
    destination = open('upload/csv/name.csv','wb')
    for chunk in f.chunks(): 
        destination.write(chunk)
    destination.close()
    
    csv_file = open('upload/csv/name.csv','rU')
    reader = csv.reader(csv_file, dialect='excel')

    i=0
    for line in reader:
        if i>0:
            if line[0]==P_CATEGORY_NULL_NAME:
                data=Category(name=gb_decode(line[1]), 
                    isIncome = (line[2]=='True'),
                    user=request.user)
                
                data.save()
            else:
                pcategory = Category.objects.filter(user__username=request.user.username).filter(name=gb_decode(line[0]))
                if not pcategory:
                    pass
                else:
                    data=Category(p_category = pcategory[0],
                        name=gb_decode(line[1]), 
                        isIncome = (line[2]=='True'),
                        user=request.user)
                    
                    data.save()                
     
        i=i+1
    csv_file.close()    

    destination = open('upload/csv/name.csv','w')
    destination.close()

@login_required
def import_item_csv(request):

    if request.method == 'POST':
        form = UpLoadFileForm(request.POST,request.FILES)
        if form.is_valid():
            handle_uploaded_file_item(request.FILES['upLoadFile'], request)
            return HttpResponseRedirect("/jizhang")
           
    else:
        form = UpLoadFileForm()

    context = {'form':form,'username':request.user.username}
    return render_to_response('jizhang/import_item_csv.html', RequestContext(request,context))	

    
@login_required
def import_category_csv(request):

    if request.method == 'POST':
        form = UpLoadFileForm(request.POST,request.FILES)
        if form.is_valid():
            handle_uploaded_file_category(request.FILES['upLoadFile'], request)
            return HttpResponseRedirect("/jizhang/categorys")
           
    else:
        form = UpLoadFileForm()

    context = {'form':form,'username':request.user.username}
    return render_to_response('jizhang/import_category_csv.html', RequestContext(request,context))
    
@login_required    
def autocomplete_comments(request):
    term = request.GET.get('term')

    if not term:
        items=Item.objects.filter(category__user__username=request.user.username)[:12]
    else:
        items=Item.objects.filter(category__user__username=request.user.username).filter(comment__icontains=term)[:12]
    json_comments = []
    for item in items:
        have_track = 0
        for json_c in json_comments:
            if json_c['value'] == item.comment and json_c['category_id'] == item.category.id:
                have_track=1
                break

        if have_track==0:
            json_comments.append({"id": item.id,
                             "category_id": item.category.id,
                             "label": item.comment+"--"+item.category.name,
                             "value": item.comment
                             })
    return HttpResponse(json.dumps(json_comments), content_type="application/json") 
        
	
    
def first_login_category(userid):
    new_category=Category(name=u'工作收入',isIncome=True,user_id=userid)
    new_category.save()
    pid = new_category.id
    sub_category=Category(name=u'工资收入',isIncome=True,user_id=userid,p_category_id=pid)
    sub_category.save()
    sub_category=Category(name=u'股票收入',isIncome=True,user_id=userid,p_category_id=pid)
    sub_category.save()
    sub_category=Category(name=u'奖金收入',isIncome=True,user_id=userid,p_category_id=pid)
    sub_category.save()
    sub_category=Category(name=u'其他收入',isIncome=True,user_id=userid,p_category_id=pid)
    sub_category.save()
    
    new_category=Category(name=u'餐饮',isIncome=False,user_id=userid)
    new_category.save()
    pid = new_category.id
    sub_category=Category(name=u'早餐',isIncome=False,user_id=userid,p_category_id=pid)
    sub_category.save()
    sub_category=Category(name=u'午餐',isIncome=False,user_id=userid,p_category_id=pid)
    sub_category.save()
    sub_category=Category(name=u'晚餐',isIncome=False,user_id=userid,p_category_id=pid)
    sub_category.save()
    sub_category=Category(name=u'饮料水果',isIncome=False,user_id=userid,p_category_id=pid)    
    sub_category.save()
    sub_category=Category(name=u'零食',isIncome=False,user_id=userid,p_category_id=pid)     
    sub_category.save()
    
    new_category=Category(name=u'交通',isIncome=False,user_id=userid)
    new_category.save()
    pid = new_category.id
    sub_category=Category(name=u'公交地铁',isIncome=False,user_id=userid,p_category_id=pid)
    sub_category.save()
    sub_category=Category(name=u'加油',isIncome=False,user_id=userid,p_category_id=pid)
    sub_category.save()
    sub_category=Category(name=u'停车过路',isIncome=False,user_id=userid,p_category_id=pid)
    sub_category.save()
    sub_category=Category(name=u'汽车保养',isIncome=False,user_id=userid,p_category_id=pid)    
    sub_category.save()
    sub_category=Category(name=u'打的',isIncome=False,user_id=userid,p_category_id=pid)     
    sub_category.save()
    
    new_category=Category(name=u'购物',isIncome=False,user_id=userid)
    new_category.save()
    pid = new_category.id
    sub_category=Category(name=u'生活用品',isIncome=False,user_id=userid,p_category_id=pid)
    sub_category.save()
    sub_category=Category(name=u'衣裤鞋帽',isIncome=False,user_id=userid,p_category_id=pid)
    sub_category.save()
    sub_category=Category(name=u'化妆品',isIncome=False,user_id=userid,p_category_id=pid)
    sub_category.save()
    sub_category=Category(name=u'首饰手表',isIncome=False,user_id=userid,p_category_id=pid)    
    sub_category.save()
    sub_category=Category(name=u'宝宝用品',isIncome=False,user_id=userid,p_category_id=pid)     
    sub_category.save()    
    sub_category=Category(name=u'书籍报刊',isIncome=False,user_id=userid,p_category_id=pid)     
    sub_category.save() 
    
    new_category=Category(name=u'医疗',isIncome=False,user_id=userid)
    new_category.save()
    pid = new_category.id
    sub_category=Category(name=u'看病门诊',isIncome=False,user_id=userid,p_category_id=pid)
    sub_category.save()
    sub_category=Category(name=u'药店买药',isIncome=False,user_id=userid,p_category_id=pid)
    sub_category.save()
    sub_category=Category(name=u'保健品',isIncome=False,user_id=userid,p_category_id=pid)
    sub_category.save()
