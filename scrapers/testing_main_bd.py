import os
from re import X
os.chdir("/home/data/uploads")
import datetime
import sys
from time import sleep,time
import random
import pandas as pd 
import logging
import csv
import testing_scraper_for_bd
import testing_sheetupdation
import multiprocessing

import logging

output_timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

logging.basicConfig( filename=f'/home/data/uploads/log/process-{output_timestamp}.log',
                    format='%(asctime)s %(levelname)s %(threadName)-10s %(message)s',
                     level=logging.INFO)
logger = logging.getLogger(__name__)

#Taking desired folder names from user and creating folder using the timestamp
folder = str(sys.argv[1])
sub_folder = str(sys.argv[2])

print(sub_folder)
project_path= os.getcwd()
filepath = os.path.join(project_path,folder,sub_folder)

def status_file(path_of_file,status):
    if status == 'Running':
        with open(path_of_file, 'w') as f:
            f.write(status)
    elif status == 'Completed':
        with open(path_of_file, 'w') as f:
            f.write(status)

try :
    os.makedirs(os.path.join(filepath,output_timestamp))
except Exception as e:
    logging.info(e)

filenames = ["data.csv",
            f"result_{output_timestamp}.csv",
            f"modified_{output_timestamp}.csv",
            f"featured_snippet_{output_timestamp}.csv",
            f"related_searches_{output_timestamp}.csv",
            f"related_questions_{output_timestamp}.csv",
            "response.csv",
            "status.txt"]

new_path = os.path.join(filepath,output_timestamp)
path = os.path.join(new_path,filenames[0])
path2 = os.path.join(new_path,filenames[1])
path3 = os.path.join(new_path,filenames[2])
path4 = os.path.join(new_path,filenames[3])
path5 = os.path.join(new_path,filenames[4])
path6 = os.path.join(new_path,filenames[5])
path7 = os.path.join(new_path,filenames[6])
path8 = os.path.join(new_path,filenames[7])

testing_sheetupdation.updateDir(folder,sub_folder,output_timestamp,path)
status_file(path8,'Running')

keyword_file=pd.read_csv(path,encoding='utf-8-sig')

keyword_file.columns = keyword_file.columns.str.lower()
req_col = [x for x in keyword_file.columns if 'keyword' in x]
keyword_file.rename(columns = {req_col[0]:"keyword"},inplace = True)
keyword_file.drop_duplicates(inplace=True)

keywords=keyword_file[keyword_file.columns[0]].tolist()

print(keywords)

rank_df=pd.DataFrame(columns=['keyword','pos', 'url', 'desc', 'title',
                            'url_shown', 'pos_overall', 'domain','date'],)
feature_df =  pd.DataFrame(columns=['keyword','url', 'desc', 'title', 
                                    'url_shown', 'pos_overall', 'domain'])
related_searches_df = pd.DataFrame(columns=[ 'keyword','rel_searches'])
related_questions_df = pd.DataFrame(columns=['keyword','pos', 'answer', 'search',
                                            'source', 'question', 'pos_overall', 'url','domain'])
response_df = pd.DataFrame(columns=['keyword','response','try'])

rank_df.to_csv(path2,index = False)
feature_df.to_csv(path4,index = False)
related_searches_df.to_csv(path5,index = False)
related_questions_df.to_csv(path6,index = False)
response_df.to_csv(path7,index = False)

def add_row(temp_df,keyword):
    global rank_df 
    rank_df = pd.concat([rank_df,temp_df],ignore_index=True)
    return rank_df

def save_df(df,path_to_save):
    try: 
        logging.info("------------------------")
        df = df.set_index('keyword')
        # df =  pd.merge(df,keyword_file.set_index('keyword'),on='keyword')
        df.to_csv(path_to_save,mode = 'a',header = False)
    except Exception as e:
        logging.info(e,"there is an error in save_df")
        logging.info({output_timestamp},"- there is an error in save_df")

def createmod_file():
    global path2,path3
    global keyword_file
    global mod_file
    global mod_feature_df
    global related_questions_df
    global related_searches_df
    global rank_df
    global response_df
    
    rank_df1 = pd.read_csv(path2,encoding='utf-8-sig',usecols = ['keyword','pos', 'url', 'desc', 'title','url_shown', 'pos_overall', 'domain','date'])
    rank_df1.drop_duplicates(inplace=True)
    
    mod = testing_scraper_for_bd.new_format_gen(rank_df1)
        
    print('mod_file_created')
    rank_df1 = rank_df1.set_index('keyword')
    result =  pd.merge(rank_df1,keyword_file.set_index('keyword'),on='keyword')
    mod_file = pd.merge(mod,keyword_file.set_index('keyword'),on='keyword')
    mod_feature_df = feature_df[['keyword','url', 'desc', 'title', 
                'pos_overall', 'domain']]
    mod_feature_df.columns=['keyword','featured_url', 'featured_desc', 
                    'featured_title', 'featured_pos_overall', 
                    'featured_domain']    
    mod_file = pd.merge(mod_file,mod_feature_df.set_index('keyword'),on='keyword',how="outer")
    mod_file.to_csv(path3)

def run_process(keyword):
    global path2, path3, path4, path5, path6, path7, path8
    global rank_df
    global feature_df
    global related_searches_df
    global related_questions_df
    global response_df
    global folder
    global sub_folder

    try:     
        context_dict = testing_scraper_for_bd.run_processs_api(keyword,folder,sub_folder)
        print("run_processs_api_process",keyword)
        logging.info(f'run_processs_api_process for {keyword}')
        
        if context_dict['success']==1:

            for key in context_dict.keys():
                if key not in ['success']:
                    print(key)
                    if context_dict[key] is  None:
                        print(key,1)
                        context_dict[key] = pd.DataFrame()

            if context_dict['temp_df'].shape[0]>0:
                rank_df = add_row(context_dict['temp_df'],keyword)
                print(rank_df)
                logging.info("{0} got {1} lines".format(keyword,context_dict['temp_df'].shape[0]))
                save_df(context_dict['temp_df'],path2)
                print("df saved")
            else:
                print("temp df has 0 shape")

            if context_dict['ft_temp'].shape[0]>0:
                feature_df = pd.concat([feature_df,context_dict['ft_temp']],ignore_index=True)
                logging.info("{0} got {1} lines for featured snippet".format(keyword,context_dict['ft_temp'].shape[0]))
                print(feature_df)
                save_df(context_dict['ft_temp'],path4)
            else:
                print("ft_temp has 0 shape")

            if context_dict['sr_temp'].shape[0]>0:
                related_searches_df = pd.concat([related_searches_df,context_dict['sr_temp']],ignore_index=True)
                print(related_searches_df)
                save_df(context_dict['sr_temp'],path5)
                logging.info("{0} got {1} lines for related searches".format(keyword,context_dict['sr_temp'].shape[0]))
            else:
                print("sr_temp has 0 shape")

            if context_dict['ques'].shape[0]>0: 
                related_questions_df = pd.concat([related_questions_df,context_dict['ques']],ignore_index=True)
                save_df(context_dict['ques'],path6)
                logging.info("{0} got {1} lines".format(keyword,context_dict['ques'].shape[0]))
            else:
                logging.info("ques has 0 shape")

            if context_dict['response'].shape[0]>0: 
                response_df = pd.concat([response_df,context_dict['response']],ignore_index=True)
                save_df(context_dict['response'],path7)
                logging.info("{0} got {1} lines".format(keyword,context_dict['ques'].shape[0]))
            else:
                logging.info("response has 0 shape")
        elif context_dict['success']==0:
            if context_dict['response'].shape[0]>0:
                response_df = pd.concat([response_df,context_dict['response']],ignore_index=True)
                save_df(context_dict['response'],path7)
                logging.info("{0} got {1} lines".format(keyword,context_dict['ques'].shape[0]))
            else:
                logging.info("response has 0 shape")
    except Exception as e:
        print("error in run process api")
        logging.info(f"{keyword} in exceptions : {e}")

def concurrent_func(total_length,keywords):
    for i in range(0,total_length):          
        print(i)           
        try:
            sleep(random.randint(1,3))
            run_process(keywords[i])
        except Exception as e:
            print("error in concurrent function")
            logging.info("in exceptions",e)

def split(a, n):
    k, m = divmod(len(a), n)
    return (a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n))

if __name__=="__main__":
    start_time = time()
    total_length = len(keywords)
    
    keywords_split = split(keywords, 4)
    for_pool = [(len(i),i) for i in keywords_split]

    pool = multiprocessing.Pool(4)

    pool.starmap(func=concurrent_func, iterable=for_pool)

    pool.close()

    # concurrent_func(total_length,keywords)
    createmod_file()
    filenames = ["data.csv",
            f"modified_{output_timestamp}.csv",
            f"featured_snippet_{output_timestamp}.csv",
            ]
    
    status_file(path8,'Completed')
    testing_scraper_for_bd.send_mail(new_path,filenames,folder,sub_folder)   
    end_time = time()
    logging.info('send mail')
    elapsed_time = end_time - start_time
    logging.info(f"Elapsed run time: {elapsed_time} seconds")