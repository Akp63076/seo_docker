#!/home/django_app/myenv/bin/python
print("file started")
import json
import requests
import pandas as pd
import datetime
import time
import logging
import sys
import os
from concurrent.futures import ThreadPoolExecutor
print(os.getcwd())
os.chdir("/home/django_app/seo/ranking/static/ranking")

# change to keywords of interest
# KEYWORD = "jee main"
# change this to the website of interest

websites = {'collegedunia.com':"CollegeDunia",
             'prepp.in':"Prepp",
              'shiksha.com':"Shiksha",
              'careers360.com':"Careers360",
               'collegedekho.com':"collegedekho",
            'jeemains.in': 'jeemains',
            'mbbsneet.in':'mbbsneet',
           "aglasem.com":"Aglasem",
           "byjus.com":"Byjus",
           "fresherslive.com":"fresherslive",
            "embibe.com":"embibe" ,"leverageedu.com":"leverageedu.com","buddy4study.com":"buddy4study.com"}

output_timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
# print(output_timestamp)
filename = str(sys.argv[1])
print(filename)

date_folder = f"data/{output_timestamp}"
folder_loc = os.path.join("/home/django_app/seo/ranking/static/ranking",date_folder)
print(folder_loc)
try:
    os.mkdir(folder_loc)
    os.mkdir(f"{folder_loc}/result")
    os.mkdir(f"{folder_loc}/modified")    
except FileExistsError as  e :
    pass


path2 =f"{date_folder}/result/{filename}-result.csv"
path3 = f"{date_folder}/modified/{filename}-modified.csv"

keyword_file = pd.read_csv(f"data/input/{filename}.csv",encoding='unicode_escape')

keywords=keyword_file['Keyword'].tolist()

rank_df=pd.DataFrame(columns=('Keyword,Rank,Website,Date,URL').split(','))

def get_job_id(keyword):
    headers = {'Content-Type': 'application/json'}
    job_params = {
        'q': keyword,
        'num':100,
        'parse':True,
        'device':'desktop_chrome',
        'geo':'India',
        'scraper': 'google_search',
    }
    
    response = requests.post(
        'https://api.serpmaster.com/cb',
        headers=headers,
        json=job_params,
        auth=('nishit', 'r6BEJudux75')
    )
    # // Print the response body
    # print(response.json())
    cb_json = response.json()
    job_id= cb_json['id']
    print(job_id)
    return job_id

def get_response(job_id):
    google_search = requests.get(
        f'https://api.serpmaster.com/cb/{job_id}/results',
        auth=('nishit', 'r6BEJudux75'))
    
    google_search_json = google_search.json()
    return google_search_json


def get_rank(pagesource, keyword, WEBSITE):

    temp_df = pd.DataFrame(columns=("Keyword,Rank,Website,Date,URL").split(","))
    data = pagesource['results'][0]['content']['results']
    organic_sr= data['organic']
    if len(organic_sr)!=0:

        for result in organic_sr:
            link = result["url"]
            # description  =result['description']
            now = datetime.date.today().strftime("%d-%m-%Y")
            rank = result['pos']
            # print(link)
            if rank == 1:
                print(rank)
                data = {
                    "Keyword": keyword,
                    "URL": link,
                    "Rank": rank,
                    "Date": now,
                    "Website": "TOP SITE",
                }
                temp_df = temp_df.append(data, ignore_index=True)

            for web in WEBSITE:

                if web in link:
                    print(web)
                    print("Found website at rank: " + str(rank))
                    found_in_results = True
                    # data= {'Keyword': keyword,'title':title,'URL':link,'description':description,'Rank':rank}
                    data = {
                        "Keyword": keyword,
                        "URL": link,
                        "Rank": rank,
                        "Date": now,
                        "Website": web,
                    }
                    temp_df = temp_df.append(data, ignore_index=True)
                    # print(temp_df)
    else:
        print("in function get response : empty page resource")

    return temp_df                 
                    
def new_format_gen(rank_df):
    df=rank_df.copy()

    final = pd.DataFrame(columns=["Keyword", "Rank", "Website", "Date", "URL"]) 
    final = final.set_index('Keyword')
    on_top = df[df['Rank']==1]   

    df=df.drop(['Date','Website'],1)

    final = final.join(on_top.set_index('Keyword'),on="Keyword",how ="outer",rsuffix="_top") 

    for c,i in websites.items():
        temp_df = df[df['URL'].str.contains(c)]

        
        final = final.join(temp_df.set_index('Keyword'),on="Keyword",rsuffix="_"+c,how ="outer")
    final = final.dropna(how='all',axis=1)
    final_copy = final.drop_duplicates()

    return final_copy


def save_df(rank_df):
    try: 
        print("save_df")
        rank_df = rank_df[['Keyword', 'Rank', 'Website', 'Date', 'URL']]
        mod = new_format_gen(rank_df)    
        print('mod_file_created')
        rank_df = rank_df.set_index('Keyword')
        result =  pd.merge(rank_df,keyword_file.set_index('Keyword'),on='Keyword')
        mod_file = pd.merge(mod,keyword_file.set_index('Keyword'),on='Keyword')
        result.to_csv(path2)
        mod_file.to_csv(path3)
    except Exception as e:
        print("error in saving file")
        logging.info(e,"there is an error in save_df")
       

def run_processs_api(keyword):
    """
    Parameters
    ----------
    keyword : string
        keyword of which rank need to be scraped.       
        this funtion calls rapidApi, and scrpe serp page
    Returns
    -------
    temp_df : DataFrame
        this data frame will contain keyword,url and postion in which our and our competitors 
        are on google serp page.

    """

    job_id = get_job_id(keyword)
    print("job id:",job_id)
    time.sleep(10)
    google_search_json = get_response(job_id)
    temp_df = pd.DataFrame(columns=["Keyword","Rank","Website","Date","URL"])
    count = 0
    while count<10:
        try :
            status_code = google_search_json['results'][0]['status_code']                
            print(status_code)
            if status_code == 200:
                print(status_code)
                temp_df = get_rank(google_search_json,keyword,websites)
                print("temp_df done ")
                return temp_df
            else :
                print("status not 200")
                time.sleep(10)
                google_search_json = get_response(job_id)
                print("retrying {0} {1}".format(keyword,count))
                count += 1

        except Exceptions as e:
            count += 1
            print("retrying {0} {1}".format(keyword,count))
            print(e)
    return temp_df

def run_process(keyword):
    global rank_df       
    try :     
        temp_df = run_processs_api(keyword)
        print("run_processs_api_process",keyword)            
        # print("--------------keyword---temp--------------------")
        if temp_df.shape[0]>0:
            print("df not empty")           
            rank_df  = rank_df.append(temp_df,ignore_index=True)
            save_df(rank_df)
            print("saved successfully")
            logging.info("keyword got"+str(temp_df.size)+"lines")
            return 1
        else:
            print("there is an error in check_df")
            logging.info("there is an error in check_df")
    except Exception as e:
        logging.info("in exceptions",e)
        print("error in function run_process : ",keyword)
    return 0 
    


def concurrent_func(keywords):
    futures = []
    with ThreadPoolExecutor(max_workers=20) as executor:
        print(executor)
        total_length = len(keywords)
        start_time = time.time()
        failed_keywords= []
        for i in range(0,total_length):          
                    
            try:
                print(i,keywords[i])
                status = run_process(keywords[i])
                print(status)
                if status == 0 :
                    failed_keywords.append(keywords[i])
            except Exception as e:
                print(e)
                logging.info("in exceptions",e) 
        end = time.time()
        print(f"Runtime of the program is {end - start_time}") 
    return failed_keywords
  
if __name__=="__main__":    
    
    start_time = time.time()
        
    #add filepath which neeeds to be read and scrawled
    
    new_keywords = concurrent_func(keywords)  
    print(new_keywords)
    for i in range(10):
        if len(new_keywords) !=0:
            new_keywords = concurrent_func(new_keywords)
    
    # end time
    end = time.time()
    print(f"Runtime of the program is {end - start_time}")   
    
#references 
#https://docs.serpmaster.com/docs/quick-start-guide