# Create your tasks here
import ast
from cmath import nan
from glob import glob
import os
from django.utils import timezone
import shutil
from datetime import datetime
from asyncio import exceptions
from time import sleep
import pandas as pd
import sqlalchemy
from celery import shared_task
import logging

#from macpath import join

logger = logging.getLogger("django")
pd.options.mode.chained_assignment = None


@shared_task()
def database_update(input_path, output_path): 
    """ This function  is used for update to database by  csv files and insert record on all tables 
    it takes 2 arguments 
    input_path= data directry path , output_path=destination directory path after updation of database """   
    input_path = input_path+"/"
   
    conn = sqlalchemy.create_engine(
        "postgresql://{user}:{pw}@localhost/{db}".format(user="analyst", pw="12345", db="postgres"))
    try:
        for brand in os.listdir(input_path):
            if brand in ['collegedunia','left']:
                for time_period in os.listdir(os.path.join(input_path,brand)):                    
                    if time_period.startswith('monthly'):
                        frequency='monthly'
                    elif time_period.startswith('weekly'):
                        frequency='weekly'
                    elif time_period.startswith('daily'):
                        frequency='daily'
                    elif time_period.startswith('additional'):
                        frequency='temporary'
                    if frequency in ['daily','weekly','monthly']:
                        for today_files in os.listdir(os.path.join(input_path,brand,time_period)):
                            rel_path = os.path.join(input_path,brand,time_period,today_files)
                            print(rel_path)
                            if glob(rel_path+"/status.txt"):
                                with open(rel_path+"/status.txt", 'r') as f:
                                        state=f.read()
                                if state=="Completed":
                                    if glob(rel_path+"/result*.csv"):
                                        update_keyword_table(glob(rel_path+"/data*.csv")[0],conn)
                                        update_keyword_frequency_table(glob(rel_path+"/data*.csv")[0],conn,frequency)
                                        update_tag_table(glob(rel_path+"/data*.csv")[0],conn)
                                        update_domain_table('/home/ranking_data/domain.csv', conn)

                                        update_description_table(glob(rel_path+"/result*.csv")[0], conn,frequency)

                                        # update_question_table(glob(rel_path+"/result*.csv")[0],conn)

                                        # update_sitelink_table(glob(rel_path+"/result*.csv")[0],conn)

                                    # if glob(rel_path+"/related_searches*.csv"):
                                        # update_rel_search_table(glob(rel_path+"/related_searches*.csv")[0],conn)

                                        # update_rel_question_table(glob(rel_path+"/related_question*.csv")[0],conn)

                                    print("data uploaded successfully for " + today_files)
                                    shutil.move(os.path.join(input_path,brand,time_period,today_files),os.path.join(output_path,brand,time_period,today_files))
                            
    except Exception as e:
        logger.error(e)
    else:
        return "database update successfully :) "


def update_keyword_table(path, conn):
    """function is used for updated keyword_table 
    it takes 2 arguments 
    path= csv file path, conn =  database connection string  """
    try:
        
        data=pd.read_csv(path,usecols=['Keyword','search_volume','category',"tracking_url"]  ,on_bad_lines='skip',skipinitialspace = True).drop_duplicates(keep='first')
        data.columns=data.columns.str.lower()        
        df = data[data["keyword"].str.contains("site:https") == False]
        #df = data[data["sv"].str.contains("-") == False]
        df["search_volume"]=df["search_volume"].replace({'-':0,})
        df["search_volume"]=df["search_volume"].fillna(0)
        df['category']=df['category'].str.title()
        df['category']=df['category'].str.strip()
        df["search_volume"]=df.search_volume.str.split(',').str.join('').astype(int,errors='ignore')
        df["category"]=df["category"].replace({nan:'undefined',"":'undefined',None:'undefined' })
        df['search_volume'] = pd.to_numeric(df['search_volume'],errors='ignore')
        if df.empty != True:
            df1=df.assign(with_year=False)
            df1.rename(columns={ "tracking_url": 'req_url'}, inplace=True)
            data_type = {'id': sqlalchemy.Integer, 'keyword': sqlalchemy.String, 'req_url': sqlalchemy.String,
                        'with_year': sqlalchemy.Boolean, 'search_volume': sqlalchemy.Integer, 'category': sqlalchemy.String}
            df1.to_sql('temp_table', conn, if_exists='replace',dtype=data_type)
            sql = """
                UPDATE cd_ranking_keyword_table AS f
                SET search_volume = t.search_volume ,req_url=t.req_url,with_year=t.with_year,category=t.category
                FROM temp_table AS t
                WHERE f.keyword = t.keyword 
            """
      
            conn.execute(sql)
            conn.execute("DROP Table temp_table")
            sleep(1)
            unique_upload(df1, 'cd_ranking_keyword_table',
                        conn, data_type=data_type)
            
    except Exception as e:
        logger.error(e)
 
def update_keyword_frequency_table(path , conn,frequency):
    """function is used for updated frequency_table and mapping keyword with frequency and storing in keyword_frequency_table  
    it takes 3 arguments 
    path= csv file path, conn =  database connection string ,frequency=ranking frequency (daily ,weekly,monthly,temporary) """
    try:

        df = pd.DataFrame()
        df["frequency"]=[frequency]
        if df.empty != True:
           
            data_type = {'domain': sqlalchemy.String}
            unique_upload(df, 'cd_ranking_frequency_table',
                          conn, data_type=data_type)
    except Exception as e:
        logger.error(e)
    try:
        data=pd.read_csv( path ,usecols=['Keyword'] ,on_bad_lines='skip',skipinitialspace = True).drop_duplicates(keep='first')
        data.columns=data.columns.str.lower()
        data['frequency']=frequency
        data1=dict(conn.execute("select frequency, id from cd_ranking_frequency_table ").fetchall())
        data2=dict(conn.execute("select keyword, id from cd_ranking_keyword_table ").fetchall())
        data["frequency"]=data['frequency'].map(data1)
        data["keyword"]=data['keyword'].map(data2)
        df=data.dropna()
        df.rename(columns={'keyword':'keyword_id','frequency':'frequency_id'},inplace=True)
        unique_upload(df,'cd_ranking_keyword_frequency_table',conn)
    except Exception as e:
        logger.error(e)
def update_tag_table(path,conn):
    """function is used for updated to tag in tag_table  and  mapping keyword with tag and storing in keyword_tag_table table 
    it takes 2 arguments 
    path= csv file path, conn =  database connection string  """
    try:
       
        data=pd.read_csv( path ,usecols=['Keyword','tag'] ,on_bad_lines='skip',skipinitialspace = True)
        data.columns=data.columns.str.lower()
        data['tag']=data['tag'].replace({nan:'undefined',"":'undefined',None:'undefined'})
        data['tag']=data['tag'].str.split(',')
        data=data.explode('tag')
        data_type={'tag':sqlalchemy.String}
        data['tag']=data['tag'].str.title()
        data['tag']=data['tag'].str.strip()
        df=data[['tag']].fillna("undefined").drop_duplicates(keep='first')
        unique_upload(df,'cd_ranking_tag_table',conn,data_type=data_type)
    except Exception as e :
            logger.error(e)
    try:
       
        data1=dict(conn.execute("select tag, id from cd_ranking_tag_table ").fetchall())
        data2=dict(conn.execute("select keyword, id from cd_ranking_keyword_table ").fetchall())
        data["tag"]=data['tag'].map(data1)
        data["keyword"]=data['keyword'].map(data2)
        df=data.dropna().drop_duplicates(keep='first')
        df.rename(columns={'keyword':'keyword_id','tag':'tag_id'},inplace=True)
        df.to_sql('temp_table', conn, if_exists='replace',dtype=data_type)
        sql=""" delete from cd_ranking_keyword_tag_table where
         tag_id in (select id from cd_ranking_tag_table where tag='Undefined')
          and keyword_id in (select keyword_id from temp_table)"""
        conn.execute(sql)
        conn.execute("DROP Table temp_table")
        sleep(1)
        unique_upload(df,'cd_ranking_keyword_tag_table',conn)
    except Exception as e :
            logger.error(e)
def update_rel_search_table(path,conn):
    """function is used for updated to  related_search about keyword rel_search_table 
    it takes 2 arguments 
    path= csv file path, conn =  database connection string  """
    try:

        data1 = pd.read_csv(path, on_bad_lines='skip',skipinitialspace = True)[
            ['keyword', 'rel_searches']].dropna().drop_duplicates(keep='first')
        if data1.empty != True:
            data1.rename(columns={'rel_searches': 'rel_search'}, inplace=True)
            data_type = {'keyword': sqlalchemy.String,
                         'req_search': sqlalchemy.String}
            df = data1[['rel_search']]
            unique_upload(df, 'cd_ranking_rel_search_table',
                          conn, data_type=data_type)

            #"""key_rel_search_table udation"""#
            data2 = dict(conn.execute(
                "select rel_search, id from cd_ranking_rel_search_table ").fetchall())
            data3 = dict(conn.execute(
                "select keyword, id from cd_ranking_keyword_table ").fetchall())
            data1["rel_search"] = data1['rel_search'].map(data2)
            data1["keyword"] = data1['keyword'].map(data3)
            data4 = data1.dropna()
            data4.insert(0, 'date', value=datetime.now().date())
            df = data4.rename(columns={'rel_search': 'rel_search_id', 'keyword': 'keyword_id'})[
                ['date', 'keyword_id', 'rel_search_id']]
            data_type = {'date': sqlalchemy.Date, 'keyword_id': sqlalchemy.Integer,
                         'rel_search_id': sqlalchemy.Integer}
            unique_upload(df, 'cd_ranking_keyword_rel_search_table',
                          conn, data_type=data_type)
    except Exception as e:
        logger.error(e)


def update_domain_table(path, conn):
    """function is used for updated to domain in domain_table 
    it takes 2 arguments 
    path= csv file path, conn =  database connection string  """
    try:

        df = pd.read_csv(path, on_bad_lines='skip',skipinitialspace = True)[
            ['domain']].dropna().drop_duplicates(keep='first')
        if df.empty != True:
           
            data_type = {'domain': sqlalchemy.String}
            unique_upload(df, 'cd_ranking_domain_table',
                          conn, data_type=data_type)
    except Exception as e:
        logger.error(e)


def update_rel_question_table(path, conn):
    """function is used for updated to related_question with respect to keyword and storing in related_question_table
    it takes 2 arguments 
    path= csv file path, conn =  database connection string  """
    try:

        # [['related_questions','sitelinks']]
        data1 = pd.read_csv(path, engine='python',  encoding='latin-1',
                            on_bad_lines='skip',skipinitialspace = True).drop_duplicates(keep='first')
        if data1.empty != True:
            df1 = data1[['question', 'pos', 'answer', 'domain']].dropna()
            df = data1[['source']].dropna()
            df['new_source'] = df['source'].apply(
                lambda x: ast.literal_eval(x))
            data = pd.DataFrame(df['new_source'].tolist())
            result = pd.concat([df1, data], axis=1, join='inner')
            domain_id = dict(conn.execute(
                "select domain, id from cd_ranking_domain_table ").fetchall())
            result['domain'] = result['domain'].map(domain_id)
            result = result.rename(columns={
                                   'question': 'rel_question', 'url': 'source_url', 'title': 'source_title', 'domain': 'domain_id'})
            df = result.dropna()[['rel_question', 'pos', 'answer',
                                  'source_url', 'source_title', 'domain_id', 'url_shown']]
            data_type = {'rel_question': sqlalchemy.String, 'pos': sqlalchemy.Integer, 'answer': sqlalchemy.Text,
                         'source_url': sqlalchemy.String, 'source_title': sqlalchemy.String, 'domain_id': sqlalchemy.Integer, 'url_shown': sqlalchemy.String}
            unique_upload(df, 'cd_ranking_rel_question_table',
                          conn, data_type=data_type)

            #"""update of key_rel_question_table updation"""#
            df = data1[['keyword', 'question']]
            question_id = dict(conn.execute(
                "select rel_question, id from cd_ranking_rel_question_table ").fetchall())
            key_id = dict(conn.execute(
                "select keyword, id from cd_ranking_keyword_table ").fetchall())
            df["question_id"] = df['question'].copy().map(question_id)
            df["keyword_id"] = df['keyword'].copy().map(key_id)
            df.insert(2, 'date', value=datetime.now().date())
            df = df[['date', 'keyword_id', 'question_id']].dropna()
            data_type = {'date': sqlalchemy.Date,
                         'keyword_id': sqlalchemy.Integer, 'question_id': sqlalchemy.Integer}
            unique_upload(df, 'cd_ranking_keyword_rel_question_table',
                          conn, data_type=data_type)
    except Exception as e:
        logger.error(e)


def update_description_table(path, conn,frequency):
    """function is used for updated ranking of urls with repect to keyword at specific date  and storing in description_table 
    it takes 3 arguments 
    path= csv file path, conn =  database connection string ,frequency=ranking frequency (daily ,weekly,monthly,temporary) """
    try:
        data1 = pd.read_csv(path, usecols=['keyword', 'pos', 'url',  'title', 'url_shown', 'pos_overall',
                            'domain', 'desc', 'date'], on_bad_lines='skip',skipinitialspace = True).drop_duplicates(keep='first')
        if data1.empty != True:
            data1.insert(0, 'desc_id', value=(
                data1['keyword']+data1['date']+data1['domain']+data1['pos'].astype(str)+frequency))
            data2 = dict(conn.execute(
                "select domain, id from cd_ranking_domain_table ").fetchall())
            data3 = dict(conn.execute(
                "select keyword, id from cd_ranking_keyword_table ").fetchall())
            data1["domain"] = data1['domain'].map(data2)
            data1["keyword"] = data1['keyword'].map(data3)
            data2 = data1.dropna().drop_duplicates(subset=["desc_id"], keep='first')
            data2 = data2.rename(
                columns={'keyword': 'keyword_id', 'domain': 'domain_id', 'desc': 'description'})
            data_type = {'desc_id': sqlalchemy.String, 'keyword_id': sqlalchemy.Integer, 'pos': sqlalchemy.Integer, 'url': sqlalchemy.String, 'desc': sqlalchemy.String, 'title': sqlalchemy.String, 'url_shown': sqlalchemy.String,
                         'pos_overall': sqlalchemy.Integer, 'domain_id': sqlalchemy.Integer, 'date': sqlalchemy.Date}
            data2['date'] = pd.to_datetime(data2['date'], format='%d-%m-%Y')
            data2.to_sql('myTempTable', con=conn, schema='public', index=True,
                         index_label='id', if_exists='replace', dtype=data_type)
            query = """select DISTINCT(desc_id), keyword_id,pos, url,  title, url_shown,pos_overall, domain_id,description, date from public."myTempTable"  WHERE desc_id NOT IN (select distinct(desc_id) from cd_ranking_description_table)
            Except
            select desc_id,keyword_id ,pos, url,  title, url_shown,pos_overall, domain_id,description, date from cd_ranking_description_table"""
            new_data = pd.read_sql(query, con=conn)
            ##print(len(df.index)- len(new_data.index) ,"  data are skipped due to duplicate data")
            new_data.to_sql('cd_ranking_description_table', con=conn,
                            index=False, if_exists='append', dtype=data_type)
            print("cd_ranking_description_table update successfully \n\n")
            conn.execute('drop table "myTempTable"')
    except Exception as e:
        logger.error(e)


def update_question_table(path, conn):
    """function is used for updated question along with url and keyword and store in question_table
    it takes 2 arguments 
    path= csv file path, conn =  database connection string   """
    try:

        data1 = pd.read_csv(path, engine='python', encoding='latin-1',
                            on_bad_lines='skip',skipinitialspace = True).drop_duplicates(keep='first')
        if data1.empty != True:
            data1.insert(0, 'desc_id', value=(
                data1['keyword']+data1['date']+data1['domain']+data1['pos'].astype(str)))
            df = data1[['desc_id', 'related_questions']].dropna()
            df['new_rel'] = df['related_questions'].apply(
                lambda x: ast.literal_eval(x))

            mydata = dict(zip(df['desc_id'], df['new_rel']))
            L = [mydata]
            df = pd.DataFrame([{'desc_id': k, **y} for x in L for k, v in x.items()
                              for y in v])[['question', 'pos', 'desc_id']]
            query = """select question ,pos, desc_id  from public."myTempTable" where desc_id in (select desc_id from cd_ranking_description_table)
            Except 
            select  question ,pos,desc_id   from cd_ranking_question_table"""
            data_type = {'question': sqlalchemy.String,
                         'pos': sqlalchemy.Integer, 'desc_id': sqlalchemy.String}
            unique_upload(df, 'cd_ranking_question_table',
                          conn, query, data_type=data_type)
    except Exception as e:
        logger.error(e)


def update_sitelink_table(path, conn):
    """function is used for updated sitelinks  along with url and keyword and store in sitelink_table 
    it takes 2 arguments 
    path= csv file path, conn =  database connection string  """
    
    try:

        data1 = pd.read_csv(path, engine='python', encoding='latin-1',
                            on_bad_lines='skip',skipinitialspace = True).drop_duplicates(keep='first')
        if data1.empty != True:
            data1.insert(0, 'desc_id', value=(
                data1['keyword']+data1['date']+data1['domain']+data1['pos'].astype(str)))
            df = data1[['desc_id', 'sitelinks']].dropna()
            df['new_site'] = df['sitelinks'].apply(
                lambda x: ast.literal_eval(x))
            L = df['new_site'].tolist()
            L = [dict(zip(df['desc_id'], L))]
            df = pd.DataFrame([{'url_type': k2, 'desc_id': k1, **y}for x in L for k1, v1 in x.items()
                              for k2, v2 in v1.items() for y in v2])[['url_type', 'url', 'title', 'desc_id']]
            query = """select url_type,url,title,desc_id from public."myTempTable"  where desc_id in (select desc_id from cd_ranking_description_table)
            Except 
            select url_type,url,title,desc_id from cd_ranking_sitelink_table"""
            data_type = {'url_type': sqlalchemy.String, 'url': sqlalchemy.String,
                         'title': sqlalchemy.String, 'desc_id': sqlalchemy.String}

            unique_upload(df, 'cd_ranking_sitelink_table',
                          conn, query, data_type=data_type)
    except Exception as e:
        logger.error(e)


""" Function for unique data updation in target table"""


def unique_upload(df, target_table, conn, query_string='', data_type=''):
    """function is used for insert only  unique data in given table by the given dataframe 
    it takes 5 arguments 
    df=given dataframe , target_table = table name at which you want perform opreation,query_string = query which want to perform on target table by default its empty in empty case it perform uniaue insertion ,data_types= it is a dectionary of mapped with dtaframe column and sqlalchemy data types"""
    try:

        df.to_sql('myTempTable', con=conn, schema='public', index=True,
                  index_label='id', if_exists='replace', dtype=data_type)
        column_list = [i for i in df.columns]
        if query_string == '':
            query = """select {0} from public."myTempTable"  
            Except  
            select  {0} from {1}""".format(",".join('%s' % col for col in column_list), target_table)
        else:
            query = query_string
        new_data = pd.read_sql(query, con=conn)
        

        new_data.index += 1 + \
            int((conn.execute("select max(id) from {}".format(
                target_table))).fetchone()[0] or 0)
        #print(len(df.index)- len(new_data.index) ,"  data are skipped due to duplicate data")
        new_data.to_sql(target_table, con=conn, index=True,
                        index_label='id', if_exists='append', dtype=data_type)
        conn.execute('drop table public."myTempTable"')
        print(target_table + " update successfully")

    except Exception as e:
        logger.error(e )

@shared_task
def scrapper():
    from scrapper.main_for_bd import  main
    main()
