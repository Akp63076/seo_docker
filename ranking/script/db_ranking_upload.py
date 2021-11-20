import pandas as pd
import os
import glob

import psycopg2
from config import config

import pandas as pd 

base_dir = os.getcwd()
data_rel_path = "/ranking/static/ranking/data"
com_path = os.path.join(base_dir+data_rel_path)
# print(com_path) 
dir_list = os.listdir(com_path)
# print(dir_list)

start_letter = '20'
with_20 = [x for x in dir_list if x.startswith(start_letter)]
# print(with_20)
def check_combinecsv(all_filenames):
    for file in all_filenames:
        if "combined_csv_" in file:
            return True
    return False


for x in with_20:
    path = com_path+"/"+x
    dir_list = [f for f in os.listdir(path) if not f.startswith('.')]
    for d in dir_list:
        # print(d)
        
        all_filenames = [f for f in os.listdir(os.path.join(path,d)) if not f.startswith('.')]
        # print(all_filenames)
        filename = f"/combined_csv_{d}.csv"
        if not check_combinecsv(all_filenames):
            print("check combine:",x)
            
            combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
            combined_csv.to_csv( path+filename, index=False)



