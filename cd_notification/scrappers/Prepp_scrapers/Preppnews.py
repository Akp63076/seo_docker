from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
# from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from datetime import datetime
from zoneinfo import ZoneInfo
import requests
import os
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import time
import pandas as pd

news_articles = []
success = []
failure = []

#load_dotenv()
now = datetime.now(tz=ZoneInfo('Asia/Kolkata'))
timestamp = now.strftime("%Y-%m-%d %H:%M")
print (now.strftime("%Y-%m-%d %H:%M:%S"))

options=Options()
options.headless=True
fp=webdriver.FirefoxProfile()
fp.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36")
fp.set_preference("dom.webnotifications.enabled", False)
fp.set_preference("network.cookie.cookieBehavior", 2)

# Driver Initiated
# driver=webdriver.Firefox(options= options)
driver = webdriver.Firefox(options=options,firefox_profile=fp )



#Aaj ki news
try:
    url = 'https://aajkinews.net/category/jobs/'
    base_url = 'https://aajkinews.net/'
    name = "Aaj ki news"
    content = requests.get(url)
    soup = BeautifulSoup(content.text, "html.parser")
    headlines = soup.find_all('h3', class_ = 'entry-title mh-loop-title')
    for line in headlines: 
        headline = line.find('a').text.replace("\n","")
        link = line.find('a').get('href')
        if link.startswith('http'):
            link = link
        else:
            link = base_url+link
        news_articles.append((name, headline, link))
    success.append(name)
except Exception as e:
    name = "Aaj ki news"
    failure.append((name,e))

 #ZEEBIZ
try :
    base_url = "https://www.zeebiz.com/"
    url = "https://www.zeebiz.com/hindi/jobs"
    res = requests.get(url, verify=False)
    soup = BeautifulSoup(res.text,"html.parser")
    link_list = soup.find_all('div', class_ = 'mstrecntbx clearfix')
    for i in link_list[:10]:
        box = i.find('div', class_ = 'text-overflow')
        content = box.find('a')
        if content is not None:
            headline = content.get_text()
            link = content.get('href')
            if 'http' not in link:
                link = base_url+link
            news_articles.append(('ZEEBIZ',headline,link))
    success.append('ZEEBIZ')      
except Exception as e:
    failure.append(('ZEEBIZ',e))

#ASAMNEWS18(done)

try:
    base_url = "https://assam.news18.com/"
    url = "https://assam.news18.com/tag/job/news/"
    res = requests.get(url, verify=False)
    soup = BeautifulSoup(res.text,"html.parser")
 
    content = soup.find('ul', class_ = 'tag-listing-new clearfix')
    if content is not None:
        link_list = content.find_all('li')
        for i in link_list[:10]:
            box = i.find('a')
            if box is not None:
                headline = box.get_text()
                link = box.get('href')
                if 'http' not in link:
                    link = base_url+link
                news_articles.append(('ASAMNEWS18',headline,link))
        success.append('ASAMNEWS18')      
except Exception as e:
    failure.append(('ASAMNEWS18',e))
 

#HINDINEWS18

try:
    url = 'https://hindi.news18.com/news/jobs/'
    base_url = 'https://hindi.news18.com/'
    name = "HINDINEWS18"
    content = requests.get(url) 
#     print(content.status_code)
    soup = BeautifulSoup(content.text, "html.parser")
    
    results = soup.find_all('ul',  class_ ='jsx-1173356385')
    for result in results:
        headlines = result.find_all('a')
        for line in headlines:
            headline = line.text
            link = line.get('href')
            if link.startswith('http'):
                link = link
            else:
                link = base_url+link
            news_articles.append((name, headline, link))
            
    results2 = soup.find_all('div', class_ ='jsx-3343455497 blog_list_row') 
    for result in results2:
        headline = result.text
        link = result.find('a').get('href')
        if link.startswith('http'):
            link = link
        else:
            link =base_url+link
        news_articles.append((name, headline, link))    
           
    success.append(name)
except Exception as e:
    name = "HINDINEWS18"
    failure.append((name,e))

#INDIANEXPRESS

try:
    base_url = "https://indianexpress.com/"
    url = "https://indianexpress.com/article/jobs/"
    res = requests.get(url, verify=False)
    soup = BeautifulSoup(res.text,"html.parser")
    content = soup.find('div', class_ = 'nation')
    link_list = content.find_all('div', class_ = 'articles')
    for i in link_list[:5]:
        con = i.find('h2')
        box = con.find('a')
        if box is not None:
            headline = box.text
            link = box.get('href')
            if 'http' not in link:
                link = base_url+link
            news_articles.append(('INDIANEXPRESS',headline,link))
    success.append('INDIANEXPRESS')      
except Exception as e:
    failure.append(('INDIANEXPRESS',e))

#LOKMATNEWS18

try:
    base_url = "https://lokmat.news18.com/"
    url = "https://lokmat.news18.com/category/career/"
    res = requests.get(url, verify=False)
    soup = BeautifulSoup(res.text,"html.parser")
    content = soup.find_all('div', class_ = 'tp-3story clearfix')
    for i in content[:5]:
        link_list = i.find_all('li')
        for j in link_list:
            con = i.find('h2')
            box = con.find('a')
            if box is not None:
                headline = box.text
                link = box.get('href')
                if 'http' not in link:
                    link = base_url+link
                news_articles.append(('LOKMATNEWS18',headline,link))
    success.append('LOKMATNEWS18')      
except Exception as e:
    failure.append(('LOKMATNEWS18',e))
    pass


#MALAYALAMNEWS18
try:
    base_url = "https://malayalam.news18.com/"
    url = "https://malayalam.news18.com/career/"
    res = requests.get(url, verify=False)
    soup = BeautifulSoup(res.text,"html.parser")
 
    content_1 = soup.find('div', class_ = 'section-blog-left-img-list')
    content_2 = soup.find('div', class_ = 'blog-list')
 
    link_list_1 = content_1.find_all('li')
    link_list_2 = content_2.find_all('div', class_ = 'blog-list-blog')
 
    for i in link_list_1[:10]:
        box = i.find('a')
        if box is not None:
            headline = box.text
            link = box.get('href')
            if 'http' not in link:
                link = base_url+link
        news_articles.append(('MALAYALAMNEWS18',headline,link))
 
    for i in link_list_2[:10]:
        con = i.find('p')
        box = con.find('a')
        if box is not None:
            headline = box.text
            link = box.get('href')
            if 'http' not in link:
                link = base_url+link

            news_articles.append(('MALAYALAMNEWS18',headline,link))
    
    success.append('MALAYALAMNEWS18')  
except Exception as e:
    failure.append(('MALAYALAMNEWS18',e))

 
#MPBREAKINGNEWS 


try:
    base_url = "https://mpbreakingnews.in/"
    url = "https://mpbreakingnews.in/job-vacancy/"
    res = requests.get(url, verify=False)
    soup = BeautifulSoup(res.text,"html.parser")
   
    content_1 = soup.find_all('div', class_ = 'td-meta-info-container')
    content_2 = soup.find('div', class_ = 'td-ss-main-content')
 
    link_list_2 = content_2.find_all('h3')
 
    for i in content_1[:5]:
        con = i.find('h3')
        box = con.find('a')
        if box is not None:
            headline = box.text
            link = box.get('href')
            if 'http' not in link:
                link = base_url+link
            news_articles.append(('mpbreakingnews',headline,link))
 
    for i in link_list_2[:5]:
        box = i.find('a')
        if box is not None:
            headline = box.text
            link = box.get('href')
            if 'http' not in link:
                link = base_url+link
            news_articles.append(('mpbreakingnews',headline,link))
       
    success.append('mpbreakingnews')
except Exception as e:
    failure.append(('mpbreakingnews',e))


#NDTV

try:
    base_url = "https://ndtv.in/"
    url = "https://ndtv.in/jobs"
    res = requests.get(url, verify=False)
    soup = BeautifulSoup(res.text,"html.parser")
 
    content = soup.find('div', class_ = 'lisingNews')
    link_list = content.find_all('div', class_ = 'news_Itm')
    for i in link_list[:10]:
        con = i.find('h2')
        if con is not None:
            box = con.find('a')
            if box is not None:
                headline = box.text
                link = box.get('href')
                if 'http' not in link:
                    link = base_url+link
                news_articles.append(('NDTV',headline,link))
    success.append('NDTV')      
except Exception as e:
    failure.append(('NDTV',e))

#AAJTAKCAREER

try:
    base_url = "https://www.aajtak.in/"
    url = "https://www.aajtak.in/education/career"
    res = requests.get(url, verify=False)
    soup = BeautifulSoup(res.text,"html.parser")
    content = soup.find('div', class_ = 'section-listing-LHS')
    link_list = content.find_all('div', class_ ='widget-listing')
 
    for i in link_list[:5]:
        con = i.find('h2')
        box = con.find('a')
        if box is not None:
            headline = box.text
            link = box.get('href')
            if 'http' not in link:
                link = base_url+link
        news_articles.append(('AAJTAKCAREER',headline,link))
    success.append('AAJTAKCAREER')      
except Exception as e:
    failure.append(('AAJTAKCAREER',e))
    pass


#adda247

try:
    url = 'https://www.adda247.com/jobs/'
    base_url = "https://www.adda247.com"
    name = 'adda247'
    content = requests.get(url)
    document = BeautifulSoup(content.text, "html.parser")
    div1 = document.find('div',class_="entry-content").find_all('div', class_="wp-block-column new-icon")
    for div2 in div1:
        seg = div2.find('ul').find_all('li')
        for i in seg:
            headline = i.get_text()
            link = i.find_all('a', href=True)[0]['href']
            news_articles.append((name,headline,link))
            
    success.append(name)
    # print(news_articles)
except Exception as e:
    failure.append((name,e))
    pass



#ADDABANKJOBS

try:
    base_url = "https://www.adda247.com/"
    url = "https://www.adda247.com/jobs/bank-jobs/"
    res = requests.get(url, verify=False)
    soup = BeautifulSoup(res.text,"html.parser")
 
    section = soup.find_all('div', class_ = 'wp-block-column')
    content = section[0].find('ul', class_ ='lcp_catlist')
    link_list = content.find_all('li')
    for i in link_list[:10]:
        box = i.find('a')
        if box is not None:
            headline = box.text
            link = box.get('href')
            if 'http' not in link:
                link = base_url+link
            news_articles.append(('ADDABANKJOBS',headline,link))
    success.append('ADDABANKJOBS')      
except Exception as e:
    failure.append(('ADDABANKJOBS',e))
    pass


#AMARUJALA

try:
    base_url = "https://www.amarujala.com/"
    url = "https://www.amarujala.com/jobs/government-jobs"
    res = requests.get(url, verify=False)
    soup = BeautifulSoup(res.text,"html.parser")

    content = soup.find('div', id ='page0')
    link_list = content.find_all('section', class_ = '__main_listing_content')  
    for i in link_list:
        con  = i.find('h3')
        if con is not None:
            box = con.find('a')
            if box is not None:
                headline = box.text
                link = box.get('href')
                if 'http' not in link:
                    link = base_url+link
                news_articles.append(('AMARUJALA',headline,link))
    success.append('AMARUJALA')      
except Exception as e:
    failure.append(('AMARUJALA',e))
    pass


#PATRIKA 

try:
    base_url = "https://www.patrika.com/"
    url = "https://www.patrika.com/jobs/"
    res = requests.get(url, verify=False)
    soup = BeautifulSoup(res.text,"html.parser") 
    content = soup.find('div', class_ = 'flex flex-col space-y-4 divide-y')
    link_list = content.find_all('div', class_ = 'w-2/3 flex flex-col md:pr-5')

    for i in link_list:
        box = i.find('a')
        if box is not None:
            headline = box.text
            link = box.get('href')
            if 'http' not in link:
                link = base_url+link
            news_articles.append(('PATRIKA',headline,link))
    success.append('PATRIKA')      
except Exception as e:
    failure.append(('PATRIKA',e))
    pass


#REWARIYAT

try:
    base_url = "https://www.rewariyasat.com/"
    url = "https://www.rewariyasat.com/jobs/"
    res = requests.get(url, verify=False)
    soup = BeautifulSoup(res.text,"html.parser")
    
    content = soup.find('div', class_ = 'm_top15')
    link_list = content.find_all('h2')
    
    for i in link_list:
        box = i.find('a')
        if box is not None:
            headline = box.text.strip()
            link = box.get('href')
            if 'http' not in link:
                link = base_url+link
            news_articles.append(('REWARIYAT',headline,link))
    success.append('REWARIYAT')      
except Exception as e:
    failure.append(('REWARIYAT',e))
    pass


#TIMESBULL

try:
    base_url = "https://www.timesbull.com/"
    url = "https://www.timesbull.com/jobs/news"
    res = requests.get(url, verify=False)
    soup = BeautifulSoup(res.text,"html.parser")

    content = soup.find('main', class_ = 'site-main')
    link_list = content.find_all('article')
    for i in link_list:
        con = i.find('h2')
        box = con.find('a')
        if box is not None:
            headline = box.text.strip()
            link = box.get('href')
            if 'http' not in link:
                link = base_url+link
            news_articles.append(('TIMESBULL',headline,link))
    success.append('TIMESBULL')      
except Exception as e:
    failure.append(('TIMESBULL',e))
#INDIATVNEWS

try:
    base_url = "https://www.indiatvnews.com/"
    url = "https://www.indiatvnews.com/education/career/"
    res = requests.get(url, verify=False)
    soup = BeautifulSoup(res.text,"html.parser")
    content = soup.find('div', class_ ='row lhsBox s_two_column pt20')
    link_list = content.find_all('ul', class_ = 'list')

    for i in link_list:
        lists = i.find_all('li')
        for j in lists:
            con = j.find('p')
            box = con.find('a')
            if box is not None:
                headline = box.text
                link = box.get('href')
                if 'http' not in link:
                    link = base_url+link
                news_articles.append(('INDIATVNEWS',headline,link))
    success.append('INDIATVNEWS')      
except Exception as e:
    failure.append(('INDIATVNEWS',e))

        
#LOKMAT

try:
    base_url = "https://www.lokmat.com/"
    url = "https://www.lokmat.com/career/"
    res = requests.get(url, verify=False)
    soup = BeautifulSoup(res.text,"html.parser")

    content = soup.find('section', class_ ='list-view')
    link_list = content.find_all('figure')
    for i in link_list:
        con = i.find('h2')
        box = con.find_all('a')
        if box[1] is not None:
            headline = box[1].text
            link = box[1].get('href')
            if 'http' not in link:
                link = base_url+link
        news_articles.append(('LOKMAT',headline,link))
    success.append('LOKMAT')      
except Exception as e:
    failure.append(('LOKMAT',e))
    pass
# Employment News
try:           
    url = 'http://employmentnews.gov.in/NewEmp/'                                 
    base_url = 'http://employmentnews.gov.in/NewEmp/Home1.aspx'
    res = requests.get(base_url)
    soup = BeautifulSoup(res.text, 'html.parser')
    newss = soup.find_all(class_='divBorder')
    for i in range(len(newss)):
        if i >= 3:
            success.append('Employment News')
        else:
            headline = newss[i].find('a').get_text().strip()[:999]
            link = url + newss[i].find('a').get('href')
            news_articles.append(('Employment News', headline, link))  
except Exception as e:
    failure.append(('Employment News', e))
    pass

# Hindustan Times
try:
    url = 'https://www.hindustantimes.com/education'
    base_url = 'https://www.hindustantimes.com/'
    name = "Hindustan times"
#     headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    content = requests.get(url)
#     print(content.status_code)
    soup = BeautifulSoup(content.text, "html.parser")
    headlines = soup.find_all('h3', class_ = 'hdg3')
    for line in headlines: 
        headline = line.find('a').text
        link = line.find('a').get('href')
        if link.startswith('http'):
            link = link
        else:
            link = base_url+link
        news_articles.append((name, headline, link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass


# Live Hindustan Job Alerts
try:
    url = 'https://www.livehindustan.com/career/jobs/news'
    base_url = 'https://www.livehindustan.com/career/jobs/news'
    name = "Live Hindustan"
    # headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    content = requests.get(url)
#     print(content.status_code)
    soup = BeautifulSoup(content.text, "html.parser")
    results = soup.find_all('a', class_ = 'card-sm')
    for result in results:
        headline = result.text
        link = result.get('href')
        if link.startswith('http'):
            link = link
        else:
            link = base_url+link
        news_articles.append((name, headline, link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

#sarkariresult

try:
    url = 'https://www.sarkariresult.com/'
    baseurl = 'https://www.sarkariresult.com/'
    res = requests.get(url)
    soup=BeautifulSoup(res.text,'html.parser')
    for div in soup.find_all('div',id='post')[:2]:
        for a in div.find_all('a')[:10]:
            text=a.text
            link=a['href']
            text=text.strip()
            link=link.strip()
            if 'http' not in link:
                link=baseurl+link
            news_articles.append(('sarkariresult',text,link))
    for div in soup.find_all('div',id='post')[3:7:3]:   
        for a in div.find_all('a')[:10]:
            text=a.text
            link=a['href']
            text=text.strip()
            link=link.strip()
            if 'http' not in link:
                link=baseurl+link  
            news_articles.append(('sarkariresult',text,link))
    success.append(('sarkariresult'))
except  Exception as e:
    failure.append(('sarkariresult',e))
    pass


#linking sky
try:
    Headline =[]
    Link=[]
    url = "https://linkingsky.com/"
    base_url = "https://linkingsky.com/"
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    results = soup.find_all("div", class_='col-sm-6')
    for var in results:
        var2 = var.find_all('li')
        for var3 in var2:
            headline = var3.text
            Headline.append(headline)
            link = var3.find('a', href=True).get('href').strip()
            Link.append(link)
            news_articles.append(('linking sky', headline, link))
    success.append(('linking sky'))
    # print(news_articles)
except Exception as e:
    failure.append(('linking sky ', e))
    pass

#SSC Adda
try :
    
    url = 'https://www.sscadda.com/'
    req = requests.get(url)

    all_cont = req.content
    document = BeautifulSoup(all_cont, 'html.parser')

    div1 = document.find_all("div",class_='wp-block-column new-icon')#.find_all('h2')#.get_text()#
    div2 = document.find_all("div",class_='wp-block-column')
    Sec = [div1,div2]

    for div in Sec:
        for i in div:
            try:
                Seg = i.find_all('ul', class_="lcp_catlist", id="lcp_instance_0")
                for j in Seg:
                    text = j.find_all('li')
                    for k in j:
                        link = k.find_all('a', href=True)[0].get("href").strip()
                        headline = k.get_text(strip =True).split(',')[0]
                        news_articles.append(('SSC Adda', headline, link))
                
            except Exception as e:
                failure.append(('SSC Adda', e))
                pass
    success.append('SSC Adda')
except Exception as e:
    failure.append(('SSC Adda',e))

#JAGRANJOSH(Govt)
try:
    news_articles=[]
    url = 'https://www.jagranjosh.com/articles-sarkari-naukri-government-jobs-1303378740'
    base_url = 'https://www.jagranjosh.com'
    name = "JAGRANJOSH(Govt)"
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    tags = soup.find('div', class_ = 'related-list article-list').find_all('li')
    base_url = 'https://www.jagranjosh.com'
    for tg in tags:
        try:
            headline = tg.h2.a.get('title')
            url = tg.h2.a.get('href')
            if url.startswith('https'):
                url  = url
            else:
                url = base_url+url
            news_articles.append((name, headline, url))
        except:
            pass
    success.append(name)
except Exception as e:
    failure.append((name, e))
    
#ODISHATV

try:
    base_url = "https://odishatv.in/"
    url = "https://odishatv.in/jobs"
    res = requests.get(url, verify=False)
    soup = BeautifulSoup(res.text,"html.parser")

    content = soup.find('div', class_ = 'listing-news-start')
    link_list = content.find_all('div', class_ = 'listing-result-news')
    for i in link_list:
        con = i.find_all('a')
        for j in con:
            box = j.find('h5')
            if box is not None:
                headline = j.text
                link = j.get('href')
                if 'http' not in link:
                    link = base_url+link
                news_articles.append(('ODISHATV',headline,link))
            else:
                continue
            
    success.append('ODISHATV')      
except Exception as e:
    failure.append(('ODISHATV',e))

#BENGALINEWS18

try:
    url = 'https://bengali.news18.com/job/'
    base_url = 'https://bengali.news18.com/'
    name = "BENGALINEWS18"
    content = requests.get(url)
#     print(content.status_code)
    soup = BeautifulSoup(content.text, "html.parser")
    results = soup.find('ul',  class_ ='jsx-696593263').find_all('a', class_="jsx-696593263")
    for result in results:
        headline = result.text
        link = result.get('href')
        if link.startswith('http'):
            link = link
        else:
            link = base_url+link
        news_articles.append((name, headline, link))
    
    results2 = soup.find_all('div', class_ = 'jsx-2852348614 blog_list_row')
    for result in results2:
        headline = result.find('a').text
        link = result.find('a').get('href')
        if link.startswith('http'):
            link = link
        else:
            link = base_url+link
        news_articles.append((name, headline, link))
    success.append(name)   
except Exception as e:
    failure.append((name,e))
    pass
 

#GUJARATINEWS18

 
try:
    base_url = "https://gujarati.news18.com/"
    url = "https://gujarati.news18.com/career/"
    res = requests.get(url, verify=False)
    soup = BeautifulSoup(res.text,"html.parser")
    content = soup.find('div', class_ = 'blog-list')
    link_list = content.find_all('div', class_ = 'blog-list-blog')
    for i in link_list[:5]:
        con = i.find('p')
        box = con.find('a')
        if box is not None:
            headline = box.text
            link = box.get('href')
            if 'http' not in link:
                link = base_url+link
            news_articles.append(('GUJARATINEWS18',headline,link))
    success.append('GUJARATINEWS18')      
except Exception as e:
    failure.append(('GUJARATINEWS18',e))
    
    
#KANNADANEWS18

try:
    url = 'https://kannada.news18.com/news/jobs'
    base_url = 'https://kannada.news18.com/news/jobs'
    name = "KANNADANEWS18"
    content = requests.get(url) 
#     print(content.status_code)
    soup = BeautifulSoup(content.text, "html.parser")
    
    results = soup.find('div',  class_ ='section-blog-left-img')
    headline = results.text
    link = results.find('a').get('href')
    if link.startswith('http'):
        link = link
    else:
        link = base_url+link
    news_articles.append((name, headline, link)) 
    
    results2 = soup.find('div',  class_ ='section-blog-left-img-list')
    headlines = results2.find_all('a')
    for line in headlines:
        headline = line.text
        link = line.get('href')
        if link.startswith('http'):
            link = link
        else:
            link = base_url+link
        news_articles.append((name, headline, link)) 
            
    results3 = soup.find_all('div', class_ = 'blog-list-blog')
    for result in results3:
        headline = result.text
        link = result.find('a').get('href')
        if link.startswith('http'):
            link = link
        else:
            link = base_url+link
        news_articles.append((name, headline, link))  
            
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

#TIMESOFINDIA
try:
    base_url = "https://timesofindia.indiatimes.com/"
    url = "https://timesofindia.indiatimes.com/education/jobs"
    res = requests.get(url, verify=False)
    soup = BeautifulSoup(res.text,"html.parser")
 
    content = soup.find('ul', id = 'content')
    link_list = content.find_all('li')
    for i in link_list[:10]:
        con = i.find('span', class_ = 'w_tle')
        if con is not None:
            box = con.find('a')
            if box is not None:
                headline = box.text
                link = box.get('href')
                if 'http' not in link:
                    link = base_url+link
                news_articles.append(('TIMESOFINDIA',headline,link))
    success.append('TIMESOFINDIA')      
except Exception as e:
    failure.append(('TIMESOFINDIA',e))

#Free Job Alert
try:
    name ='Free Job Alert'
    url = 'https://www.freejobalert.com/'

    # driver = webdriver.Edge(executable_path = 'D:\\edgedriver\\msedgedriver.exe')
    req = driver.get(url)
    time.sleep(2)
    document = BeautifulSoup(driver.page_source, 'html.parser')
    div1 = document.find('div',class_="gb-container gb-container-a2c5ed7b")
    if div1 is not None:
        div2 = div1.find_all("li") 
        if div2 is not None: 
            for y in div2:
                div3 = y.find('a')
                
                if div3 is not None:

                    # print(div3)
                    headline= div3.text
                    # print()
                    link=div3.get('href')
                    news_articles.append((name, headline, link))
                            # print((name, headline, link))
                    if name not in success:
                        success.append(name)   
                else :
                    failure.append((name, 'div1 is None')) 
        else :
            failure.append((name, 'div2 is None'))  
    else :
        failure.append((name, 'div1 is None'))            
except Exception as e:
    name ='Free Job Alert'
    failure.append((name, e))
    pass



driver.quit()

print('Successful Scrapers -', success)
print('Failed Scrapers -', failure)
df = pd.DataFrame(news_articles)

df.drop_duplicates(inplace = True) 
df['date'] = now.strftime("%Y-%m-%d %H:%M")
df.columns = ['source','title','link','date']

df.to_csv('/root/New_Scrapers/Prepp_scrapers/preppnewscraper_try.csv', index = False)
data = pd.DataFrame()
try:    
    data = pd.read_csv ('/root/New_Scrapers/Cd_scrapers/cd_main.csv')
except:
    pass
data = pd.concat([ data,df])

data.drop_duplicates(subset = ['title'], inplace = True)
data.to_csv('/root/New_Scrapers/Cd_scrapers/cd_main.csv', index = False)
print(df[df['source']=='Free Job Alert'].date.to_list())
print(data[(data['source']=='Free Job Alert') & (pd.to_datetime(data['date']).dt.date.astype(str) == now.strftime("%Y-%m-%d"))])
print("all done")


#REPUBLICWORLD

# try:
#     base_url = "https://www.republicworld.com/"
#     url = "https://www.republicworld.com/education/jobs"
#     res = requests.get(url, verify=False)
#     soup = BeautifulSoup(res.text,"html.parser")

#     content_1 = soup.find('div', class_ = 'sub-mrgnright sub-left-stories')
#     link_list_1 = content_1.find_all('article')
#     for i in link_list_1:
#         box = i.find('a')
#         if box is not None:
#             headline = box.text.strip()
#             link = box.get('href')
#             if 'http' not in link:
#                 link = base_url+link
#         news_articles.append(('REPUBLICWORLD',headline,link))

#     content_2 = soup.find('div', class_ = 'sub-mrgnright sub-right-stories')
#     link_list_2 = content_2.find_all('article')
#     for i in link_list_2:
#         box = i.find('a')
#         if box is not None:
#             headline = box.text.strip()
#             link = box.get('href')
#             if 'http' not in link:
#                 link = base_url+link
#         news_articles.append(('REPUBLICWORLD',headline,link))

#     content_3 = soup.find('div', class_ = 'channel-card-wrapper')
#     link_list_3 = content_3.find_all('article')
#     for i in link_list_3:
#         box = i.find('a')
#         if box is not None:
#             headline = box.find('h2').text.strip()
#             link = box.get('href')
#             if 'http' not in link:
#                 link = base_url+link
#         news_articles.append(('REPUBLICWORLD',headline,link))
        
#     success.append('REPUBLICWORLD')      
# except Exception as e:
#     failure.append(('REPUBLICWORLD',e))
#     pass

# News.careers-360
# try:
#     base_url = 'https://news.careers360.com'
#     url = 'https://news.careers360.com/latest?page=1'
#     res = requests.get(url)
#     soup = BeautifulSoup(res.text, 'html.parser')
#     newss = soup.find(class_="artiLis-MainBlock").find_all(class_='heading4')
#     for news in newss:
#         headline = news.find('a').get_text()
#         link = news.find('a').get('href')
#         link = base_url+link
#         if headline == '':
#             continue
#         else:
#             news_articles.append(('Careers-360 Jobs', headline[:999], link))
#     success.append('Careers-360 Jobs')
# except Exception as e:
#     failure.append(('Careers-360 Jobs', e))
#     pass

#Jagranjosh(govt)
# for i in range(1,4):
#     if i == 1:
#         try:
#             url = 'https://www.jagranjosh.com/articles-sarkari-naukri-government-jobs-1303378740-1'
#             base_url = 'https://www.jagranjosh.com'
#             name = "JAGRANJOSH(Govt)"
#             driver.get(url)
#             time.sleep(3)
#             new_notf = driver.find_elements(By.CLASS_NAME, "articlelanding_detail")
#             link_a = driver.find_elements(By.XPATH, '//*[@id="tag_Sample"]/div/div/h2/strong/a')

#             b = len(new_notf)
#             for j in range(b):
#                 text = new_notf[j].text.split('\n')
#                 link = link_a[j].get_attribute('href')
#                 news_articles.append((name, text[-1], link))
#             success.append(name)
#                 # print(news_articles)
#         except Exception as e:
#             failure.append((name, e))
#             pass
        
#     else:
#         try:
#             # 'https://www.jagranjosh.com/articles-sarkari-naukri-government-jobs-1303378740-1-p2'
#             url = 'https://www.jagranjosh.com/articles-sarkari-naukri-government-jobs-1303378740-1-p'+str(i)
#             base_url = 'https://www.jagranjosh.com'
#             name = "JAGARNJOSH"
#             driver.get(url)
#             time.sleep(3)
#             new_notf = driver.find_elements(By.CLASS_NAME,"articlelanding_detail")
#             link_a = driver.find_elements(By.XPATH,'//*[@id="tag_Sample"]/div/div/h2/strong/a')

#             b = len(new_notf)
#             for j in range(b):
#                 text = new_notf[j].text.split('\n')
#                 link = link_a[j].get_attribute('href')
#                 news_articles.append((name,text[-1],link))
#             success.append(name)
#                 # print(news_articles)
#         except Exception as e:
#             failure.append((name,e))
#             pass


#shiksha_sarkari_exams
# try:
#     url = 'https://www.shiksha.com/sarkari-exams/articles-st-21'
#     base_url = 'https://www.shiksha.com'
#     name = "shiksha_sarkari_exams"
#     content = requests.get(url)
#     soup = BeautifulSoup(content.text, "html.parser")
#     headlines = soup.find_all('h3', class_ = 'articleTitle')
#     for line in headlines: 
#         headline = line.find('a').text
#         link = line.find('a').get('href')
#         if link.startswith('http'):
#             link = link
#         else:
#             link = base_url+link
#         news_articles.append((name, headline, link))
#     success.append((name))
# except Exception as e:
#     failure.append((name,e))
#     pass

#TAMIL INDIAN EXPRESS


# try:
#     base_url = "https://tamil.indianexpress.com/"
#     url = "https://tamil.indianexpress.com/education-jobs/"
#     res = requests.get(url, verify=False)
#     soup = BeautifulSoup(res.text,"html.parser")

#     content = soup.find_all('div', class_ = 'wp-block-newspack-blocks-ie-stories')
#     for i in content[:10]:
#         link_list = i.find_all('div', class_ = 'entry-title')
#         for j in link_list:
#             box = j.find('a')
#             if box is not None:
#                 headline = box.text
#                 link = box.get('href')
#                 if 'http' not in link:
#                     link = url+link
#             news_articles.append(('TAMILINDIANEXPRESS',headline,link))
#     success.append('TAMILINDIANEXPRESS')      
# except Exception as e:
#     failure.append(('TAMILINDIANEXPRESS',e))
#     pass



#HARIBHOOMI

# try:
#     base_url = "https://www.haribhoomi.com/"
#     url = "https://www.haribhoomi.com/career"
#     res = requests.get(url, verify=False)
#     soup = BeautifulSoup(res.text,"html.parser")
#     content_1 = soup.find('div', class_ ='listing_main_level_top mtop15')

#     content_2 = soup.find('div', class_ ='listing_main_level_middle_tw_column mtop15')
#     link_list_1 = content_1.find_all('div',class_ = 'list_content')
#     link_list_2 = content_2.find_all('li',class_ = 'news_listing')
#     for i in link_list_1:
#         con  = i.find('h3')
#         box = con.find('a')
#         if box is not None:
#             headline = box.text
#             link = box.get('href')
#             if 'http' not in link:
#                 link = base_url+link
#         news_articles.append(('HARIBHOOMI',headline,link))
        
#     for i in link_list_2:
#         con  = i.find('h4')
#         box = con.find('a')
#         if box is not None:
#             headline = box.text
#             link = box.get('href')
#             if 'http' not in link:
#                 link = base_url+link
#         news_articles.append(('HARIBHOOMI',headline,link))
        
#     success.append('HARIBHOOMI')      
# except Exception as e:
#     failure.append(('HARIBHOOMI',e))
#     pass