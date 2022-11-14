import time
import pandas as pd
from sqlalchemy import create_engine

def RedshiftSql(user_url, user_time):
    redshift_user = "report"
    redshift_pass = "lVxOY5Kn0NHe6Y5m"
    port = 5439
    dbname = "collegedunia"
    host = "redshift-cluster-1.cjkc5tvkknao.ap-south-1.redshift.amazonaws.com"

    engine_string = "postgresql+psycopg2://%s:%s@%s:%d/%s" % (
        redshift_user,
        redshift_pass,
        host,
        port,
        dbname,
    )
    engine = create_engine(engine_string)

    print("Redshift Tunnel Engine Successfully Created")

    print("Running SQL query 1")

    url = user_url
    date = user_time

    query = f"""SELECT event_value, link_title, SUM(countt) AS session_count
            FROM (SELECT event_value, link_title, cast(ts as date), COUNT(session_id) AS countt
                  FROM cd_schema.Events
                  WHERE referrer = %s
                  AND event = 'link_click'
                  AND cast(ts as date)<=CURRENT_DATE
                  AND cast(ts as date)>=CURRENT_DATE - interval %s
                  GROUP BY cast(ts as date), event_value, link_title, event, referrer)
            GROUP BY event_value, link_title
            ORDER BY session_count DESC"""
    start = time.time()
    query_result_df = pd.read_sql_query(query, engine, params=[url, date])
    query_result_df.sort_values(by=["session_count"], ascending=False, inplace=True)
    end = time.time()
    print("time taken on sql query: {}".format(end - start))
    # query_result_df.to_csv('/home/flask_app/college_pred/data/linking/query.csv')
    query_result_dict = query_result_df.to_dict("records")
    return query_result_dict
data=RedshiftSql("https://collegedunia.com/courses/post-graduate-diploma-in-information-technology-pgdit","1 week")
print(data)