import datetime
import glob
import os

import numpy as np
import pandas as pd
import psycopg2

from config import config
from database_connector import connect

base_dir = os.getcwd()
data_rel_path = "/ranking/static/ranking/data"
com_path = os.path.join(base_dir+data_rel_path)
# print(com_path) 
dir_list = os.listdir(com_path)
# print(dir_list)

output_timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
current_data = datetime.datetime.now().strftime("%Y-%m-%d")
start_letter = f'{output_timestamp}'
# start_letter = "2021"
print(start_letter)
with_20 = [x for x in dir_list if x.startswith(start_letter)]
# print(with_20)

def check_combinecsv(all_filenames):
    for file in all_filenames:
        if "combined_csv_" in file:
            return True
    return False

def combine_csv(path,d):
    all_filenames = [f for f in os.listdir(os.path.join(path,d)) if (not f.startswith('.')) if (not f.startswith('combined_csv')) ]
    filename = f"combined_csv_{d}-{current_data}.csv"
    filepath = os.path.join(path,d,filename)
    if not check_combinecsv(all_filenames):
        
        combined_csv = pd.concat([pd.read_csv(os.path.join(path,d,f),engine ='python',encoding= 'unicode_escape') for f in all_filenames ])
        combined_csv.to_csv( filepath, index=False)


def get_status():
    try :
        status_df = pd.read_csv('ranking/script/status.csv')
        return status_df.loc[0,'lastindex']
        
    except Exception as e:
        status_df = pd.DataFrame(columns=['lastindex'])
        status_df.loc[0,'lastindex'] = 0
        status_df.to_csv('ranking/script/status.csv',index=False)

        return 0

def update_status(shape):
        status_df = pd.read_csv('ranking/script/status.csv')
        print(status_df.loc[0,'lastindex'])
        print(shape)
        status_df.loc[0,'lastindex'] = status_df.loc[0,'lastindex']+shape
        status_df.to_csv('ranking/script/status.csv',index=False)
    
def upload_csv(filepath):
    print("in upload csv")
    
    status_num = get_status()

    get_id = pd.read_csv('ranking/script/data-export.csv',encoding= 'unicode_escape')

    temp_df = pd.read_csv(filepath,encoding= 'unicode_escape')
    temp_df = temp_df.rename(columns={'Keyword':'keyword','Rank':'rank','Date':'date','Website':'domain','URL':'url'})
    
    merged_df = get_id.merge(temp_df,on = 'keyword')
    merged_df = merged_df[['rank','date','domain','url','id']]
    merged_df.rename(columns={'id':'keyword_id'},inplace=True)
    merged_df.index = np.arange(status_num, len(merged_df)+status_num)
    # print(merged_df.head())
    table = "ranking_googleserp"
    update_status(merged_df.shape[0])
    merged_df.to_csv("ranking/script/data-merged.csv", header=False,sep='|')
    connect(merged_df,table)

for x in with_20:
    path = com_path+"/"+x
    dir_list = [f for f in os.listdir(path) if not f.startswith('.')]
    for d in dir_list:
        print(d)
        combine_csv(path,d)

        filename = f"combined_csv_{d}-{current_data}.csv"
        filepath = os.path.join(path,d,filename)
        #will combine all csv to 1
        if d == 'result':
            upload_csv(filepath)

       





