#Load Libraries
import argparse
import datetime
import os
import re
import json
from collections import defaultdict
from datetime import date, timedelta

import pandas as pd
from urllib.parse import urlparse

import httplib2
from http.client import responses
from dateutil import relativedelta
# from apiclient.discovery import build
from googleapiclient.discovery import build
from oauth2client import client, file, tools
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.service_account import ServiceAccountCredentials

from seoTool.settings import BASE_DIR
filepath = os.path.join(BASE_DIR,"web_analytics/auth")


import logging
logger = logging.getLogger(__name__)

GA_CREDS =  'rank_tool_api.json'
def ga_response_dataframe(response):
    row_list = []
    # Get each collected report
    for report in response.get('reports', []):
        # Set column headers
        column_header = report.get('columnHeader', {})
        dimension_headers = column_header.get('dimensions', [])
        metric_headers = column_header.get('metricHeader', {}).get('metricHeaderEntries', [])
    
        # Get each row in the report
        for row in report.get('data', {}).get('rows', []):
            # create dict for each row
            row_dict = {}
            dimensions = row.get('dimensions', [])
            date_range_values = row.get('metrics', [])

            # Fill dict with dimension header (key) and dimension value (value)
            for header, dimension in zip(dimension_headers, dimensions):
                row_dict[header] = dimension

            # Fill dict with metric header (key) and metric value (value)
            for i, values in enumerate(date_range_values):
                for metric, value in zip(metric_headers, values.get('values')):
                # Set int as int, float a float
                    if ',' in value or '.' in value:
                        row_dict[metric.get('name')] = float(value)
                    else:
                        row_dict[metric.get('name')] = int(value)

            row_list.append(row_dict)
    return pd.DataFrame(row_list)

def ga_authorize_creds():
    try : 
        os.chdir(filepath)
        OAUTH_SCOPE = ['https://www.googleapis.com/auth/analytics.readonly']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(GA_CREDS, OAUTH_SCOPE)
        analytics_service = build('analyticsreporting', 'v4', credentials=credentials)
        logger.info("ga auth successful")
        return analytics_service
    except Exception as e:
        logger.error("function ga_authorize_creds",e)
        return None

def ga_main_data_collector(view_id,analytics_service,url_with_operator,startDate,endDate): 
    try :
        
        VIEW_ID = view_id
        response = analytics_service.reports().batchGet(body={
            'reportRequests': [
                {
                'viewId': VIEW_ID,
                'dateRanges': [{'startDate':startDate , 'endDate':endDate }],
                'metrics': [{'expression': 'ga:sessions'},
                            {'expression': 'ga:bounceRate'},
                            {'expression': 'ga:pageviewsPerSession'},
                            {'expression': 'ga:avgSessionDuration'},
                            {'expression': 'ga:avgTimeOnPage'},
                            {'expression':'ga:goal4Starts'}
                            ],
                'dimensions': [{'name': 'ga:landingPagePath'}],
                "orderBys":[{"fieldName":"ga:sessions","sortOrder": "DESCENDING"}],
                # 'filtersExpression':"ga:landingPagePath=@/university/25356-indian-institute-of-technology-iit-hyderabad"
                'filtersExpression':"ga:landingPagePath"+url_with_operator
                }]}).execute()
                
          
        return response
    except Exception as e:
        logger.error('function ga_main_data_collector',e)
        return {}

def main_analytics_func(VIEW_ID,url,startDate,endDate,operator):  
    
    #input data
    gaMAinDf = pd.DataFrame([[url,"","","","","",""]],
                        columns=['Landing_page','sessions','Bounce_Rate',
                        'Pages_per_Session','Avg_Session_Duration','Avg_TimeOnPage','Leads_Filled'])
    url_with_operator = operator+url
    analytics_service = ga_authorize_creds()
    if analytics_service is None:
        return gaMAinDf
    response= ga_main_data_collector(VIEW_ID,analytics_service,url_with_operator,startDate,endDate)
    # print(response)
    if response == {}:
        return gaMAinDf
    try : 
        ga_df = ga_response_dataframe(response)
    except Exception as e:
        logger.error('function main_analytics_func , error in ga_df variable',e)
        ga_df = gaMAinDf.copy()
    #renameing of columns
    # print(ga_df)
    ga_df = ga_df.rename(columns={'ga:landingPagePath': "Landing_page", 
                        'ga:sessions':"sessions",
                        'ga:bounceRate':"Bounce_Rate", 
                        'ga:pageviewsPerSession':"Pages_per_Session",   
                        'ga:avgSessionDuration':"Avg_Session_Duration",
                        'ga:avgTimeOnPage':"Avg_TimeOnPage",
                        'ga:goal4Starts':"Leads_Filled" ,})
    # convert in minutes avgSessionDuration,avgTimeOnPage
    ga_df[["Avg_Session_Duration" , "Avg_TimeOnPage"]] = ga_df[["Avg_Session_Duration" , "Avg_TimeOnPage"]]/60
    ga_df = ga_df.round(2)
    return ga_df

def ga_events_data_collector(view_id,analytics_service,url_with_operator,startDate,endDate): 
    try :
        
        VIEW_ID = view_id
        response = analytics_service.reports().batchGet(body={
            'reportRequests': [
                {
                'viewId': VIEW_ID,
                'dateRanges': [{'startDate':startDate , 'endDate':endDate }],
                'metrics': [{'expression': 'ga:totalEvents'},
                            {'expression': 'ga:uniqueEvents'},
                            {'expression': 'ga:eventValue'},
                            {'expression': 'ga:avgEventValue'},
                            ],
                'dimensions': [{'name': 'ga:eventAction'}],
                "orderBys":[{"fieldName":'ga:totalEvents',"sortOrder": "DESCENDING"}],
                # 'filtersExpression':"ga:landingPagePath=@/university/25356-indian-institute-of-technology-iit-hyderabad"
                'filtersExpression':"ga:landingPagePath"+url_with_operator
                }]}).execute()
        return response
    except Exception as e:
        logger.error('function ga_events_data_collector',e)
        return {}

def events_analytics_func(VIEW_ID,url,startDate,endDate,operator):  
    
    #input data
    gaEventsDf = pd.DataFrame(columns =["event_action","totalEvents","uniqueEvents","eventValue","avgEventValue"])
    url_with_operator = operator+url
    #inputs data
    # url = "exams/neet"
    # startDate ='90daysAgo'
    # endDate = 'today'
    #authoriztion
    analytics_service = ga_authorize_creds()
    
    if analytics_service is None:
        return gaEventsDf
    response= ga_events_data_collector(VIEW_ID,analytics_service,url_with_operator,startDate,endDate)
    # print(response)
    if response == {}:
        return gaEventsDf
    try:
        ga_df = ga_response_dataframe(response)
    except Exception as e:
        logger.error('function events_analytics_func :',e)
        ga_df = gaEventsDf.copy()

    #renameing of columns
    # print(ga_df)
    ga_df = ga_df.rename(columns={'ga:eventAction': "event_action", 
                        'ga:totalEvents':"totalEvents",
                        'ga:uniqueEvents':"uniqueEvents", 
                        'ga:eventValue':"eventValue",   
                        'ga:avgEventValue':"avgEventValue",})
    # convert in minutes avgSessionDuration,avgTimeOnPage
    ga_df = ga_df.round(2)
    return ga_df

if __name__ == "__main__":
    BASE_DIR = os.getcwd()
    print(dir)
    filepath = os.path.join(BASE_DIR,"seoTool/web_analytics/auth")
    VIEW_ID = '211130889'
    data = main_analytics_func(VIEW_ID,"/ssc-cgl-exam","90daysAgo",'today',"=@")
    event_data = events_analytics_func(VIEW_ID,"/ssc-cgl-exam","90daysAgo",'today',"=@")
    print(data)
    print(event_data)