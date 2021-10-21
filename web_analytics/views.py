import csv 
from datetime import date,datetime,timedelta
from multiprocessing import context
import os, tempfile, zipfile
import mimetypes

from django.shortcuts import render,HttpResponse
from django.contrib.auth.decorators import login_required 
from django.http import HttpResponseRedirect

from .forms import Myform ,AdForm
from . import functions

from wsgiref.util import FileWrapper

import logging
logger = logging.getLogger(__name__)


def homepage(request):
    return render(request, 'web_analytics/homepage.html')

@login_required
def index(request):
    
    if request.method == 'POST':
        form = Myform(request.POST)
        if form.is_valid():
            #input parameters 
            
            
            url = request.POST['Link']
            range = request.POST['Range']
            print(url,range)
            today  = datetime.today()
            endDate = today.strftime("%Y-%m-%d")
            if functions.domain_check(url):
                form = Myform()
                logger.error(endDate,":provided url : ",url)
                return render(request, 'web_analytics/indexform.html', {'form':form,'error':"Incorrect domain"})



            
            startDate = functions.get_startDate(range)
            # print(startDate,endDate)
            context = functions.data_operation(url,startDate,endDate,range)
            context['user_url'] = url
            context['user_range'] = range

            return render(request,'web_analytics/result.html',context)
    else:
        form = Myform()
        
    return render(request, 'web_analytics/indexform.html', {'form':form})

@login_required
def kwplanner(request):
    
    if request.method == 'POST':
        form = AdForm(request.POST)
        if form.is_valid():
            #input parameters 
            keyword = request.POST['keyword']

            keyword = keyword.strip().split("\r\n")
            
            print(keyword)
            #call adword function to get volume and ideas
            context = {}
            context = functions.KwplannerOperation(keyword)
            # print(context)
            # context['user_keyword'] = keyword
            request.session['filename'] = context['path']

            return render(request,'web_analytics/ad_result.html',context)
    else:
        form = AdForm()
        
    return render(request, 'web_analytics/ad_indexform.html', {'form':form})


def getfile(request):  
    filename=request.session['filename']
    print(filename)
    chunk_size=8092
    wrapper = FileWrapper(open(filename, 'rb'), chunk_size)
    download_name ="ideas.csv"
    content_type='text/csv'
    response = HttpResponse(wrapper,content_type=content_type)  
    response['Content-Length']  = os.path.getsize(filename) 
    response['Content-Disposition'] = f'attachment; filename="{download_name}"'   
    return response