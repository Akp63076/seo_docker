import os
import datetime
from time import sleep
import time
import pandas as pd
import logging
import testing_brightdata
import json

import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE,formatdate
from email import encoders
from email.mime.base import MIMEBase

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
            "ielts-mentor",
            "mini-ielts",
            "ieltsadvantage",
            "ieltsbuddy",
            "ieltsmaterial",
            "mastersportal",
            "yocket",
            "usnews",
            "topuniversities",
            'collegepravesh',
            "zoutons"
            ]

import logging
output_timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H")
logger = logging.getLogger(__name__)
rank_df=pd.DataFrame(columns=('Keyword,Rank,Website,Date,URL').split(','))

def run_processs_api(keyword,folder,sub_folder):
    """
    Parameters
    ----------
    keyword : string
        keyword of which rank need to be scraped.
    
    this funtion calls rapidApi, and scrpe serp page

    Returns
    -------
    context : dictionary with different dfs and success of the code

    """
    print("run_processs_api fuction started")
    count = 1
    temp_response_df = pd.DataFrame(columns = 'keyword,response,try'.split(','))  
    while count<10:
        try :
            google_search = testing_brightdata.get_response(keyword,folder,sub_folder)
            status_code = google_search.getcode()
            print(status_code)
            temp_response_data = {'keyword': keyword,'response':status_code,'try':count}
            temp_response_df = pd.concat([temp_response_df,pd.DataFrame.from_records([temp_response_data])],ignore_index=True)
            if status_code == 200:
                api_end_time = datetime.datetime.now()
                response = google_search.read().decode('utf-8')
                google_search_json = json.loads(response)
                logging.info(status_code)
                temp_df = testing_brightdata.get_rank(google_search_json,keyword,websites)
                ft_temp = testing_brightdata.get_snippet(google_search_json,keyword)
                sr_temp = testing_brightdata.get_rel_searches(google_search_json,keyword)
                ques  = testing_brightdata.get_rel_ques(google_search_json,keyword)
                df_collection = {"success":1,
                                "temp_df":temp_df,
                                "ft_temp":ft_temp,
                                "sr_temp":sr_temp,
                                "ques":ques,
                                "response":temp_response_df}
                return df_collection
            else :
                logging.info("status not 200")
                time.sleep(10)
                logging.info("retrying {0} {1}".format(keyword,count))
                count += 1
        except Exception as e:
            temp_response_data = {'keyword': keyword,'response':'error','try':count}
            temp_response_df = pd.concat([temp_response_df,pd.DataFrame.from_records([temp_response_data])],ignore_index=True)
            count += 1
            logging.info("retrying {0} {1}".format(keyword,count))
            logging.info(e, "error in run process api")
    return {"success":0,"response":temp_response_df}

def new_format_gen(rank_df):
    global websites 

    df=rank_df.copy()
    final = pd.DataFrame(columns=['keyword']) 
    final = final.set_index('keyword')
    on_top = df[df['pos']==1]   

    df=df.drop(columns = ['date','domain','url_shown'])

    final = final.join(on_top.set_index('keyword'),on="keyword",how ="outer",rsuffix="_top") 

    for c in websites:
        temp_df = df[df['url'].str.contains(c)]
        final = final.join(temp_df.set_index('keyword'),on="keyword",rsuffix="_"+c,how ="outer")
    final = final.dropna(how='all',axis=1)
    final_copy = final.drop_duplicates()

    return final_copy

def send_mail(path,filenames,folder,freq):
    os.chdir(path)
    subject = "Rank-data"
    attachment = " ".join(filenames)
    body = f"{attachment} are attached of {freq} data of {folder}"
    smtp_server = "smtp.gmail.com"
    port = 587  # For SSL
    sender_email = "binoy.p@collegedunia.com"
    password = "CD2340@Binoy"
    if folder == "zollege":
        receiver_email = ['rohini.mishra@collegedunia.com',
                            'binoy.p@collegedunia.com',
                            ]
    elif folder == 'left':
        if freq == "additional":
            receiver_email = ['binoy.p@collegedunia.com','rohini.mishra@collegedunia.com','deepika.kunwar@collegedunia.com',\
                            'nishit.kumar@collegedunia.com']
        else:
            receiver_email = ['binoy.p@collegedunia.com','aashish.pandey@collegedunia.com']
    elif folder == "zoutons":
        receiver_email = ['binoy.p@collegedunia.com','rohini.mishra@collegedunia.com',\
                            'nishit.kumar@collegedunia.com','krati.rathore@collegedunia.com']
    else:
        receiver_email = ['binoy.p@collegedunia.com','rohini.mishra@collegedunia.com','deepika.kunwar@collegedunia.com',\
                            'nishit.kumar@collegedunia.com']

    message = MIMEMultipart("alternative")
    message["Subject"] = "Google Ranking of Keywords"
    message["From"] = sender_email
    message["To"] = COMMASPACE.join(receiver_email)

    message.attach(MIMEText(body, "plain"))

    for file in filenames:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(open(file,"rb").read())
        encoders.encode_base64(part)
        part.add_header(
        "Content-Disposition",
        f"attachment; filename= {file}",)
        message.attach(part)
        text = message.as_string()
    context = ssl.create_default_context()

    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)
        logging.info('send mail')
        print("send mail")  