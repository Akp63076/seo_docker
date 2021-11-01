
import json
import requests
import pandas as pd
import datetime
import time
import logging
import sys
import os

from concurrent.futures import ThreadPoolExecutor

# os.chdir("/home/django_app/seo/ranking/")
os.chdir(os.getcwd())
# change this
ACCESS_KEY = "d98dff95c6mshbdce2aebd6a6bd5p13b64ejsn38873cb010b6"
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

output_timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H")
# print(output_timestamp)
filename = str(sys.argv[1])
print(filename)

date_folder = f"data/{output_timestamp}"
try:
    os.mkdir(date_folder)
    os.mkdir(f"{date_folder}/result")
    os.mkdir(f"{date_folder}/modified")
    
except FileExistsError as  e :
    pass

path2 =f"{date_folder}/result/{filename}-result.csv"
path3 = f"{date_folder}/modified/{filename}-modified.csv"

keyword_file = pd.read_csv(f"data/input/{filename}.csv",encoding='unicode_escape')

keywords=keyword_file['Keyword'].tolist()

def get_url(KEYWORD):

    country = "IN"
    language = "lang_en"
    
    data = {
    "q" : KEYWORD,
    "country" : country,
    "language" : language,
    "num": 100
    }

    url = "https://google-search3.p.rapidapi.com/api/v1/search/q="+data.get("q")+"&country="+data.get("country")+"&language="+data.get("language")+"&gl=IN&num=100&uule=w+CAIQICIFSU5ESUE"
    return url

def get_response(url):

    headers = {
    'x-rapidapi-key': "d98dff95c6mshbdce2aebd6a6bd5p13b64ejsn38873cb010b6",
    'x-rapidapi-host': "google-search3.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers)
    content = response.text
    results = json.loads(content)
    return results

def get_rank(pagesource,keyword,WEBSITE):
    
    temp_df=pd.DataFrame(columns=('Keyword,Rank,Website,Date,URL').split(','))
    found_in_results = False # keep track if we found the website
    
    if pagesource['results']:
    
        for rank, result in enumerate(pagesource['results'],start=1):
           
            # title = result['title']
    
            link = result['link']
          
            # description  =result['description']
            now = datetime.date.today().strftime("%d-%m-%Y")
            rank = str(rank)
            # print(link)
            if rank == '1':
                print(rank)
                data= {'Keyword': keyword,'URL':link,'Rank':rank,'Date':now,'Website':'TOP SITE'}
                temp_df = temp_df.append(data,ignore_index=True)
             
    
            for web in WEBSITE:
    
                if web in link:
                    # print(web)
                    # print("Found website at rank: " + str(rank))
                    found_in_results = True
                    # data= {'Keyword': keyword,'title':title,'URL':link,'description':description,'Rank':rank}
                    data= {'Keyword': keyword,'URL':link,'Rank':rank,'Date':now,'Website':web}
                    temp_df = temp_df.append(data,ignore_index=True)
                    
    else :
        print("empty page resource")                    
                    

    return temp_df
    
def check_df(size,keyword,i):
    try :

        if(size==0):
            logging.info("Got Empty DataFrame",keyword,i)
            raise Exception("Got Empty DataFrame",keyword,i)            
        else :
            return True
    except Exception as e:
        print(e)
        print("error in check df")
        return False     
        
rank_df=pd.DataFrame(columns=('Keyword,Rank,Website,Date,URL').split(','))


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
    url = get_url(keyword)
    print(url)
    results = get_response(url)
    print("result_done")
    temp_df = get_rank(results,keyword,websites)
    print("temp_df done ")
    return temp_df    
    
    
    
def run_process(keyword):
    global rank_df
    # print(id(rank_df))
    ty=0
    while ty<=20:      
        try :     
            temp_df = run_processs_api(keyword)
            print("run_processs_api_process",ty,keyword)            
            # print("--------------keyword---temp--------------------")
            if check_df(temp_df.size,keyword,ty):
                print("df not empty")
                ty = 20
                rank_df  = rank_df.append(temp_df,ignore_index=True)
                save_df(rank_df)
                print("saved successfully")
                logging.info("keyword got"+str(temp_df.size)+"lines")
                return 1
            else:
                print("there is an error in check_df")
                logging.info("there is an error in check_df")
                ty += 1

        except Exception as e:

            logging.info("in exceptions",e)
            print("error : ",keyword,"attempt:",ty)
            ty += 1


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
    
