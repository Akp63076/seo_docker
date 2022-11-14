from __future__ import absolute_import
from typing import Counter
from celery import Celery, shared_task
#from celery.decorators import task
from celery.utils.log import get_task_logger
from django.conf import settings
from django.core import mail
from django.core.mail import EmailMessage, send_mail
from celery.schedules import crontab
import random
import time
import os

cwd = os.getcwd()
filepath = "redshiftClicks/templates/redshiftClicks/redshift.html"
tem_path = os.path.join(cwd, filepath)

logger = get_task_logger(__name__)
from django.template import Context
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage

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


@shared_task(name="sendRedshiftEmail")
def sendRedshiftEmail(url, recipient, timeRange):    
    print(url, recipient, timeRange)
    user_choice = {"url": url, "duration": timeRange}
    print("function has started")
    task_data = RedshiftSql(url, timeRange)

    ctx = {"task_data": task_data, "user_choice": user_choice}
    print(task_data)
    message = get_template(tem_path).render(ctx)
    # message = ""
    email_from = settings.EMAIL_HOST_USER
    subject = "Redshift Data for query url : {0}".format(url)
    recipient_list = [recipient]
    #recipient_list.append("datateam.main@gmail.com")    
    print("sending email")
    email = EmailMessage(subject, message, email_from, recipient_list)
    email.content_subtype = "html"
    email.send()
    """Background task that runs a long function with progress reports."""
    verb = ["Starting up", "Booting", "Repairing", "Loading", "Checking"]
    status_message = ""
    
    for i, file in enumerate(task_data):
        if not status_message:
            status_message = "{0}...".format(random.choice(verb))
        
        sendRedshiftEmail.update_state(
            state="PROGRESS",
            meta={"current": i, "total": len(file), "status": status_message},
        )
        time.sleep(1)
        
    

    return {
        "current": 100,
        "total": 100,
        "status": "Task completed!",
        "result": task_data,
    }
