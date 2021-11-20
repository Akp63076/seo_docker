import os

import psycopg2
from config import config

import pandas as pd 
print(os.getcwd())
base_dir = os.getcwd()


path = "/Users/collegedunia/Documents/flask_project/seoTool/ranking/script/data.csv"
df= pd.read_csv(path,encoding = 'unicode_escape')
def copy_from_file(conn,df,table):
    """
    Here we are going save the dataframe on disk as 
    a csv file, load the csv file  
    and use copy_from() to copy it to the table
    """
    # Save the dataframe to disk
    import pandas as pd
    
    tmp_df = "/Users/collegedunia/Documents/flask_project/seoTool/ranking/script/data-1.csv"
    
    df.to_csv(tmp_df,index_label='id', header=False,sep='|')
    
    # tmp_df = ""
    # df.to_csv(tmp_df, index_label='id', header=False)
    f = open(tmp_df, 'r')
    print(f)
    cursor = conn.cursor()
    try:
        cursor.copy_from(f, table, sep="|")
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
      
        print("Error: %s" % error)
        conn.rollback()
        cursor.close()
        return 1
    print("copy_from_file() done")
    cursor.close()
    return 1

def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        # table = "ranking_keywords"
        # x = copy_from_file(conn,df,table)
        # print(x)
        # create a cursor
        cur = conn.cursor()

        # execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')
        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)

        # close the communication with the PostgreSQL
        cur.close()
    except  (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

if __name__ == '__main__':
    connect()
