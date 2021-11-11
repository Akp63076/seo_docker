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


import logging
logger = logging.getLogger(__name__)

filepath = os.path.join(BASE_DIR,"web_analytics/auth")
GSC_CREDS = 'client_secrets.json'

def gsc_authorize_creds():
    os.chdir(filepath)
    try :
        SCOPES = ["https://www.googleapis.com/auth/webmasters",
                'https://www.googleapis.com/auth/webmasters.readonly']
        CLIENT_SECRETS_PATH = GSC_CREDS
 
        # Create a parser to be able to open browser for Authorization
        parser = argparse.ArgumentParser(
            formatter_class=argparse.RawDescriptionHelpFormatter,
            parents=[tools.argparser])
        
        flags = parser.parse_args([])
        
        flow = client.flow_from_clientsecrets(
            CLIENT_SECRETS_PATH, scope = SCOPES,
            message = tools.message_if_missing(CLIENT_SECRETS_PATH))
        
        # Prepare credentials and authorize HTTP
        # If they exist, get them from the storage object
        # credentials will get written back to a file.
        storage = file.Storage('authorizedcreds.dat')
        
        credentials = storage.get()
        
    
        # If authenticated credentials don't exist, open Browser to authenticate
        if credentials is None or credentials.invalid:
            credentials = tools.run_flow(flow, storage, flags)
        http = credentials.authorize(http=httplib2.Http())
        webmasters_service = build('searchconsole', 'v1', http=http)
        # webmasters_service = build('webmasters', 'v3', http=http)
        
        return webmasters_service
    except Exception as e:
        logger.error("function name gsc_authorize_creds",e)
        return {}


def gsc_data_collector(domain,SITE_URL,webmasters_service,url,operator,startDate,endDate,dimension):
    #https://developers.google.com/webmaster-tools/search-console-api-original/v3/how-tos/all-your-data
    try :
        request = {
                    'startDate' : startDate,
                    'endDate' : endDate,
                    'dimensions' : dimension,
                
                    "searchType": "Web",
                        'dimensionFilterGroups': [{
                'filters': [{
                    'dimension':['page'] ,
                    # "operator": "contains",
                    "operator":operator,
                    #   eg : 'expression': 'https://collegedunia.com/university/25356-indian-institute-of-technology-iit-hyderabad'
                    'expression': url,
                }]
            }],   
                    # 'rowLimit' : maxRows,
                    # 'startRow' : i * maxRows
                }
        response = webmasters_service.searchanalytics().query(siteUrl = domain, body=request).execute()
        return response
    except Exception as e:
        logger.error('function name gsc_data_collectore :',e)
        return {}

def gsc_response_dataframe(SITE_URL,response,url):   
    url_m =url.replace(SITE_URL,"") 
    gsc_df = pd.DataFrame([[url_m,"","","",""]],columns=['key', 'clicks', 'impressions', 'ctr', 'avg_position'])
    output_rows = []
    try:
        for row in response['rows']:
            key = row['keys'][0]            
            # output_row = [page,keyword, device ,row['clicks'], row['impressions'], row['ctr'], row['position']]
            output_row = [key,row['clicks'], row['impressions'], row['ctr'], row['position']]
            output_rows.append(output_row)

        gsc_df = pd.DataFrame(output_rows, columns=['key', 'clicks', 'impressions', 'ctr', 'avg_position']) #'query', 'device',
        gsc_df['key'] = gsc_df['key'].apply(lambda x: x.replace(SITE_URL,""))
        gsc_df[['ctr']] = gsc_df[['ctr']]*100
        gsc_df = gsc_df.round(2)
    except Exception as e:
        logger.error("function name gsc_response_dataframe : ",e)
    # 
    return gsc_df

def gsc_function(domain,site_url,url,startDate,endDate,operator,dimension):
    # url = "https://collegedunia.com/university/25356-indian-institute-of-technology-iit-hyderabad"
    # startDate='2020-03-01'
    # endDate='2021-03-01'
    # operator = "contains" or "equals",
    domain = domain
    SITE_URL = site_url
    url_m = url.replace(SITE_URL,"")
    gsc_data = pd.DataFrame([[url_m,"","","",""]],columns=['key', 'clicks', 'impressions', 'ctr', 'avg_position'])
    dimension = dimension # ["searchAppearance","country","page","query"]
  
    webmasters_service = gsc_authorize_creds()
    if webmasters_service == {}:
        return gsc_data
    response = gsc_data_collector(domain,SITE_URL,webmasters_service,url,operator,startDate,endDate,dimension)
    gsc_data = gsc_response_dataframe(SITE_URL,response,url)
    
    # print(gsc_data)
    return gsc_data

if __name__ == "__main__":
    BASE_DIR = os.getcwd()
    print(dir)
    filepath = os.path.join(BASE_DIR,"seoTool/web_analytics/auth")
    data = gsc_function("sc-domain:prepp.in","https://prepp.in","https://prepp.in/ssc-cgl-exam",'2020-03-01','2021-03-01',"contains",['page'])
    print(data)