
import string
import random
import sys
import itertools
from multiprocessing import Pool
import uuid


import pandas
from datetime import date,datetime,timedelta
from web_analytics.auth.google_analytics import  main_analytics_func as method1
from web_analytics.auth.google_analytics import events_analytics_func as method2
from web_analytics.auth.search_analytics import gsc_function as method3
from web_analytics.auth.adwords import kwvolume,kwIdeas
from multiprocessing import Process, Queue
from django.conf import settings

import logging
logger = logging.getLogger(__name__)

fileDir = settings.STATIC_ROOT
range_conv = {"1 week":7,
            "1 month":30,
            "3 month":90,
            "6 month":180,
            "1 year":360}

def domain_check(url):
    domain_list = set(['prepp.in','collegedunia.com'])
    url_list = set(url.strip().split("/"))
    if (domain_list & url_list):
        return False
    else:
        return True


def get_startDate(range):
    init_date= datetime.now()

    req_days = range_conv[range]

    startDat = (init_date - timedelta(days =req_days)).strftime("%Y-%m-%d")

    return startDat

def get_prevstartDate(range):
    init_date= datetime.now()
 
    req_days = 2*range_conv[range]

    startDat = (init_date - timedelta(days =req_days)).strftime("%Y-%m-%d")
 
    return startDat

def unzip_func(a,b):
    return a,b

def distributor(option_args):
    option, args = unzip_func(*option_args)    # unzip option and args 

    attr_name = "method"+str(option)      
    # creating attr_name depending on option argument

    value = getattr(sys.modules[__name__], attr_name)(*args) 
    # call the function with name 'attr_name' with argument args

    return value



def data_operation(url,startDate,endDate,range):
            
    url = url.replace("http://",'https://')
    domain_dict = {'prepp.in':"211130889",
                    "collegedunia" : "86509496"}

    if "collegedunia" in url:
        domain = "https://collegedunia.com"
        SITEURL = "https://collegedunia.com"
        VIEW_ID = domain_dict['collegedunia']
        
    elif "prepp" in url:
        domain="sc-domain:prepp.in"
        VIEW_ID = domain_dict['prepp.in']
        SITEURL = 'https://prepp.in'
        
    else :
        print("not correct domain")
    print(domain,VIEW_ID)
    ga_url = url.replace(SITEURL,"")
    print(ga_url)
    gsc_operator = "contains"
    ga_operator = "=@"
    

    ##prev week/month/year data
    prevendDate = get_startDate(range)
    prevstartDate= get_prevstartDate(range)
    print(prevendDate,prevstartDate,"prevendDate ,prevstartDate")
    
    # #page data
    # gsc_page_data = gsc_function(domain,url,startDate,endDate,gsc_operator,['page'])
    # # Query data
    # gsc_query_data = gsc_function(domain,url,startDate,endDate,gsc_operator,['query','page'])
    # #google analytics main key perfornce data
    # ga_data = main_analytics_func(VIEW_ID,ga_url,startDate,endDate,ga_operator)
    # # events data
    # events_df = events_analytics_func(VIEW_ID ,ga_url,startDate,endDate,ga_operator)

    # #prev data
    # gsc_prev_page_data = gsc_function(domain,url,prevstartDate,prevendDate,gsc_operator,['page'])
    # ga_prev_data = main_analytics_func(VIEW_ID,ga_url,prevstartDate,prevendDate,ga_operator)
    
    option_list = [3,3,1,2,3,1]      # for selecting the method number
    args_list = [(domain,SITEURL,url,startDate,endDate,gsc_operator,['page']),
            (domain,SITEURL , url,startDate,endDate,gsc_operator,['query','page']),
            (VIEW_ID,ga_url,startDate,endDate,ga_operator),
            (VIEW_ID,ga_url,startDate,endDate,ga_operator),
            (domain,SITEURL, url,prevstartDate,prevendDate,gsc_operator,['page']),
            (VIEW_ID,ga_url,prevstartDate,prevendDate,ga_operator)] 

    p = Pool(6)
    result = p.map(distributor, zip(option_list, args_list))
    
    gsc_page_data = result[0]
    gsc_query_data = result[1]
    ga_data = result[2]
    events_df = result[3]
    gsc_prev_page_data = result[4]
    ga_prev_data = result[5]
    #df to dict
    gsc_dict = gsc_page_data.to_dict("records")
    gsc_query_dict = gsc_query_data.to_dict("records")
    ga_dict= ga_data.to_dict("records")
    events_dict = events_df.to_dict("records")
    
    # merging table of ga and gsc
    df = gsc_page_data.merge(ga_data,left_on="key",right_on="Landing_page")
    df = df[df['key'] ==ga_url]
    # converting merged df to dict
    user_cur_df= df.to_dict("records")

    # merge prev console and ga data 
    prev = gsc_prev_page_data.merge(ga_prev_data,left_on="key",right_on="Landing_page")
    prev =prev[prev['key'] ==ga_url]
    
    user_prev_df= prev.to_dict("records")
    

    return {"gsc_data":gsc_dict,
            "ga_data":ga_dict,
            "requested_df":user_cur_df,
            "prev":user_prev_df,
            "gsc_query_dict":gsc_query_dict,
            "scroll":events_dict}



def KwplannerOperation(keywordlist):
    init_date= datetime.now().strftime("%Y-%m-%d")
    unique = str(uuid.uuid4())

    fileVariable = unique+init_date
    filePath = fileDir+"/web_analytics/csvFiles/"

    fileName= "ideas"+fileVariable+".csv"
    completePath = filePath+fileName
    kwdf = kwvolume(keywordlist)
    kwdf = kwdf.sort_values(by=['search_volume'],ascending=False)
    kwdf = kwdf.round(2)
    kw_dict = kwdf.to_dict("records")
    
    ideasdf = kwIdeas(keywordlist)
    ideasdf = ideasdf.sort_values(by=['search_volume'],ascending=False)
    ideasdf = ideasdf.round(2)
    ideas_dict = ideasdf.to_dict("records")
    
    both_df = kwdf.append(ideasdf)
    both_df.to_csv(completePath,index=False)
    
    

    return {"kwsv" :kw_dict,"kwideas" : ideas_dict,"path":completePath}

def onPageseo():
    pass

#reference for multiprocessing : https://stackoverflow.com/questions/43474923/two-functions-in-parallel-with-multiple-arguments-and-return-values
# unpack tupple : https://www.geeksforgeeks.org/unpacking-a-tuple-in-python/

