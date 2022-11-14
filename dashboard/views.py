# from ast import keyword
# from django.core.cache import caches
# from tkinter import Frame
# from tkinter.tix import Select
# from django.db.models import Subquery,FloatField
from django.db.models.functions import Cast


# from multiprocessing.sharedctypes import Value
from django.db.models import Q,F
#from asyncio.log import logger
from django.shortcuts import render,HttpResponse,redirect,HttpResponseRedirect
import csv
from datetime import datetime,timedelta
from django.contrib.auth.decorators import login_required

# Create your views here.
import pandas as pd
from django.db import models
from django.core.paginator import Paginator

import logging
logger = logging.getLogger("django")
pd.options.display.float_format = '{:,.0f}'.format

from dashboard.models import description_table, domain_table, keyword_table, keyword_brand_table, brand_table

# Create your views here.




@login_required
def dashboard1(request):  
    if request.method=='GET':
        category1=request.GET.getlist('category1')              ### Category Filter for table 1 & 2
        if len(category1) == 0:
            category1=F('category')  

        search1=request.GET.get('low')                       ### Search Volume Range  Filter
        search2=request.GET.get('high')
        if search1 != None and search1 !='' and search2 != None and search2 !='':
            search_range=[search1,search2]
        else:
            search_range=[0,1000000000]
            
        category2=request.GET.getlist('category2')                      ### Category Filter for table 3 
        if len(category2) == 0:
            category2=F('category')
        tags=request.GET.get('tags')                              ### Tags  Filter
        if tags != None and tags !='':                               
            tags=list(map(lambda x: x.title().strip(),tags.split(',')))
        else:
            tags=F('keyword_tag_table__tag__tag')
        
        tracking_url=request.GET.get('tracking_url')                ### tracking url Filter
        if tracking_url != None and tracking_url !='':
            tracking_url=tracking_url.split(',')
        else:
            tracking_url=F('req_url')
        competitors=request.GET.getlist('competitor')                ### Competitor filter 
        if len(competitors)==0:                             
            competitors=['shiksha','careers360']
        

        time_range1=request.GET.get('time-range')                      ### Track_period  Filter for table 1 and 2
        if time_range1!= None and time_range1 !='':
           frequency1=time_range1
        else:
            frequency1='daily'
        daterange1=request.GET.get('daterange1')            
         ### Date Range  Filter on upper two table
        if daterange1 != None and daterange1 !='':
            date_range1=[datetime.strptime(d.strip(),"%d/%m/%Y").strftime("%Y-%m-%d") for d in daterange1.split('-')]            
        elif frequency1=='weekly':
            date_range1=[datetime.now() - timedelta(days=14),datetime.now()]            
        elif frequency1=='monthly':
            date_range1=[datetime.now() - timedelta(days=60),datetime.now()]            
        else:
            date_range1=[datetime.now() - timedelta(days=1),datetime.now()]             
        time_range2=request.GET.get('time-range2')                      ### Track_period  Filter for table 3
        if time_range2!= None and time_range2 !='':
           frequency2=time_range2
        else:
            frequency2='daily'
        daterange2=request.GET.get('daterange2')                                               ### Date Range  Filter on lower table
        if daterange2 != None and daterange2 !='':
            date_range2=[datetime.strptime(d.strip(),"%d/%m/%Y").strftime("%Y-%m-%d") for d in daterange2.split('-')]    
        elif frequency2=='weekly':            
            date_range2=[datetime.now() - timedelta(days=28),datetime.now()]
        elif frequency2=='monthly':            
            date_range2=[datetime.now() - timedelta(days=120),datetime.now()]
        else:            
            date_range2=[datetime.now() - timedelta(days=3),datetime.now()]
    keydata=keyword_table.objects.all()
    key_count=keydata.count()
    category_filter=keydata.values_list('category').distinct()
    competitor=domain_table.objects.values_list('domain')
    competitor_count=competitor.count()
    try:
        dash1_data1=keyword_table.objects.prefetch_related().filter(
            description_table__desc_id__contains=frequency1,description_table__domain__domain__in=['collegedunia','shiksha'],keyword_frequency_table__frequency__frequency=frequency1,
        description_table__date__range=date_range1,category__in=category1).values(
            'category','description_table__date','description_table__domain__domain').annotate(
                Below_1k=models.Count(models.Case(models.When(search_volume__lte= 1000, then='description_table__url')),distinct=True),
        Below_10k=models.Count(models.Case(models.When(search_volume__gte= 1001,search_volume__lte = 10000, then='description_table__url')),distinct=True),
        Below_100k=models.Count(models.Case(models.When(search_volume__gte= 10001,search_volume__lte = 100000, then='description_table__url')),distinct=True),
        Above_100k=models.Count(models.Case(models.When(search_volume__gte= 100001, then='description_table__url')),distinct=True))
        tbl1=pd.DataFrame(dash1_data1).pivot_table(index=['description_table__date','description_table__domain__domain'],columns='category',values=['Below_1k','Below_10k','Below_100k','Above_100k']).swaplevel(0,1,1).sort_index(1).T.rename_axis(columns={'description_table__domain__domain':None,'description_table__date':None})
        dash1_data1=tbl1.to_html(classes='search_volume_wise',bold_rows=False,border=None,table_id = 'weeklyranking',na_rep='0')
        request.session['tbl1']=tbl1.reset_index().to_json()
    except Exception as err:
        logger.error(err)
        dash1_data1=None
    
    try:

        dash2_data1=keyword_table.objects.prefetch_related().filter(description_table__date__range=date_range1,
        description_table__desc_id__contains=frequency1,keyword_frequency_table__frequency__frequency=frequency1,category__in=category1).values('category','keyword_tag_table__tag__tag').annotate(
            total_key=models.Count('keyword',distinct=True), cd_prepp=models.Count(models.Case(models.When(
                description_table__domain__domain__in=['collegedunia','prepp'],description_table__pos=1, then='keyword')),distinct=True)).values('category','keyword_tag_table__tag__tag','total_key','cd_prepp','description_table__date').order_by('category')
        tbl2=pd.DataFrame(dash2_data1).rename(columns={'keyword_tag_table__tag__tag':'Tag','category':'Category','description_table__date':'date','total_key':'Total Key','cd_prepp':'CD/Prepp'}).pivot_table(index=['Category','Tag'],columns='date',values=['Total Key','CD/Prepp']).rename_axis(columns={'date': None}).swaplevel(0,1,1).sort_index(axis=1)
        dash2_data1=tbl2.to_html(classes='top_rank_wise',bold_rows=False,border=None,table_id = 'topranking',na_rep='--')
        request.session['tbl2']=tbl2.reset_index().to_json()
    except Exception as err:
        logger.error(err)
        dash2_data1=None    
    
    finally:
            try:
                dash3_data1=keyword_table.objects.prefetch_related().filter(description_table__desc_id__contains=frequency2,keyword_frequency_table__frequency__frequency=frequency2,description_table__domain__domain__in=['collegedunia','prepp'],
                description_table__date__range=date_range2,search_volume__range=search_range,keyword_tag_table__tag__tag__in=tags,category__in=category2,req_url__in=tracking_url).values(
                'keyword','search_volume','category','keyword_tag_table__tag__tag','req_url','description_table__url','description_table__date','description_table__pos').order_by('keyword','-description_table__date')
       
                df=pd.DataFrame(dash3_data1)
                data=description_table.objects.select_related('keyword','domain').filter(date__range=date_range2).values_list('keyword__keyword',
                'date','domain__domain','pos').order_by('keyword__keyword','-date','pos').distinct('keyword__keyword')
                df=(((pd.DataFrame(data).rename(columns={0:'keyword',2:'Top Ranker'}).set_index('keyword').loc[:,'Top Ranker']).to_frame().join(df.set_index('keyword'),how='right'))).reset_index().rename(columns={'keyword':'Keyword','category':'Category','search_volume':'Search Volume','req_url':'Tracking URL','keyword_tag_table__tag__tag':'Tag','description_table__url':'Ranking URL','description_table__date':'Date','description_table__pos':'pos'})              
                data=df.pivot_table( index=['Keyword','Search Volume','Category','Tag','Tracking URL','Ranking URL','Top Ranker'] ,columns=['Date'],values=['pos']).rename_axis(columns={'Date': None})
                

                topcomp=description_table.objects.select_related('keyword','domain').filter(desc_id__contains=frequency2,date__in=dash3_data1.values_list('description_table__date').order_by('-description_table__date')[0],domain__domain__in=competitors).values('keyword__keyword','date','domain__domain','pos').order_by('keyword__keyword','-date')
                topcomp=pd.DataFrame(topcomp)
                
                topcomp=topcomp.pivot_table(index=['keyword__keyword'],columns=['domain__domain'],values=['pos']).rename_axis(columns={'domain__domain':None}).reset_index().rename(columns={'keyword__keyword':'Keyword'})           
                dash3_data1=pd.merge(data.reset_index(),topcomp,how='left')
                                
                dash3_data1=dash3_data1.iloc[dash3_data1.isnull().sum(1).sort_values(ascending=True).index] 
                
                tag_data=dash3_data1.groupby(['Keyword','Ranking URL']).apply(lambda x: ' , '.join(x.Tag)).reset_index().rename(columns={})
                df=pd.merge(dash3_data1,tag_data[[0,'Keyword']],on='Keyword',how='left')
                df[('Tag', '')]=df[0]
                dash3_data1=df.drop([0,'Keyword'],axis=1).drop_duplicates(keep='first')
                dash3_data1=dash3_data1.fillna(0).astype(int,errors='ignore').to_dict('records')
                row = request.GET.get('row-counter')
                if row == None:
                    row = 10
                paginator = Paginator(dash3_data1, row) #row Show  contacts per page. 
                page_number = request.GET.get('page')
                summary = paginator.get_page(page_number)
            except Exception as e :                     
                logger.error(e)
                

            finally: 
                if len(dash3_data1)==0:
                    summary=None
                
                request.session['dash3_data1']=pd.DataFrame(dash3_data1).to_json() 
                key=request.GET.get('key')
                if key != None and  key !='' :
                    date_data,pos_data=trend(request) 
                else:
                    date_data=None
                    pos_data=None                  
                return render(request,'dashboard/newdashboard.html',{'key_count':key_count,'competitor_count':competitor_count,'dash1_data1':dash1_data1,'dash2_data1':dash2_data1,'dataframe':summary,'category':category_filter,'competitor':competitor,'date_data':date_data,'pos_data':pos_data})
                    
   
   
           

def trend(request):
    if request.method=='GET':
        key = request.GET.get('key')
        date_range=request.GET.get('date_range')
        if date_range ==None or date_range =='':
            date_range=30
        data=description_table.objects.select_related('keyword','domain').filter(keyword__keyword=key,domain__domain='collegedunia',date__gte=datetime.now() - timedelta(days=int(date_range))).values_list('date','pos')
    date_data=[]
    pos_data=[]
    for i in data:
        date_data.append(i[0].strftime('%d-%m-%Y'))
        pos_data.append(i[1])
        date_data.sort(key=lambda date: datetime.strptime(date, "%d-%m-%Y"))
    return date_data,pos_data
    

def export_dash(request):
    try:
        export=request.GET.get('export')
        logger.info(export)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=Ranking data.csv' 
        if export == '2':
            dash3_data1=request.session['dash3_data1']                  
            pd.read_json(dash3_data1).to_csv(response,index=False)            
            del request.session['dash3_data1']
        if export =='1':
            tbl1=request.session['tbl1']
            tbl2=request.session['tbl2']
            pd.read_json(tbl1).to_csv(response,index=False)
            pd.read_json(tbl2).to_csv(response,index=False )
            del request.session['tbl1']
            del request.session['tbl2']
    except Exception as e  :
        logger.error(e)
        print(" please refresh pages or select filters again ")
        return redirect('../')
    else:
        return response
        
    

# data=description_table.objects.select_related('keyword','domain').filter(keyword__keyword__in=dash3_data1.values_list('keyword'),date__range=date_range2).values_list('keyword__keyword',
#                 'date','domain__domain','pos').order_by('keyword__keyword','-date','pos').distinct('keyword__keyword')
               
#  topcomp=description_table.objects.select_related('keyword','domain').filter(desc_id__contains=frequency2,keyword__keyword__in=dash3_data1.values_list('keyword'),date__in=dash3_data1.values_list('description_table__date').order_by('-description_table__date')[0],domain__domain__in=competitors).values('keyword__keyword','date','domain__domain','pos').order_by('keyword__keyword','-date')
             