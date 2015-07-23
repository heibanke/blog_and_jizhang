#coding=utf-8
import re
#[id, name, pid]
def sort_category(category_list,pid,row_start,level):
	row_num = len(category_list)
	tmp=[]
	for row_i in range(row_start,row_num):
		category = category_list[row_i]
		
		#print(row_i,row_start, level, pid,category, category[1]==pid, row_start<=row_num)
		if  category[2]==pid:
			
			#print(row_i,row_start, level)
			tmp=category
			category_list[row_i]=category_list[row_start]
			category_list[row_start]=tmp
			category_list[row_start][1]=level*'----'+category_list[row_start][1]
			category_list,row_start = sort_category(category_list,category[0],row_start+1,level+1)
			
	return category_list,row_start
	
	
def check_parent_category(id,pid,choice):
	level = 1000
	isvalid=True
	for aa in choice:
	
		if level<len(re.split(r'----',aa[1])):
			#sub category
			#print(aa)
			if pid==aa[0]:
				isvalid=False
		elif not level==1000:
			break
		
		if aa[0]==id:
			level = len(re.split(r'----',aa[1]))
			#print(aa[1])
	return isvalid


	
if __name__ == '__main__':
	
	#id, pid, name
	category_list=[{'id':2,'name':'收入','pid':0,'sum':['30','20']},{'id':6,'name':'lp股票收入','pid':5,'sum':['30','20']},{'id':5,'name':'lp收入','pid':2,'sum':['30','20']},{'id':4,'name':'汽车消费','pid':3,'sum':['30','20']}]
	
	tmp,row_start = sort_category(category_list,0,0,0)
	
	aa=[]
	for category in tmp:
		aa.extend((category["id"], category["sum"].extend(category["name"])))

	print(aa)

	id = 3
	choice=[('', '----------------'),
		 (1, '生活消费'),
		 (2, '----生活用品'),
		 (3, '----汽车消费'),
		 (4, '--------加油'),
		 (5, '--------汽车养护'),
		 (6, '--------停车过路'),
		 (7, '----医疗保健'),
		 (13, 'lg收入'),
		 (12, '----股票收入'),
		 (11, '----工资收入')]
 
	print(check_parent_category(id,5,choice))
	print(check_parent_category(id,7,choice))
