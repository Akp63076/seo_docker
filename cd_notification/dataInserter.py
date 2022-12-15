import pandas as pd
from .models import News
from .scrappers.testScrapper import scrapping
from celery import shared_task

@shared_task()
def insertNewsData():
    scrapping()
    print("insertion going on")
    df = pd.read_csv('news/scrappers/cd_main.csv')

    df = df.drop_duplicates(['source', 'title', 'date'])

    # print(df.iloc[1, 5])

    for i in range(len(df)):
        # print(df.loc[i, "source"], df.loc[i, "title"], df.loc[i, "link"], df.loc[i, 'date'])
        try:
            source = df.iloc[i, 0]
        except Exception as e:
            source = "N/A"
            print(e)
        
        try:
            headline = df.iloc[i, 1]
        except Exception as e:
            headline = "N/A"
            print(e)
        
        try:
            link = df.iloc[i, 2]
        except Exception as e:
            link = "N/A"
            print(e)
        
        try:
            reportedAt = df.iloc[i, 3]
        except Exception as e:
            reportedAt = "N/A"
            print(e)
        
        # print(source , headline,  link, reportedAt)

        # if reportedAt == "N/A":
        #     News.objects.create(source=source, headline=headline,
        #                     link=link)
        # else:
        #     News.objects.create(source=source, headline=headline,
        #                     link=link, reportedAt=reportedAt)