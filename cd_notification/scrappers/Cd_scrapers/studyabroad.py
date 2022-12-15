from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from datetime import datetime
from dotenv import load_dotenv
import requests
import csv
from bs4 import BeautifulSoup
import pandas as pd
# import pymysql
import os
from zoneinfo import ZoneInfo

study_abroad = []
success = []
failure = []
options=Options()
options.headless=True

load_dotenv()
now = datetime.now(tz=ZoneInfo('Asia/Kolkata'))
print (now.strftime("%Y-%m-%d %H:%M:%S"))

options=Options()
options.headless=True
fp=webdriver.FirefoxProfile()
fp.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36")
fp.set_preference("dom.webnotifications.enabled", False)
fp.set_preference("network.cookie.cookieBehavior", 2)


# Driver Initiated
driver = webdriver.Firefox(options=options)

# Selenium Scrapers Started
# Poets and Quants-1
try:
    base_url = 'https://poetsandquants.com/'
    driver.get(base_url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    results = soup.find('div', {'id':'exclusives'}).find_all('h3')
    for result in results:
        headline = result.find('a').get_text().strip()
        link = result.find('a')['href'].strip()
        study_abroad.append(('Poets n Quants', headline, link))
    success.append('Poets n Quants-1')
except Exception as e:
    failure.append(('Poets n Quants-1', e))
    pass

# Poets and Quants-2
try:
    base_url = 'https://poetsandquants.com/'
    driver.get(base_url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    results = soup.find('div', {'id':'more-stuff'}).find_all('h5')
    for result in results:
        headline = result.find('a').get_text().strip()
        link = result.find('a')['href'].strip()
        study_abroad.append(('Poets n Quants', headline, link))
    success.append('Poets n Quants-2')
except Exception as e:
    failure.append(('Poets n Quants-2', e))
    pass

# Times Higher Education
try:
    name="Times Higher Education"
    url="https://www.timeshighereducation.com/academic/news"
    base_url="https://www.timeshighereducation.com"
    driver.get(url)
    soup=BeautifulSoup(driver.page_source,"html.parser")
    results=soup.find("div",class_="panel-pane pane-article-content-list").find_all("div",class_="teaser-card__image-wrapper")
    for result in results:
        headline=result.find("a").text.replace("\n"," ").strip()
        link=result.find("a").get("href")
        if "http" in link:
            link=link
        else:
            link=base_url+link
        study_abroad.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# US News
try:
    name="US News"
    url="https://www.usnews.com/education"
    driver.get(url)
    soup=BeautifulSoup(driver.page_source, 'html.parser')
    results=soup.find_all("div",class_="Box-w0dun1-0 MediaObject__Content-sc-19vl09d-3 CYZBT gilvxg")
    for result in results:
        headline=result.find('h3').text.strip()
        link=result.find("h3").a.get("href")
        study_abroad.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# Selenium Scrapers Ended
# Driver Quit
driver.quit()

# Request Scrapers Started
# Indian-Express-1
try:                                            
    base_url = 'https://indianexpress.com/section/education/study-abroad/'
    res = requests.get(base_url)
    soup = BeautifulSoup(res.text, 'html.parser')
    newss = soup.find(class_='nation').find_all(class_='articles')
    for news in newss:
        headline = news.find(class_='title').find('a').get_text()
        link = news.find(class_='title').find('a').get('href')
        study_abroad.append(('Indian-Express-SA', headline[:999], link))
    success.append('Indian-Express-SA')
except Exception as e:
    failure.append(('Indian-Express-SA', e))
    pass



#CIC News-1
try:
    base_url = 'https://www.cicnews.com/'
    agent = {"User-Agent":"Mozilla/5.0"}
    res=requests.get(base_url, headers=agent)
    soup = BeautifulSoup(res.text, 'html.parser')
    results = soup.find(class_='article_content').find_all('article')
    for result in results:
        headline = result.find('span').get_text().strip()
        link = result.find('h3').find('a')['href'].strip()
        study_abroad.append(('CIC-News', headline, link))
    success.append('CIC-News-1')
except Exception as e:
    failure.append(('CIC-News-1', e))
    pass

# CIC News-2
try:
    base_url = 'https://www.cicnews.com/'
    agent = {"User-Agent":"Mozilla/5.0"}
    res=requests.get(base_url, headers=agent)
    soup = BeautifulSoup(res.text, 'html.parser')
    results = soup.find(class_='row-flex').find_all(class_='caption_box')
    for result in results:
        headline = result.find(['h2','h3']).get_text().strip()
        link = result.find_next_sibling('a')['href'].strip()
        study_abroad.append(('CIC-News', headline, link))
    success.append('CIC-News-2')
except Exception as e:
    failure.append(('CIC-News-2', e))
    pass

# CIC News-3
try:
    base_url = 'https://www.cicnews.com/'
    agent = {"User-Agent":"Mozilla/5.0"}
    res=requests.get(base_url, headers=agent)
    soup = BeautifulSoup(res.text, 'html.parser')
    results = soup.find(class_='trending_list').find_all('li')
    for result in results:
        headline = result.find('h4').get_text().strip()
        link = result.find('h4').find('a')['href'].strip()
        study_abroad.append(('CIC-News', headline, link))
    success.append('CIC-News-3')
except Exception as e:
    failure.append(('CIC-News-3', e))
    pass

#Inside Higher Ed
try:
    base_url = 'https://www.insidehighered.com/news'
    url = 'https://www.insidehighered.com'
    res=requests.get(base_url)
    soup = BeautifulSoup(res.text, 'html.parser')
    results = soup.find(class_='panel-pane pane-views pane-news').find_all('h3')
    for result in results:
        headline = result.find('a').get_text().strip()
        link = url+result.find('a')['href'].strip()
        study_abroad.append(('Inside Higher Ed', headline, link))
    success.append('Inside Higher Ed')
except Exception as e:
    failure.append(('Inside Higher Ed', e))
    pass

# Buddy4study
try:
    base_url = 'https://www.buddy4study.com/scholarships/study-abroad'
    url = 'https://www.buddy4study.com'
    res=requests.get(base_url)
    soup = BeautifulSoup(res.text, 'html.parser')
    results = soup.find(class_='scholarshiplist_listItem__3XH3k row').find_all(class_='scholarshipslistcard_listCard__3oVnA')
    for result in results:
        headline = result.find('h4').find('span').get_text().strip()
        link = url+result.find('a')['href'].strip()
        study_abroad.append(('Buddy4study', headline, link))
    success.append('Buddy4study')
except Exception as e:
    failure.append(('Buddy4study', e))
    pass

# Leverage Edu
try:
    base_url = 'https://leverageedu.com/blog/category/study-abroad/'
    res=requests.get(base_url)
    soup = BeautifulSoup(res.text, 'html.parser')
    results = soup.find(class_='archive-wrap').find_all(class_='post-outer')
    for result in results:
        headline = result.find('h2').get_text().strip()
        link = result.find('h2').find('a')['href'].strip()
        study_abroad.append(('Leverage Edu', headline, link))
    success.append('Leverage Edu')
except Exception as e:
    failure.append(('Leverage Edu', e))
    pass

# NDTV
try:                                            
    base_url = 'https://www.ndtv.com/topic/study-abroad'
    res = requests.get(base_url)
    soup = BeautifulSoup(res.text, 'html.parser')
    newss = soup.find('div', {'id':'news_list'}).find('ul').find_all('li')
    for news in newss:
        headline = news.find('a').get('title')
        link = news.find('a').get('href')
        study_abroad.append(('NDTV', headline[:999], link))
    success.append('NDTV')
except Exception as e:
    failure.append(('NDTV', e))
    pass


# Top Universities
try:
    base_url = 'https://www.topuniversities.com/student-info/studying-abroad-articles'
    url = 'https://www.topuniversities.com'
    res = requests.get(base_url)
    soup = BeautifulSoup(res.text, 'html.parser')
    results = soup.find(class_='view-content').find_all(class_='right-wrap')
    for result in results:
        headline = result.find('a')['title']
        link = url + result.find('a')['href']
        study_abroad.append(('Top Universities', headline, link))
    success.append('Top Universities')
except Exception as e:
    failure.append(('Top Universities', e))
    pass

# Study International
try:
    base_url = 'https://www.studyinternational.com/postgraduate/'
    res = requests.get(base_url)
    soup = BeautifulSoup(res.text, 'html.parser')
    results = soup.find(class_='content-wrapper').find_all(class_='col col--third')
    for result in results:
        headline = result.find(class_='post-meta').find('h3').get_text().strip()
        link = result.find('a')['href'].strip()
        study_abroad.append(('Study International', headline, link))
    success.append('Study International')
except Exception as e:
    failure.append(('Study International', e))
    pass

# MBA news-1
try:
    base_url = 'https://www.mbanews.com.au/'
    agent = {"User-Agent":"Mozilla/5.0"}
    res = requests.get(base_url, headers=agent)
    soup = BeautifulSoup(res.text, 'html.parser')
    results = soup.find(class_='td_block_wrap td_block_1 tdi_25 td_with_ajax_pagination td-pb-border-top td_block_template_1 td-column-2').find_all('h3')
    for result in results:
        headline = result.find('a').get_text().strip()
        link = result.find('a')['href'].strip()
        study_abroad.append(('MBA news', headline, link))
    success.append('MBA news-1')
except Exception as e:
    failure.append(('MBA news-1', e))
    pass

# MBA news-2
try:
    base_url = 'https://www.mbanews.com.au/'
    agent = {"User-Agent":"Mozilla/5.0"}
    res = requests.get(base_url, headers=agent)
    soup = BeautifulSoup(res.text, 'html.parser')
    results = soup.find(class_='td_block_wrap td_block_1 tdi_30 td-pb-border-top td_block_template_1 td_ajax_preloading_preload td-column-2').find_all('h3')
    for result in results:
        headline = result.find('a').get_text().strip()
        link = result.find('a')['href'].strip()
        study_abroad.append(('MBA news', headline, link))
    success.append('MBA news-2')
except Exception as e:
    failure.append(('MBA news-2', e))
    pass

# MBA news-3
try:
    base_url = 'https://www.mbanews.com.au/'
    agent = {"User-Agent":"Mozilla/5.0"}
    res = requests.get(base_url, headers=agent)
    soup = BeautifulSoup(res.text, 'html.parser')
    results = soup.find(class_='td_block_wrap td_block_1 tdi_31 td_with_ajax_pagination td-pb-border-top td_block_template_1 td-column-2').find_all('h3')
    for result in results:
        headline = result.find('a').get_text().strip()
        link = result.find('a')['href'].strip()
        study_abroad.append(('MBA news', headline, link))
    success.append('MBA news-3')
except Exception as e:
    failure.append(('MBA news-3', e))
    pass

# Collegedekho Study Abroad
try:
    name="Collegedekho Study Abroad"
    url="https://www.collegedekho.com/study-abroad/news/"
    res=requests.get(url)
    soup=BeautifulSoup(res.text,"html.parser")
    results=soup.find("div",class_="container countryDetail blogBlock").find_all("li")
    for result in results[:6]:
        headline=result.find("h3").text
        link=result.find("a").get("href")
        if "http" in link:
            link=link
        else:
            link=url+link
        study_abroad.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# Studies in Australia
try:
    name="Studies in Australia"
    url="https://www.studiesinaustralia.com/Blog/australian-education-news"
    res=requests.get(url)
    soup=BeautifulSoup(res.text,"html.parser")
    results=soup.find_all("div",class_="card-body")
    for result in results:
        if (result.find('a',class_="card-title")==None):
            continue
        else:
            headline=result.text.replace('read more'," ")[:-15].strip()
            link=result.a.get("href")
        study_abroad.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# Edugraph
try:
    name="Edugraph"
    url="https://www.telegraphindia.com/edugraph/news"
    base_url="https://www.telegraphindia.com"
    res=requests.get(url)
    soup=BeautifulSoup(res.text,"html.parser")
    results=soup.find('div',class_="more-grid d-flex flex-wrap").find_all('div', class_='more-col mb-40')
    for result in results:
        headline=result.h2.text.strip()
        link=result.find('a').get('href')
        if "http" in link:
            link=link
        else:
            link=base_url+link
        study_abroad.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# The Conversation
try:
    name="The Conversation"
    url="https://theconversation.com/global"
    base_url="https://theconversation.com"
    res=requests.get(url)
    soup=BeautifulSoup(res.text,"html.parser")
    results=soup.find("div",id="outer").find_all("div",class_="article--header")
    for result in results:
        headline=result.find("h2").text.strip()
        link=result.find("a").get("href")
        if "http" in link:
            link=link
        else:
            link=base_url+link
        study_abroad.append((name,headline.replace("\xa0"," ").strip(),link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# The Pie News
try:
    name="The Pie News"
    url="https://thepienews.com/news/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text,'html.parser')
    results=soup.find("div",class_="container").find_all('article')
    for result in results:
        headline = result.find('h3').text
        link =  result.find('a')['href']
        study_abroad.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# Study in UK
try:
    name="Study in UK"
    url="https://www.studyin-uk.com/news/"
    base_url="https://www.studyin-uk.com"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results=soup.find_all("div",class_="news-post")
    for result in results:
        headline=result.find("h3").text.strip()
        link=result.find("a").get("href")
        if "http" in link:
            link=link
        else:
            link=base_url+link
        study_abroad.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# The Economic Times
try:
    name="The Economic Times"
    url="https://economictimes.indiatimes.com/nri/study"
    base_url="https://economictimes.indiatimes.com"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results=soup.find("div",class_="tabdata").find_all("div",class_="eachStory")
    for result in results:
        headline=result.find("h3").text.strip()
        link=result.find("h3").a.get("href")
        if "http" in link:
            link=link
        else:
            link=base_url+link
        study_abroad.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# SI-News
try:                                            
    base_url = 'https://www.studyinternational.com/news/'
    res = requests.get(base_url)
    soup = BeautifulSoup(res.text, 'html.parser')
    newss = soup.find_all('article', {'role':'article'})
    for news in newss:
        headline = news.find(class_='entry-title').find('a').get('title').strip()
        link = news.find(class_='entry-title').find('a').get('href')
        study_abroad.append(('SI-News', headline[:999], link))
    success.append('SI-News')
except Exception as e:
    failure.append(('SI-News', e))
    pass
# Request Scrapers Ended

print('Successful Scrapers -', success)
print('Failed Scrapers -', failure)
df = pd.DataFrame(study_abroad)
df.drop_duplicates(inplace = True) 
df['date'] = now.strftime("%Y-%m-%d %H:%M")
df.columns = ['source','title','link','date']


try:    
    data = pd.read_csv('/root/New_Scrapers/Cd_scrapers/cd_main.csv')
except:
    data = pd.DataFrame()
    print("error in csv read")
print(f"df shape {df.shape}")
print(f"data shape: {data.shape}")
data = pd.concat([ data,df])
print("After append")
print(f"df shape {df.shape}")
print(f"data shape: {data.shape}")

data.drop_duplicates(subset = ['title'], inplace = True)
data.to_csv('/root/New_Scrapers/Cd_scrapers/cd_main.csv', index = False)

