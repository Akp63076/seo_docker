
from celery.utils.log import get_task_logger
from django.conf import settings
from django.core.mail import EmailMessage,send_mail
from django.core import mail
from rank_tool.models import upload
import random
import os
import datetime
import pandas as pd   
from time import sleep
from celery import  shared_task
from cd_ranking.scrapers import testing_brightdata
import json



logger = get_task_logger(__name__)



def new_format(rank_df):
    df=rank_df.copy()
    on_top = df[df['Rank']=='1']   
    df=df.drop(['Date','Website'],1)
    careers360 = df[df['URL'].str.contains('careers360.com')]
    careers360.columns = ['Keyword','Careers360 Rank','Careers360 URL']
    shiksha = df[df['URL'].str.contains('shiksha.com')]
    shiksha.columns = ['Keyword', 'Shiksha Rank', 'Shiksha URL']
    collegedunia = df[df['URL'].str.contains('collegedunia')]
    collegedunia.columns  = ['Keyword','CollegeDunia Rank','CollegeDunia URL']
    collegedekho = df[df['URL'].str.contains('collegedekho')]
    collegedekho.columns  = ['Keyword','collegedekho Rank','collegedekho URL']
    dfs = [on_top,collegedunia,shiksha,careers360,collegedekho]
    dfs = [df.set_index('Keyword') for df in dfs]
    final = dfs[0].join(dfs[1:])
    final_copy = final.drop_duplicates()
    final_copy=final_copy[['Rank', 'URL', 'Date', 'Website', 
                          'CollegeDunia Rank','Shiksha Rank','Careers360 Rank','collegedekho Rank',
                          'CollegeDunia URL', 'Shiksha URL',  'Careers360 URL','collegedekho URL']]
    final_copy.columns=['Rank', 'Top URL', 'Date', 'Website', 
                         'CollegeDunia Rank','Shiksha Rank','Careers360 Rank','collegedekho Rank',
                        'CollegeDunia URL', 'Shiksha URL',  'Careers360 URL','collegedekho URL']
    
    return final_copy    


@ shared_task(name="send_feedback_email_task")
def send_feedback_email_task(fileid):
    """sends an email when ranking is done successfully"""
    # print(fileid)
    fileobject=upload.objects.get(id=fileid)
    if(fileobject.status!="In Queue"):
        return 0
    print("In send feedback ",fileobject.file.name)
    fileobject.status="In Progress"
    fileobject.save()
    # print(fileobject.file_name)
    file_path=fileobject.file.name.split("/")
    file_path=file_path[1]+"/"+file_path[2]
    recipient_email=fileobject.email
    file_name=fileobject.file_name
    # # print(fileobject.email)
    # #PROXY = '127.0.0.1:24010'
    # chrome_options = webdriver.ChromeOptions()
    # #chrome_options.add_argument('--proxy-server=%s' % PROXY)
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--no-sandbox") 
    # chrome_options.add_argument('--allow-running-insecure-content')
    # chrome_options.add_argument('--ignore-certificate-errors')
    # chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
    path = os.getcwd()+'/uploads/'+file_path    
    df=pd.read_csv(path,encoding='unicode_escape')
    user_path=file_path.split("/")[0]
    unique_file_path=file_path.split("/")[1]
    path2 = os.getcwd()+'/uploads/results/'+user_path
    try:
        os.makedirs(path2)
    except FileExistsError:
        print("path already exists {0}".format(path2))
    
    path2 = os.getcwd()+'/uploads/results/'+user_path+'/rank_'+unique_file_path
    
    
    path3 = os.getcwd()+'/uploads/mod_results/'+user_path
    try:
        
        os.makedirs(path3)
    except FileExistsError:
        print("path already exists {0}".format(path3))
    path3 =os.getcwd()+'/uploads/mod_results/'+user_path+'/modified_'+unique_file_path

    keywords=df[df.columns[0]].tolist()
    websites={'collegedunia.com':"CollegeDunia",
             'prepp':"Prepp",
              'shiksha.com':"Shiksha",
              'careers360.com':"Careers360",
               'collegedekho.com':"collegedekho",
                'jeemains.in': 'jeemains',
                 'mbbsneet.in':'mbbsneet' }
    rank_df=pd.DataFrame(columns=('Keyword,Rank,Website,Date,URL').split(','))
    fileobject.result='results/'+user_path+'/rank_'+unique_file_path
    fileobject.result_mod='mod_results/'+user_path+'/modified_'+unique_file_path
    keywords=df[df.columns[0]].tolist()
    total_length=len(keywords)
    current=0
    fileobject.total=total_length
    fileobject.current=current
    fileobject.save()

    def rank(keyword):
        temp_df=pd.DataFrame(columns=('Keyword,Rank,Website,Date,URL').split(','))   
        google_search = testing_brightdata.get_response(keyword,'a','b')
        status_code = google_search.getcode()
        print(status_code)
        if status_code == 200:
                response = google_search.read().decode('utf-8')
                google_search_json = json.loads(response)                
                temp_df = testing_brightdata.get_rank(google_search_json,keyword,websites)
                logger.error(status_code)
        
        temp_df=temp_df[['keyword','pos','domain','date','url']].rename(columns={'keyword':'Keyword','pos':'Rank','domain':'Website','date':'Date','url':'URL'})
        print(temp_df)
        return(temp_df)

    for i in range(0,total_length):
        ty = 0
        #print(keywords[i])
        while ty<20:
            try:
                sleep(random.randint(1,3))
                temp_df = rank(keywords[i])
                if(temp_df.size==0):
                    sleep(random.randint(10,15))
                    raise Exception("Got Empty DataFrame",keywords[i],ty,)
                    
                rank_df=rank_df.append(temp_df,ignore_index=True)
                ty=20
                print(keywords[i]+"       keyword got"+str(temp_df.size)+"lines")
                sleep(random.randint(7,15))

            except Exception as e:
                print("in exceptions",e)
                ty += 1
        fileobject.current= int(i+1)
        fileobject.save()
        div=int(total_length/50)+1
        if (i%div==0):
            rank_df.to_csv(path2)
        if (i%101 == 100):
            sleep(5)
        if (i%501 == 500):
            sleep(20)
        if (i%1001 == 1000):
            sleep(100)

    rank_df.to_csv(path2)
    new_format(rank_df).to_csv(path3)
    fileobject.status="Complete"
    fileobject.time_complete=datetime.datetime.now()
    fileobject.save()
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [recipient_email]
    recipient_list.append('datateam.main@gmail.com') 
    print("sending email")
    email = EmailMessage("Google Rank Report","PFA Your File "+file_name,email_from,recipient_list)
    email.attach_file(path)
    email.attach_file(path2)
    email.attach_file(path3)
    print("file attached")
    email.send()
    fileobject.status="Email Sent"
    fileobject.save()

    print("email sent to",recipient_list)
