import json
import logging
import requests
import pandas as pd
import datetime
import time
import tldextract
import ssl
import urllib.request
import urllib.parse
import logging

output_timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H")

logger = logging.getLogger(__name__)

def get_response(keyword,folder,country):
    ssl._create_default_https_context = ssl._create_unverified_context
    query = urllib.parse.quote(keyword).replace('/','%2F')
    if folder == 'zoutons':
        if country == 'uae':
            opener = urllib.request.build_opener(
                urllib.request.ProxyHandler(
                    {'http': 'http://brd-customer-c_a4a3b5b0-zone-content_scraping:cgfv9xdh0va6@zproxy.lum-superproxy.io:22225',
                    'https': 'http://brd-customer-c_a4a3b5b0-zone-content_scraping:cgfv9xdh0va6@zproxy.lum-superproxy.io:22225'}))
            response = opener.open('https://www.google.com/search?q='+query+'&gl=ae&hl=ar&num=100&lum_json=1')
        else :
            opener = urllib.request.build_opener(
                urllib.request.ProxyHandler(
                    {'http': 'http://brd-customer-c_a4a3b5b0-zone-content_scraping:cgfv9xdh0va6@zproxy.lum-superproxy.io:22225',
                    'https': 'http://brd-customer-c_a4a3b5b0-zone-content_scraping:cgfv9xdh0va6@zproxy.lum-superproxy.io:22225'}))
            response = opener.open('https://www.google.com/search?q='+query+'&gl=sa&hl=ar&num=100&lum_json=1')
    else:
        opener = urllib.request.build_opener(
            urllib.request.ProxyHandler(
                {'http': 'http://brd-customer-c_a4a3b5b0-zone-content_scraping:cgfv9xdh0va6@zproxy.lum-superproxy.io:22225',
                'https': 'http://brd-customer-c_a4a3b5b0-zone-content_scraping:cgfv9xdh0va6@zproxy.lum-superproxy.io:22225'}))
        response = opener.open('https://www.google.com/search?q='+query+'&gl=in&location=New+Delhi%2CDelhi%2CIndia&uule=w+CAIQICIVTmV3IERlbGhpLERlbGhpLEluZGlh&num=100&hl=en&lum_json=1')
    
    #saudi arabia &gl=sa&hl=ar&num=100&lum_json=1
    #uae &gl=ae&hl=ar&num=100&lum_json=1
    #new delhi &gl=in&location=New+Delhi%2CDelhi%2CIndia&uule=w+CAIQICIVTmV3IERlbGhpLERlbGhpLEluZGlh&num=100&hl=en&lum_json=1
    return response

websites = [
            'collegedunia',
            'prepp',
            'shiksha',
            'careers360',
            'collegedekho',
           "aglasem",
           "byjus",
           "fresherslive",
            "embibe" ,
            "leverageedu",
            "buddy4study",
            "careerpower",
            "byjusexamprep",
            "adda247",
            "vedantu",
            "toppr",
            "zollege",
            "testbook",
            "zoutons"
            ]

def get_rank(pagesource, keyword, WEBSITE):
    logging.info("----------------------------end of page source--------------")
    temp = pd.DataFrame(columns=['keyword','pos', 'url', 'desc', 'title', 'url_shown', 'pos_overall', 'domain','date'])
    try :
        data = pagesource
        json_object = json.dumps(data, indent = 4)
        with open("sample_bd.json", "w") as outfile:
            outfile.write(json_object)

        if "organic" in data.keys():
            organic_sr= pd.DataFrame(data['organic']) 
            organic_sr['domain'] = organic_sr['link'].apply(lambda row: tldextract.extract(row).domain)
            temp = organic_sr[organic_sr['link'].str.contains("|".join(WEBSITE))]
            if temp['rank'][temp['rank']==1].any():
                pass
            else :
                temp = pd.concat([temp,organic_sr[organic_sr['rank']==1]],ignore_index=True)
            temp['date'] = datetime.date.today().strftime("%d-%m-%Y")
            temp['keyword'] = keyword
            temp.rename(columns = {'link':'url', 'rank':'pos','description':'desc','global_rank':'pos_overall',
                                    'display_link': 'url_shown','link_title':'title'}, inplace = True)
            return temp[['keyword','pos', 'url', 'desc', 'title', 'url_shown', 'pos_overall', 'domain','date']]
    except Exception as e:
        logging.info(e, "error in get_rank block")
    else :
        return temp

def get_snippet(pagesource,keyword):
    ft_temp =  pd.DataFrame(columns=['keyword','url', 'desc', 'title', 'url_shown','pos_overall', 'domain'])
    try:
        data = pagesource
        if "featured_snippets" in data.keys():
            featured_snippet_sr= data['featured_snippets']
            ft_temp =pd.DataFrame(featured_snippet_sr )
            ft_temp['domain'] =  ft_temp['link'].apply(lambda row: tldextract.extract(row).domain)
            ft_temp['keyword'] = keyword
            ft_temp.rename(columns = {'link':'url', 'rank':'pos','description':'desc','global_rank':'pos_overall',
                                    'display_link': 'url_shown','link_title':'title'}, inplace = True)
            ft_temp['desc'] = 'N/A'
            for i in ft_temp.index:
                ft_temp['desc'][i] = ft_temp['value'][i]['text']
            return ft_temp[['keyword','url', 'desc', 'title', 'url_shown','pos_overall', 'domain']]
    except Exception as e:
        logging.info(e," error in get_snippet")
    return ft_temp

def get_rel_searches(pagesource,keyword):
    sr_temp = pd.DataFrame(columns=['keyword','rel_searches'])
    try:
        data = pagesource
        if "related" in data.keys():
            related_searches_sr= data['related']
            related_searches = [ i['text'] for i in related_searches_sr] 
            sr_temp = pd.DataFrame(related_searches,columns=["rel_searches"])
            sr_temp['keyword'] =keyword
            sr_temp.rename(columns = {'link':'url', 'rank':'pos','description':'desc','global_rank':'pos_overall',
                                    'display_link': 'url_shown','link_title':'title'}, inplace = True)
            return sr_temp[['keyword','rel_searches']]

    except Exception as e:
        logging.info(e,"error in get_rel_searches")
    else :
        return sr_temp

def get_rel_ques(pagesource,keyword):
    ques = pd.DataFrame(columns=['keyword','pos', 'answer', 'search', 'source','question', 'pos_overall', 'url','domain'])
    try:
        data = pagesource
        logging.info("----------questions data--------------------")
        if "people_also_ask" in data.keys():
            related_questions_sr= data['people_also_ask']
            ques = pd.DataFrame(related_questions_sr)
            logging.info(ques.columns)
            logging.info(ques)
            ques.drop('answer_html',axis = 1,inplace = True)
            ques['domain'] = ques['answer_link'].apply(lambda row: tldextract.extract(row).domain)
            ques['keyword'] =keyword
            ques.rename(columns = {'link':'url', 'rank':'pos','description':'desc','global_rank':'pos_overall',
                                    'display_link': 'url_shown','link_title':'title'}, inplace = True)
            return ques[['keyword','pos', 'answer', 'search', 'source','question', 'pos_overall', 'url','domain']]
    except Exception as e:
        logging.info(e,"error in get_rel_ques")
    else :
        return ques