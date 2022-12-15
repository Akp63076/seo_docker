import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
# from dotenv import load_dotenv
from bs4 import BeautifulSoup
from datetime import datetime
# import lxml
import csv
import requests
# import pymysql
import os
import urllib3
from zoneinfo import ZoneInfo

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

news_articles = []
success = []
failure = []

# load_dotenv()
now = datetime.now(tz=ZoneInfo('Asia/Kolkata'))
print (now.strftime("%Y-%m-%d %H:%M:%S"))

# options=Options()
# options.headless=True
# fp=webdriver.FirefoxProfile()
# fp.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36")
# fp.set_preference("dom.webnotifications.enabled", False)
# fp.set_preference("network.cookie.cookieBehavior", 2)

# Driver Initiated
# driver = webdriver.Firefox(options=options)

# Selenium Scrapers Started


# Selenium Scrapers Ended
# Driver Quit
# driver.quit()

# Request Scrapers Started



# Assam University
# try:
#     base_url = "http://www.aus.ac.in"
#     url = "http://www.aus.ac.in/notices/"
#     res = requests.get(url)
#     soup = BeautifulSoup(res.text, "html.parser")
#     results = soup.find("div", class_="entry-content").find_all("li")
#     for result in results:
#         headline = result.find('a').text.strip()
#         link= result.a.get("href").strip()
#         news_articles.append(('Assam University',headline,link))
#     success.append('Assam University')
# except Exception as e:
#     failure.append(('Assam University',e))
#     pass

# Shekhawati University
try:
    base_url = "http://www.shekhauni.ac.in/"
    url = "http://www.shekhauni.ac.in/allnews.aspx"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("table", class_="table table-striped table-bordered table-hover")
    for result in results.find_all("a"):
        headline = result.text.strip()
        link= base_url+result.get("href").strip()
        news_articles.append(('Shekhawati University',headline,link))
    success.append('Shekhawati University')
except Exception as e:
    failure.append(('Shekhawati University',e))
    pass

#TNTEU
try:
    base_url = "http://www.tnteu.ac.in/"
    url = "http://www.tnteu.ac.in/notifications.php?nid=5"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("ul", class_="list prim list-ok").find_all("li")
    for result in results:
        headline = result.find("a").text.strip()
        link= result.find("a").get("href").strip().replace(' ','%20')
        if 'http' not in link:
            link=base_url+link
            news_articles.append(('TNTEU',headline,link))
        else:
            news_articles.append(('TNTEU',headline,link))
    success.append('TNTEU')
except Exception as e:
    failure.append(('TNTEU',e))
    pass

# Utkal University
try:
    base_url = "https://utkaluniversity.ac.in"
    url = "https://utkaluniversity.ac.in/#"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")    
    results = soup.find("div",id="example").find_all('a')    
    for result in results:
        headline = result.text.strip().replace('\r\n','')
        link= result.get("href").strip()
        news_articles.append(('Utkal University',headline,link))
    success.append('Utkal University')
except Exception as e:
    failure.append(('Utkal University',e))
    pass

# Jamia Millia Islamia
try:
    base_url = 'https://www.jmi.ac.in'
    url = 'https://www.jmi.ac.in/bulletinboard/NoticeOfficialorder/latest/1'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    results = soup.find_all('tr')
    for result in results:
        if result.find('td', style = 'border:1px solid #ddd; text-align:center;font-weight:bold;width: 100px;'):
            continue
        else:
            headline = result.find('a').string
            link = base_url + result.find('a').get('href')
            news_articles.append(('Jamia Millia Islamia',headline,link))
    success.append('Jamia Millia Islamia')
except Exception as e:
    failure.append(('Jamia Millia Islamia',e))
    pass

# University of Mysore
try:
    base_url = 'http://uni-mysore.ac.in'
    url = 'http://uni-mysore.ac.in/english-version/latest-news'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    results = soup.find_all('h2', class_ = 'title')
    for result in results:
        headline = result.find('a').string
        link = base_url + result.find('a').get('href')
        news_articles.append(('University of Mysore',headline,link))
    success.append('University of Mysore')
except Exception as e:
    failure.append(('University of Mysore',e))
    pass

# Dibrugarh University
try:
    url = 'https://dibru.ac.in/news/'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    results = soup.find_all('div', class_ = 'gdlr-core-blog-list-frame gdlr-core-skin-e-background')
    for result in results:
        headline = result.find('a').string
        link = result.find('a').get('href')
        news_articles.append(('Dibrugarh University',headline,link))
    success.append('Dibrugarh University')
except Exception as e:
    failure.append(('Dibrugarh University',e))
    pass

# JNTUK
try:
    url = 'https://www.jntuk.edu.in/category/notifications/'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    results = soup.find_all('div', id = 'cat_list')
    for result in results:
        headline = result.find('a').string[7:]
        link = result.find('a').get('href')
        news_articles.append(('JNTUK',headline,link))
    success.append('JNTUK')
except Exception as e:
    failure.append(('JNTUK',e))
    pass

# Nagarjuna University
try:
    base_url = 'https://www.nagarjunauniversity.ac.in/'
    url = 'https://www.nagarjunauniversity.ac.in/indexanu.html'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    results = soup.find_all('div', class_ = 'col-md-4 col-sm-4 categories_sub cats1')
    for result in results:
        headline = result.find('h3', class_ = 'mt-3').text.replace('\r\n\t\t\t\t\t\t\t\t', '')
        try:
            link = result.find('a').get('href')
        except:
            link = url
        if 'https' not in link:
            link=base_url+link
        if 'pdf' in link:
            link = link.replace(' ','%20')
            news_articles. append(('Nagarjuna University',headline,link))
    success.append('Nagarjuna University')
except Exception as e:
    failure.append(('Nagarjuna University',e))
    pass

# Ahmedabad University
try:
    base_url = 'https://ahduni.edu.in'
    url = 'https://ahduni.edu.in/news/'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    results = soup.find_all('div', class_ = 'col-xs-12 col-sm-6 col-md-4 d-flex align-items-stretch mb-4 mb-lg-5')
    for result in results:
        headline = result.find('p', class_ = 'card-title').text.strip()
        link = base_url + result.find('a').get('href').strip()
        news_articles.append(('Ahmedabad University',headline,link))
    success.append('Ahmedabad University')
except Exception as e:
    failure.append(('Ahmedabad University',e))
    pass

# IGU
try:
    url = 'http://igu.ac.in/2021/notice/'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    results = soup.find('div', class_ = 'elementor-widget-container').find_all('li')
    for result in results:
        headline = result.find('a').text
        link = result.find('a').get('href')
        news_articles.append(('IGU',headline,link))
    success.append('IGU')
except Exception as e:
    failure.append(('IGU',e))
    pass

# DAUNIV
try:
    base_url = "https://www.dauniv.ac.in/"
    url = "https://www.dauniv.ac.in/view-all/colleges"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("ul", class_="glance-p")
    for result in results.find_all("a"):
        headline = result.text
        link= result.get("href").strip()
        news_articles.append(('DAUNIV',headline,link))
    success.append('DAUNIV')
except Exception as e:
    failure.append(('DAUNIV',e))
    pass

# DBTAU
try:
   url = "https://dbatu.ac.in/"
   res = requests.get(url)
   soup = BeautifulSoup(res.text, "html.parser")
   results = soup.find('ul', class_='category-posts-internal')
   for result in results.find_all("a"):
       headline = result.text
       link= result.get("href").strip()
       news_articles.append(('DBTAU',headline,link))
   success.append('DBTAU')
except Exception as e:
   failure.append(('DBTAU',e))
   pass

#Jammu University
try:
    base_url = "http://jammuuniversity.ac.in/"
    url = "http://jammuuniversity.ac.in/announcements"
    res = requests.get(url)
    soup = BeautifulSoup(res.text,"html.parser")
    results = soup.find_all('span',class_="field-content")
    for result in results:
        headline=result.a.text
        link= "http://jammuuniversity.ac.in" + result.a.get('href')
        news_articles.append(('Jammu University',headline,link))
    success.append('Jammu University')
except Exception as e:
    failure.append(('Jammu University',e))
    pass

# Mangalore University
try:
   base_url = "https://mangaloreuniversity.ac.in"
   url = "https://mangaloreuniversity.ac.in/latest-home-news"
   res = requests.get(url)
   soup = BeautifulSoup(res.text,"html.parser")
   results = soup.find_all('span',class_="field-content")
   for result in results:
       headline=result.a.text
       link= result.a.get('href')
       if 'https' not in link:
           link = base_url+link
           news_articles.append(('Mangalore University',headline,link))
       else:
           news_articles.append(('Mangalore University',headline,link))
   success.append('Mangalore University')
except Exception as e:
   failure.append(('Mangalore University',e))
   pass

# Central University of Gujarat
try:
    base_url= "https://www.cug.ac.in/"
    url = "https://www.cug.ac.in/latest.php"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("div", id = "nav-tabContent").find_all("li")
    for result in results:
        headline = result.find('i').findNextSibling(text=True).strip()[:-3]
        link= result.find("a").get("href").strip()
        if 'https' not in link:
            link=base_url+link
            news_articles.append(('Central University of Gujarat',headline,link))
        else:
            news_articles.append(('Central University of Gujarat',headline,link))
    success.append('Central University of Gujarat')
except Exception as e:
    failure.append(('Central University of Gujarat',e))
    pass

# Goa University
try:
    base_url= "https://www.unigoa.ac.in/"
    url = "https://www.unigoa.ac.in/goa-university-news-listing.php"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find_all("div", class_ = "res_listing")
    for result in results:
        headline = result.find("a").get_text().strip()
        link= result.find("a").get("href").strip()
        news_articles.append(('Goa University',headline,link))
    success.append('Goa University')
except Exception as e:
    failure.append(('Goa University',e))
    pass

# Hemchand National Gujrat University
try:
    base_url= "https://ngu.ac.in/"
    url = "https://ngu.ac.in/NewsDetails.aspx"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("aside", class_ = "no-featured").find_all("li")
    for result in results:
        headline = result.find("a").get_text().strip()
        link= result.find("a").get("href").strip().replace(' ','%20')
        if 'https' not in link:
            link=base_url+link
            news_articles.append(('NGU',headline,link))
        else:
            news_articles.append(('NGU',headline,link))
    success.append('NGU')
except Exception as e:
    failure.append(('NGU',e))
    pass

# IISER Mohali
# IISER Mohali
try:
    base_url= "https://www.iisermohali.ac.in"
    url = "https://www.iisermohali.ac.in/events/news/news-archive"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("div", class_ = "articleBody").find_all("li")
    for result in results:         
        headline = result.text
        link_box = result.find("a")
        if link_box is not  None:
            link = link_box.get("href").strip().replace(' ','%20')
            if 'http' not in link:
                link= base_url+link
        else:
            link = url
        news_articles.append(('IISER MOHALI',headline,link))    
    success.append('IISER Mohali')
except Exception as e:
    failure.append(('IISER Mohali',e))
    pass

# Janaknayak Chandrashekar University
try:
   base_url= "https://jncu.ac.in/"
   url = "https://jncu.ac.in/"
   res = requests.get(url)
   soup = BeautifulSoup(res.text, "html.parser")
   results = soup.find("div", class_ = "content").find_all("li")
   for result in results:
       headline = result.find("a").get_text().strip()
       link= result.find("a").get("href").strip()
       news_articles.append(('JNCU',headline,link))
   success.append('JNCU')
except Exception as e:
   failure.append(('JNCU',e))
   pass

# NIT Delhi
try:
   base_url= "https://nitdelhi.ac.in/"
   url = "https://nitdelhi.ac.in/?page_id=16711"
   res = requests.get(url)
   soup = BeautifulSoup(res.text, "html.parser")
   results = soup.find('table', class_='table table-striped table-responsive').find_all('tr')
   for result in results:
       headline = result.find('a').get_text().strip()
       link= result.find('a').get("href").strip()
       news_articles.append(('NIT Delhi', headline, link))
   success.append('NIT Delhi')
except Exception as e:
   failure.append(('NIT Delhi',e))
   pass

# # UNOM
# try:
#     base_url= "https://www.unom.ac.in/"
#     url = "https://www.unom.ac.in/index.php?route=administration/announcement"
#     res = requests.get(url)
#     soup = BeautifulSoup(res.text, "html.parser")
#     results = soup.find("div", class_ = "entry-content p-10").find_all("li")
#     for result in results:
#         headline = result.find("a").get_text().strip().replace('\xa0','')
#         link= result.find("a").get("href").strip().replace(' ','%20')
#         news_articles.append(('UNOM',headline,link))
#     success.append('UNOM')
# except Exception as e:
#     failure.append(('UNOM',e))
#     pass

# NIT Rourkela
try:          
    base_url = 'http://www.nitrkl.ac.in'
    url = 'https://www.nitrkl.ac.in/Home/Our-Latest-News/'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    newss = soup.find_all("div", {"class": "news-list-item"})
    for news in newss:
        headline = news.find('p').get_text().strip().replace('\r\n                        More>>','')
        link = news.find('a').get('href').strip()
        if 'https' not in link:
            link=base_url+link
        news_articles.append(('NIT Rourkela', headline, link))
    success.append('NIT Rourkela')
except Exception as e:
    failure.append(('NIT Rourkela', e))
    pass

# NIT Silcher
try:
    base_url = 'http://www.nits.ac.in'
    url = 'http://www.nits.ac.in/newsupdates.php'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    newss = soup.find_all('b')
    for news in newss:
        try :
            headline = news.text
            link = news.find('a').get('href').replace(' ','%20')
            if 'http' not in link:
                link = base_url + link
        except:
            None
        news_articles.append(('NIT Silcher', headline.strip()[:999], link))
    success.append('NIT Silcher')
except Exception as e:
    failure.append(('NIT Silcher', e))
    pass

# IIT Bhubaneswar
try:
    base_url = 'http://www.iitbbs.ac.in/'
    url = 'https://www.iitbbs.ac.in/news.php'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    newss = soup.find_all('ol')
    for news in newss[0].children:
        headline = news.find('a').text
        link = news.find('a').get('href')
        if 'http' not in link:
            link = base_url + link
        news_articles.append(('IIT Bhubaneswar', headline.strip()[:999], link))
    success.append('IIT Bhubaneswar')
except Exception as e:
    failure.append(('IIT Bhubaneswar', e))
    pass

# Veer Sundara Sai University of Technology
try:                                            
    domain = 'VSSUT'
    base_url = 'http://www.vssut.ac.in'
    url = 'https://www.vssut.ac.in/news-events.php'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    rows = soup.find_all('tr')
    head = ''
    for row in rows:
        check = 0
        col = row.find_all('td')
        try :
            for cell in col:
                if cell['data-title'] == 'Title':
                    head = cell.text
                if cell['data-title'] == 'View':
                    link = cell.find('a').get('href')
                    if 'http' not in link:
                        link = base_url + link
            check = 1
        except:
            None
        if check == 1:
            news_articles.append(('VSSUT', head[:999].strip(), link))
    success.append('VSSUT')
except Exception as e:
    failure.append(('VSSUT', e))
    pass


# Calcutta University
try:
   url = 'https://www.caluniv.ac.in/news/news.html'
   res = requests.get(url)
   soup=BeautifulSoup(res.text,'html.parser')
   headline = soup.find('div',class_='tender_table table-responsive').find_all('td')
   for news in headline:
       headline = news.get_text().strip()[:999]
   links = soup.find('div',class_='tender_table table-responsive').find_all('a',target='_blank')
   for l in links:
       link = l.get('href')
       news_articles.append(('Calcutta University',headline,link))
   success.append('Calcutta University')
except Exception as e:
   failure.append(('Calcutta University',e))
   pass

# CU Chandigarh
try:
    url = 'https://news.cuchd.in/'
    res = requests.get(url)
    soup=BeautifulSoup(res.text,'html.parser')
    headline = soup.find('div',class_='grid-posts').find_all(class_='post-title')
    for news in headline:
        headline = news.get_text().strip()[:999]
        link = news.find('a').get('href')
        news_articles.append(('CU',headline,link))
    success.append('CU')
except Exception as e:
    failure.append(('CU',e))
    pass

# SU Digital
try:
    url = 'https://su.digitaluniversity.ac/HomeContentDisplay.aspx?Content_Type=1'
    res = requests.get(url)
    soup=BeautifulSoup(res.text,'html.parser')
    headline = soup.find('div',id='mastercontentbox').find_all('li',class_='item')
    for news in headline:
        headline = news.get_text().strip()[:999]
        link = news.find('a').get('href').replace(' ','%20')
        news_articles.append(('SU Digital',headline,link))
    success.append('SU Digital')
except Exception as e:
    failure.append(('SU Digital',e))
    pass

# Ranchi University
try:
    url = 'https://www.ranchiuniversity.ac.in/'
    base_url = 'https://www.ranchiuniversity.ac.in'
    res = requests.get(url)
    soup=BeautifulSoup(res.text,'html.parser')
    results = soup.find_all('h6')
    for result in results:
        headline = result.get_text().strip()[:999]
        link_box = result.find('a')
        if link_box is not None:
            link = base_url + link_box.get('href').replace(' ','%20')
        else:
            link = url
        news_articles.append(('Ranchi University',headline,link))
    success.append('Ranchi University')
except Exception as e:
    failure.append(('Ranchi University',e))
    pass

# NFSU
try:
    url = 'https://www.nfsu.ac.in/news'
    res = requests.get(url)
    soup=BeautifulSoup(res.text,'html.parser')
    newss = soup.find_all('div',class_='gdlr-core-blog-full-head-right')
    for news in newss:
        headline = news.get_text().strip()[:999]
        link = news.find('a').get('href')
        news_articles.append(('NFSU',headline,link))
    success.append('NFSU')
except Exception as e:
    failure.append(('NFSU',e))
    pass

# SDSUV
try:
   url = 'https://www.sdsuv.ac.in/latest-news/'
   res = requests.get(url)
   soup=BeautifulSoup(res.text,'html.parser')
   newss = soup.find('div',class_='ResultDiv',style='width: 100%;').find_all('li')
   for news in newss:
       headline = news.get_text().strip()[14:]
       link = news.find('a').get('href')
       news_articles.append(('SDSUV',headline,link))
   success.append('SDSUV')
except Exception as e:
   failure.append(('SDSUV',e))
   pass

# MAFSU
try:
    url = 'http://www.mafsu.in/#news-tab'
    base_url = 'http://www.mafsu.in/'
    res = requests.get(url)
    soup=BeautifulSoup(res.text,'html.parser')
    newss = soup.find_all('a',target='_blank',style='color:Black; font-size:12px;')
    for news in newss:
        headline = news.get_text().strip()[:999]
        link = base_url + news.get('href').replace(' ','%20')
        news_articles.append(('MAFSU',headline,link))
    success.append('MAFSU')
except Exception as e:
    failure.append(('MAFSU',e))
    pass

# CU Kashmir
# try:
#     url = 'https://www.cukashmir.ac.in/'
#     res = requests.get(url)
#     soup=BeautifulSoup(res.text,'html.parser')
#     newss = soup.find_all('div',class_='labeltext')
#     for news in newss:
#         headline = news.get_text().strip().replace('\nRead More','')
#         link = news.find('a').get('href')
#         news_articles.append(('CU Kashmir',headline,link))
#     success.append('CU Kashmir')
# except Exception as e:
#     failure.append(('CU Kashmir',e))
#     pass

# IITD
try:
    base_url = "https://home.iitd.ac.in"
    url = "https://home.iitd.ac.in/news-all.php"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    results = soup.find('div',class_="container ar-container-top").find_all('div',class_="event-details p-15")
    for result in results:
        headline = result.text.replace('Read more','').strip()
        link= base_url+result.find('a').get("href").strip()
        news_articles.append(('IITD',headline,link))
    success.append('IITD')
except Exception as e:
    failure.append(('IITD',e))
    pass

# DCRUST
try:
    base_url = "http://www.dcrustm.ac.in/"
    url = "http://www.dcrustm.ac.in/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text,"html.parser")
    results = soup.find_all('div',class_="wpb_text_column wpb_content_element")
    for result in results:
        result=result.find_all('a')
        for r in result:
            headline=r.text.strip().replace('\xa0','')
            link= r.get('href')
            news_articles.append(('DCRUST',headline,link))
    success.append('DCRUST')
except Exception as e:
    failure.append(('DCRUST',e))
    pass

# IISER BPR
try:
    url = "https://www.iiserbpr.ac.in/"
    res = requests.get(url,verify=False)
    soup = BeautifulSoup(res.text,"html.parser")
    results = soup.find('ul',class_="newstick").find_all('li')
    for result in results:
        headline=result.text.replace('\n',' ').strip()
        link= result.a.get('href')
        news_articles.append(('IISER BPR',headline,link))
    success.append('IISER BPR')
except Exception as e:
    failure.append(('IISER BPR',e))
    pass

#Lala Lajpat Rai University
try:
    url = "https://www.luvas.edu.in"
    res = requests.get(url)
    soup = BeautifulSoup(res.text,"html.parser")
    results = soup.find('div',class_="tab-pane active").find_all('li')
    for result in results:
        headline=result.text.strip()
        link= result.a.get('href')
        news_articles.append(('Luvas',headline,link))
    success.append('Luvas')
except Exception as e:
    failure.append(('Luvas',e))
    pass

# VSKUB
try:
    base_url = "http://vskub.ac.in/"
    url = "http://vskub.ac.in/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text,"html.parser")
    results = soup.find('div',class_="testimonial_content_inner").find_all('a')
    for result in results:
        headline=result.text.strip()
        link= result.get('href').strip()
        news_articles.append(('VSKUB',headline,link))
    success.append('VSKUB')
except Exception as e:
    failure.append(('VSKUB',e))
    pass

#IISER KOLKATA
try:
    base_url = "https://www.iiserkol.ac.in"
    url = "https://www.iiserkol.ac.in/web/en/#gsc.tab=0"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find('div',class_="col-md-12").find_all('li')
    for result in results:
        headline=result.text
        link= result.find('a').get("href").strip()
        if 'http' in link:
                 link=link
        else:
            link= url+link
        news_articles.append(('IISER kolkata',headline,link))
    success.append('IISER kolkata')
except Exception as e:
    failure.append(('IISER kolkata',e))
    pass

# Davangere University
try:
    base_url = "http://davangereuniversity.ac.in/"
    url = "http://davangereuniversity.ac.in/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find('div',class_="mtphr-dnt-tick-contents").find_all('a')
    for result in results:
        headline=result.text
        link= result.get("href").strip()
        news_articles.append(('Davangere University',headline,link))
    success.append('Davangere University')
except Exception as e:
    failure.append(('Davangere University',e))
    pass

# MZU :Mizoram University
try:
    url = "https://mzu.edu.in/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find_all("article")
    for result in results:
        result=result.find_all('h2')
        for r in result:
            headline=r.text
            link= r.a.get("href")
        news_articles.append(('MZU',headline,link))
    success.append('MZU')
except Exception as e:
    failure.append(('MZU',e))
    pass

# VKSU :Veer Kunwar Singh University
try:
    base_url = "http://vksu.ac.in"
    url = "http://vksu.ac.in/notices-announcement/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("div", class_="post_content").find_all('h2')
    for result in results:
        headline = result.a.text
        link= result.a.get("href").strip()
        news_articles.append(('VKSU',headline,link))
    success.append('VKSU')
except Exception as e:
    failure.append(('VKSU',e))
    pass

# MNIT
# try:
#     url = 'http://www.mnit.ac.in/news/newsall.php?type=latest'
#     base_url = 'http://www.mnit.ac.in/'
#     res = requests.get(url)
#     soup=BeautifulSoup(res.text,'html.parser')
#     results = soup.find('ol',style='list-style:none; padding:0px 0px 0px 10px; list-style-position:outside; 	font-size:12px; font-family:Verdana, Arial, Helvetica, sans-serif;').find_all('a',target='_blank')
#     for result in results:
#         headline = result.get_text().strip()[:999]
#         link = base_url + result.get('href')
#         news_articles.append(('MNIT',headline,link))
#     success.append('MNIT')
# except Exception as e:
#     failure.append(('MNIT',e))
#     pass

# Makaut
try:
    base_url = "https://makautwb.ac.in/"
    url = "https://makautwb.ac.in/page.php?id=340"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("div", class_="col-md-9").find_all("a")
    for result in results:
        headline = result.text.strip()
        link = result.get("href").strip()
        if 'https' not in link:
            link= base_url+link
            news_articles.append(('Makaut',headline,link))
        else:
            news_articles.append(('Makaut',headline,link))
    success.append('Makaut')
except Exception as e:
    failure.append(('Makaut',e))
    pass

# IIT Guwahati
try:
    base_url = "https://www.iitg.ac.in/"
    url = "https://www.iitg.ac.in/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("div", class_="tab-pane fade in active").find_all("li")
    for result in results:
        headline = result.find('a').text.strip()
        link= result.a.get("href").strip()
        news_articles.append(('IIT Guwahati',headline,link))  
    success.append('IIT Guwahati')
except Exception as e:
    failure.append(('IIT Guwahati',e))
    pass

# GBU
try:
    url = "https://www.gbu.ac.in/"
    base_url = 'https://www.gbu.ac.in'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("ul", class_="list-group list-group-flush")
    for result in results.find_all("li"):
        headline = result.a.text.strip()
        link= base_url+result.a.get("href").strip().replace(' ','%20')
        news_articles.append(('GBU',headline,link))
    success.append('GBU')
except Exception as e:
    failure.append(('GBU',e))
    pass

# CU Jammu
try:
    url = "http://www.cujammu.ac.in//Default.aspx?artid=0&type=printallevents&prvtyp=site&option=s"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("div", class_="boxes-size")
    for result in results.find_all("a"):
        headline = result.text.strip()
        link = result.get("href").strip()
        news_articles.append(('CU Jammu', headline, link))
    success.append('CU Jammu')
except Exception as e:
    failure.append(('CU Jammu', e))
    pass

# Bodoland
try:
    url = "https://www.bodolanduniversity.ac.in/"
    res = requests.get(url, verify=False)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("div", id="div1", class_="targetDiv")
    for result in results.find_all("a"):
        headline = result.text.strip()
        link = url + result.get("href").strip().replace(' ','%20')
        news_articles.append(('Bodoland', headline, link))
    success.append('Bodoland')
except Exception as e:
    failure.append(('Bodoland', e))
    pass


# Kufos
try:
    url = "http://kufos.ac.in/"
    res = requests.get(url, verify=False)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("marquee", class_="kufos-marquee", style=" margin-top: 1px;")
    for result in results.find_all("a"):
        headline = result.text.strip()
        link = result.get("href").strip()
        if headline !='':
            news_articles.append(('Kufos', headline, link))
    success.append('Kufos')
except Exception as e:
    failure.append(('Kufos', e))
    pass

# IIT Bombay
try:
    base_url = "https://www.iitb.ac.in"
    url = "https://www.iitb.ac.in/en/all-news"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("div", class_="view-content")
    for result in results.find_all("a"):
        headline = result.text
        link= base_url + result.get("href").strip()
        news_articles.append(('IIT Bombay',headline,link))
    success.append('IIT Bombay')
except Exception as e:
    failure.append(('IIT Bombay',e))
    pass

# Aditi Mahavidyalaya
# try:  
#     url = 'http://aditi.du.ac.in/index.php/newsread/'
#     res = requests.get(url)
#     soup = BeautifulSoup(res.text, 'html.parser')
#     results = soup.find_all('div', class_ = 'panel panel-default')
#     for result in results:
#         headline = result.find('h4', class_ = 'panel-title').text.strip()
#         link = result.find('a').get('href')
#         news_articles.append(('Aditi Mahavidyalaya',headline,link))
#     success.append('Aditi Mahavidyalaya')
# except Exception as e:
#     failure.append(('Aditi Mahavidyalaya',e))
#     pass

# Kaziranga University
# try:
#     base_url = 'https://www.kazirangauniversity.in'
#     url = 'https://www.kazirangauniversity.in/show/news/KU/1'
#     res = requests.get(url)
#     soup = BeautifulSoup(res.text, 'html.parser')
#     results = soup.find_all('div', class_ = 'col-md-3')
#     for result in results:
#         headline = result.find('h3').text
#         link = base_url + result.find('a').get('href')
#         news_articles.append(('Kaziranga University',headline,link))
#     success.append('Kaziranga University')
# except Exception as e:
#     failure.append(('Kaziranga University',e))
#     pass

# BPUT
try:
    base_url = 'http://www.bput.ac.in/'
    url = 'http://www.bput.ac.in/news.php'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    results = soup.find_all('tr')
    for result in results:
        headline = result.find('a').text.strip()
        link = result.find('a').get('href')
        if 'https' not in link:
            link = base_url+link
        news_articles.append(('BPUT',headline,link))
    success.append('BPUT')
except Exception as e:
    failure.append(('BPUT',e))
    pass

# CUSAT
try:
    base_url = 'https://cusat.ac.in'
    url = 'https://cusat.ac.in/news'
    res = requests.get(url, verify = False)
    soup = BeautifulSoup(res.text, 'html.parser')
    results = soup.find_all('div', class_ = 'ho-ev-link pg-eve-desc')
    for result in results:
        headline = result.find('a').text.strip()
        link = base_url + result.find('a').get('href')
        news_articles.append(('CUSAT',headline,link))
    success.append('CUSAT')
except Exception as e:
    failure.append(('CUSAT',e))
    pass

# MNNIT
try:
    base_url = 'http://www.mnnit.ac.in/'
    url = 'http://www.mnnit.ac.in/#login_form'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    results = soup.find('div', class_ = 'popup').find_all('p')
    for result in results:
        headline = result.find('a').text.strip()
        link = base_url + result.find('a').get('href')
        news_articles.append(('MNNIT',headline,link))
    success.append('MNNIT')
except Exception as e:
    failure.append(('MNNIT',e))
    pass

# NITIE
try:
    base_url = 'https://www.nitie.ac.in'
    url = 'https://www.nitie.ac.in/news'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    results = soup.find('div', class_ = 'view-content').find_all('h3', class_ = 'field-content')
    for result in results:
        headline = result.find('a').text
        link = base_url + result.find('a').get('href')
        news_articles.append(('NITIE',headline,link))
    success.append('NITIE')
except Exception as e:
    failure.append(('NITIE',e))
    pass

# Rajiv gandhi Institute of Health Sciences, Karnataka
try:
    base_url = 'http://www.rguhs.ac.in/'
    url = 'http://www.rguhs.ac.in/'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    newss = soup.find_all("td", {"class": "n12n"})
    for news in newss:
        try :
            link = news.find('a').get('href').replace(' ','%20')
            headline = news.text.strip()
        except:
            None
        if 'http' not in link:
                link = base_url + link
        news_articles.append(('RGUHS', headline, link))
    success.append('RGUHS')
except Exception as e:
    failure.append(('RGUHS', e))
    pass

# Atal Bihari Vajpayee IIITM Gwalior
try:
    base_url = 'http://www.iiitm.ac.in'
    url = 'https://www.iiitm.ac.in/index.php/en/component/content/category/79-latest-news?Itemid=437'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    newss = soup.find_all("div", {"class": "items-row"})
    for news in newss:
        data = news.find('h2')
        head = data.find('a').text.strip()
        link = data.find('a').get('href')
        if 'http' not in link:
                link = base_url + link
        news_articles.append(('IIITM', head[:999], link))
    success.append('IIITM')
except Exception as e:
    failure.append(('IIITM', e))
    pass

# Institute of Engineering and Management
try:
    base_url = 'https://iem.edu.in'
    url1 = 'https://iem.edu.in/tag/university-daily-news/'
    url2 = 'https://iem.edu.in/tag/bulletin-board/'
    res1 = requests.get(url1)
    res2 = requests.get(url2)

    soup1 = BeautifulSoup(res1.text, 'html.parser')
    soup2 = BeautifulSoup(res2.text, 'html.parser')

    newss1 = soup1.find_all('h1')
    newss2 = soup2.find_all('h1')
    
    for news in newss1:
        try :
            headline = news.find('a').text.strip()
            link = news.find('a').get('href')
        except:
            None
        if 'http' not in link:
                link = base_url + link
        news_articles.append(('IEM Kolkata', headline, link))
        
    for news in newss2:
        try :
            headline = news.find('a').text.strip()
            link = news.find('a').get('href')
        except:
            None
        if 'http' not in link:
                link = base_url + link
        news_articles.append(('IEM Kolkata', headline, link))
        
    success.append('IEM Kolkata')
except Exception as e:
    failure.append(('IEM Kolkata', e))
    pass

# Chennai Institute of Technology
try:
    base_url = 'https://www.citchennai.edu.in/'
    url1 = 'https://www.citchennai.edu.in/latestnews/'
    url2 = 'https://www.citchennai.edu.in/upcoming-events/'
    url3 = 'https://www.citchennai.edu.in/announcements/'
    res1 = requests.get(url1)
    res2 = requests.get(url2)
    res3 = requests.get(url3)

    soup1 = BeautifulSoup(res1.text, 'html.parser')
    soup2 = BeautifulSoup(res2.text, 'html.parser')
    soup3 = BeautifulSoup(res3.text, 'html.parser')

    data1 = soup1.find_all("ul", {"class": "news-li"})[0]
    data2 = soup2.find_all("ul", {"class": "news-li"})[0]
    data3 = soup3.find_all("ul", {"class": "news-li"})[0]

    newss1 = data1.find_all('li')
    newss2 = data2.find_all('li')
    newss3 = data3.find_all('li')

    for news in newss1:
        headline = news.find('a').text.strip()
        link = news.find('a').get('href')
        news_articles.append(('CIT Chennai', headline, link))

    for news in newss2:
        headline = news.find('a').text.strip()
        link = news.find('a').get('href')
        news_articles.append(('CIT Chennai', headline, link))

    for news in newss3:
        headline = news.find('a').text.strip()
        link = news.find('a').get('href')
        news_articles.append(('CIT Chennai', headline, link))

    success.append('CIT Chennai')
except Exception as e:
    failure.append(('CIT Chennai', e))
    pass

# Thiruvalluvar University
try:
    name="Thiruvalluvar University"
    base_url = "https://www.tvu.edu.in"
    url = "https://www.tvu.edu.in/admission/circular/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    results = soup.find('ul',class_="list").find_all('a')
    for result in results:
        headline = result.text.strip()
        link= result.get("href")
        if headline != '':
            news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# KRU
try:
    name="KRU"
    base_url = "https://kru.ac.in/"
    url = "https://kru.ac.in/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    results = soup.find_all('div',class_="title_small_post")
    for result in results:
        headline = result.text.strip().replace('Download','')
        link= result.find('a').get("href")
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# Vikram University
try:
    name="Vikram University"
    base_url = "https://vikramuniv.ac.in"
    url = "https://vikramuniv.ac.in/index.php/en/information-notification/academic-notice"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    results = soup.find_all('td',class_="list-title")
    for result in results:
        headline = result.text.strip()
        link= base_url+result.find('a').get("href")
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# JNU
try:
    name="JNU"
    base_url = "http://www.jnu.ac.in"
    url = "http://www.jnu.ac.in/notices"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    results = soup.find('table',class_="views-table views-view-table cols-4").find_all('td',headers="view-title-table-column")
    for result in results:
        headline = result.text.strip()
        link=result.find('a').get("href")
        if 'http' in link:
            link= link
        else:
            link= base_url+link
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# IISER TVM
try:
   name="IISER TVM"
   base_url = "http://www.jrrsanskrituniversity.ac.in"
   url = "https://www.iisertvm.ac.in/"
   res = requests.get(url)
   soup = BeautifulSoup(res.text, 'html.parser')
   results = soup.find_all('div',class_="card_row")
   for result in results[4:]:
       result=result.find_all('a')
       for r in result:
           headline = r.text
           link=r.get("href")
       news_articles.append((name,headline,link))
   success.append(name)
except Exception as e:
   failure.append((name,e))
   pass

#NIT DGP
try:
   name="NIT DGP"
   base_url = "https://nitdgp.ac.in"
   url = "https://nitdgp.ac.in/p/noticesnitd/general-2"
   res = requests.get(url)
   soup = BeautifulSoup(res.text, 'html.parser')
   results = soup.find('ul',class_="list-group list-gr").find_all('a')
   for result in results:
       headline=result.text.strip()[12:]
       link = result.get('href')
       news_articles.append((name,headline,link))
   success.append(name)
except Exception as e:
   failure.append((name,e))
   pass

# MSIT
try:
    name="MSIT"
    base_url= "https://www.msit.in"
    url = "https://www.msit.in/latest_news"
    res = requests.get(url,verify = False)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("div", class_="tab-content").find_all('a')
    for result in results:
        headline= result.text
        link= base_url+result.get('href')
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# IIITL
try:
    name="IIITL"
    base_url= "https://iiitl.ac.in/"
    url = "https://iiitl.ac.in/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find_all('h3',class_="gdlr-core-blog-title gdlr-core-skin-title")
    for result in results:
        headline= result.text.strip()
        link= result.find('a').get('href')
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

#IITRPR
try:
   name="IITRPR"
   base_url= "https://www.iitrpr.ac.in/"
   url = "https://www.iitrpr.ac.in/"
   res = requests.get(url)
   soup = BeautifulSoup(res.text, "html.parser")
   results = soup.find_all('p',align="justify")
   for result in results:
       headline= result.text
       link= result.find('a').get('href')
       if 'https' not in link:
           link=base_url+link
       news_articles.append((name,headline,link))
   success.append(name)
except Exception as e:
   failure.append((name,e))
   pass

#New Horizon College of Engineering-NHCE
try:
    name="NHCE"
    base_url= "https://newhorizonindia.edu"
    url = "https://newhorizonindia.edu/nhengineering/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find_all('h4',class_="title")
    for result in results:
        headline= result.text.strip()
        link= result.find('a').get('href')
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# IIMU
try:
    name="IIMU"
    base_url= "https://www.iimu.ac.in"
    url = "https://www.iimu.ac.in/media/news"
    res = requests.get(url,verify=False)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find_all('div',class_="evetntitle")
    for result in results:
        result=result.find_all('a')
        for r in result:
            headline= r.text.strip()
            link= r.get('href')
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

#XISS
try:
    name="XISS"
    base_url= "http://www.xiss.ac.in/"
    url = "http://www.xiss.ac.in/#"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("div", class_="news-section").find_all('a')
    for result in results:
        headline = result.text
        link= result.get("href").strip()
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# NIT Sikkim
try:                                            
    domain = 'NIT Sikkim'
    url = 'https://nitsikkim.ac.in/'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    data = soup.find_all("div", {"id": "notice"})[0]
    newss = data.find_all('li')
    for news in newss:
        headline = news.find('a').text
        link = news.find('a').get('href')
        news_articles.append((domain, headline, link))
    success.append(domain)
except Exception as e:
    failure.append((domain, e))
    pass

# NIT Mizoram
try:                                            
    domain = 'NIT Mizoram'
    base_url = 'https://www.nitmz.ac.in/'
    url = 'https://www.nitmz.ac.in/ViewAllNewsAndEvents.aspx?sNewsNotice=AllNews'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    data = soup.find_all("div", {"id": "ctl00_ContentPlaceHolder_Main_NewsEvent"})[0]
    newss = data.find_all('td',{'class':'setNewsNotice'})
    for news in newss:
        content = news.find('p')
        try :
            headline = content.find('a').text
            link = content.find('a').get('href')
        except:
            headline = content.text
            link = url
        if 'http' not in link:
            link = base_url+link
        news_articles.append((domain, headline, link))
    success.append(domain)
except Exception as e:
    failure.append((domain, e))
    pass

# FISAT
try:                                            
    domain = 'FISAT'
    base_url = 'https://www.fisat.ac.in/'
    url = 'https://www.fisat.ac.in/'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    data = soup.find_all("div", {"id": "News"})[0]
    newss = data.find_all('li')
    for news in newss:
        content = news.find('h4')
        head = content.find('a').text
        link = content.find('a').get('href')
        if 'http' not in link:
            link = base_url+link
        news_articles.append((domain, head[:999], link))
    success.append(domain)
except Exception as e:
    failure.append((domain, e))
    pass

# VNIT
try:
    url = "https://vnit.ac.in/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("div", class_="scroll-box")
    for result in results.find_all("a"):
        headline = result.text.strip()
        link= result.get("href").strip()
        news_articles.append(('VNIT',headline,link))
    success.append('VNIT')
except Exception as e:
    failure.append(('VNIT',e))
    pass

# PSITCHE
try:
    base_url = "https://psitche.ac.in/che.in/"
    url = "https://psitche.ac.in/che.in/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("div", class_="col-lg-8")
    for result in results.find_all("a"):
        headline = result.text.strip()
        link = base_url + result.get("href").strip()
        news_articles.append(('PSITCHE', headline, link))
    success.append('PSITCHE')
except Exception as e:
    failure.append(('PSITCHE', e))
    pass

# IIT Madras
try:
    name="IIT Madras"
    base_url="https://www.iitm.ac.in"
    url = "https://www.iitm.ac.in/happenings/IITM-news"
    res = requests.get(url,verify =False)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find_all("div",class_="col-sm-4")
    for result in results[1:]:
        result=result.find_all('a')
        for r in result:
                headline=r.get('title')
                link=base_url+r.get('href')
                news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# TMU
try:
    name="TMU"
    url = "https://www.tmu.ac.in/news"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find_all("div",class_="post-content" )
    for result in results:
        result=result.find_all('a')
        for r in result:
            headline = r.text
            link= r.get("href")
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# CURAJ
try:
    name="CURAJ"
    base_url = "http://www.curaj.ac.in"
    url = "http://www.curaj.ac.in/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find_all('div',class_="newsbx")
    for result in results:
        headline = result.text.replace('\n',' ').strip()
        link= base_url+result.find('a').get("href")
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# MMYVV
try:
    name="MMYVV"
    url = "http://www.mmyvv.com/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find('div',class_="myclass").find_all('li')
    for result in results:
        headline = result.text.strip()
        link=url+result.find('a').get("href").replace(' ','%20')
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# NBU
try:
    name="NBU"
    base_url = "https://www.nbu.ac.in"
    url = "https://www.nbu.ac.in/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find_all('div',class_="meta group")
    for result in results[:10]:
        headline = result.find('a').text.strip()
        link=base_url+result.find('a').get("href")
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# UOK
try:
    name="UOK"
    url = "https://www.uok.ac.in/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find_all('div',class_="col-md-9")
    for result in results:
        headline = result.text.strip()
        link=url+result.find('a').get("href")
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# VIDYASAGAR
try:
    name="Vidyasagar"
    url = "http://www.vidyasagar.ac.in/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find('div',class_="col-md-6 h6 text-left").find_all('a')
    for result in results:
        headline = result.text.strip().replace('.','').strip()
        link=result.get("href")
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# BIT Mesra
try:
    name="BIT mesra"
    base_url="https://www.bitmesra.ac.in"
    url = "https://www.bitmesra.ac.in/Display_Archive_News_List09398FGDr?cid=1"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find_all('div',class_="widget-inner")
    for result in results:
        result=result.find_all('a')
        for r in result:
            headline = r.text.strip()
            link=r
            if 'href' in link.attrs:
                    link=r.get('href')
            else:
                link=link.get('onclick').replace('return makePopUp(\'','')
                link=base_url+link.replace("','50','250','900','600')","").replace(' ','%20')
            news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# KIIT
try:
    name="KIIT"
    url = "https://news.kiit.ac.in/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find_all('h2',class_="title")
    for result in results:
        headline = result.text.replace('\n',' ').strip()
        link=result.find('a').get("href")
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# IIT BHU
try:
    name="IIT Bhu"
    base_url='https://www.iitbhu.ac.in'
    url = "https://www.iitbhu.ac.in/news_notifications"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find('div',class_="field-items").find_all('a')
    for result in results[:10]:
        headline = result.text.replace('\n',' ').strip()
        link=result.get("href")
        if 'http' in link:
                link=link
        else:
                link= base_url+link
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# NITH
try:
    name="NITH"
    base_url='http://www.nith.ac.in'
    url = "http://www.nith.ac.in/all-announcements"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find('table').find_all('a')
    for result in results[:10]:
        headline = result.text.replace('\n',' ').strip()
        link=result.get("href")
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# CRRIT
try:
    name="CRRIT"
    base_url = "http://www.crritonline.com"
    url = "http://www.crritonline.com/LatestNews.aspx"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find_all("div", class_="latest-box")
    for result in results:
        result=result.find_all('p')
        for r in result[3::4]:
            headline=r.text.strip()
            link=base_url+r.a.get("href").strip().replace(' ','%20')
            news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# RV College
try:
    name='RV College'
    base_url = "https://www.rvce.edu.in"
    url = "https://www.rvce.edu.in/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("div", class_="block block--block block--block-33").find_all('a')
    for result in results:
        headline = result.text.replace('\xa0','')
        link= result.get("href")
        if 'http' in link:
            link=link
        else:
            link= base_url+link
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# SPCE
try:
    name="SPCE"
    base_url='https://www.spce.ac.in/'
    url = "https://www.spce.ac.in/old%20notices.php"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find('tbody').find_all('a')
    for result in results[1:11]:
        headline = result.text.replace('\n',' ').strip()
        link=base_url+result.get("href").replace(' ','%20')
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# RGUKT
try:
    name="RGUKT"
    base_url='https://www.rgukt.ac.in/'
    url = "https://www.rgukt.ac.in/news-updates.html"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("table", class_="table").find_all("td")
    for result in results:
        headline=result.find("a").text.strip()
        link=result.a.get("href")
        if 'https' in link:
            link=link
        else:
            link= base_url+link
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# Sonatech
try:
   name="Sonatech"
   base_url = "https://www.sonatech.ac.in/"
   url = "https://www.sonatech.ac.in/"
   res = requests.get(url)
   soup = BeautifulSoup(res.text, "html.parser")
   results = soup.find("div", class_="anouncement-list scrollable")
   for result in results.find_all("a"):
       headline = result.text.strip()
       link= result.get("href")
       if 'https' in link:
           link=link
       else:
           link= base_url+link
       news_articles.append((name,headline,link))
   success.append(name)
except Exception as e:
   failure.append((name,e))
   pass

# IIM Kashipur
try:                                            
    domain = 'IIM Kashipur'
    url = 'http://www.iimkashipur.ac.in/'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    newss = soup.find_all("ul", {"class": "events"})
    for news in newss:
        headline = news.find('a').text.strip()
        link = news.find('a').get('href')
        if 'http' not in link:
            link = base_url+link
        news_articles.append((domain, headline, link))
    success.append(domain)
except Exception as e:
    failure.append((domain, e))
    pass

# COEP
try:
    base_url = "https://www.coep.org.in"
    url = "https://www.coep.org.in/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("table", class_="views-table cols-2").tbody
    for result in results.find_all("a"):
        headline = result.text.strip()
        link = base_url + result.get("href").strip()
        news_articles.append(('COEP', headline, link))
    success.append('COEP')
except Exception as e:
    failure.append(('COEP', e))
    pass

# RMKEC
try:
    base_url = "http://www.rmkec.ac.in/"
    url = "http://www.rmkec.ac.in/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("div", class_="popular")
    for result in results.find_all("div", class_="media"):
        headline = result.a.text
        link =  result.a.get("href").strip()
        news_articles.append(('RMKEC', headline, link))
    success.append('RMKEC')
except Exception as e:
    failure.append(('RMKEC', e))
    pass
# SVNIT
try:
    base_url = "https://www.svnit.ac.in/"
    url = "https://www.svnit.ac.in/web/notice_events_tenders.php?tag=notice"
    res = requests.get(url, verify = False)
    soup = BeautifulSoup(res.text, "html.parser")
    results= soup.find_all("td", class_="tablefont")
    for result in results[:10]:
        headline = result.a.text.strip()
        link= result.a.get("href").replace(' ','%20').strip()
        news_articles.append(('SVNIT',headline,link))
    success.append('SVNIT')
except Exception as e:
    failure.append(('SVNIT',e))
    pass

# ISI
try:
    base_url = "https://www.isical.ac.in/"
    url = "https://www.isical.ac.in/news"
    res = requests.get(url, verify = False)
    soup = BeautifulSoup(res.text, "html.parser")
    results= soup.find_all("div", class_="event-details")
    for result in results:
        headline = result.a.text.replace('\n','').strip()
        link= result.a.get("href").strip()
        if link!='':
            news_articles.append(('ISI',headline,link))
    success.append('ISI')
except Exception as e:
    failure.append(('ISI',e))
    pass

# Manuu
try:
   name="Manuu"
   base_url= "https://manuu.ac.in"
   url = "https://manuu.ac.in/Eng-Php/index-english.php"
   res = requests.get(url)
   soup = BeautifulSoup(res.text, "html.parser")
   results = soup.find("div",id="t7").find_all('a')
   for r in results[:10]:
       headline=r.text.strip()
       link=r.get('href')
       if 'http' in link:
           link=link.replace('..','')
       else:
           link=base_url+link.replace('..','')
       news_articles.append((name,headline,link))
   success.append(name)
except Exception as e:
   failure.append((name,e))
   pass

# Fakir Mohan University
try:
    name="FMU"
    url = "http://www.fmuniversity.nic.in/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("div",class_="tab-pane active").find_all('a')
    for r in results[1::2]:
        headline= r.text.strip().strip()
        link=base_url+r.get('href')
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# DEI
try:
    name="DEI"
    base_url= "https://www.dei.ac.in/"
    url = "https://www.dei.ac.in/dei/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    results_box = soup.find("div",id="gkbottombottom1", class_ = "gkCol gkColLeft")
    results = results_box.find_all('a')
    for result in results:
        headline= result.text
        link=base_url+result.get('href').replace(' ','%20')
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# Periyar University
try:
   name="Periyar University"
   base_url= "https://www.periyaruniversity.ac.in"
   url = "https://www.periyaruniversity.ac.in/AllNewsEvents.php"
   res = requests.get(url)
   soup = BeautifulSoup(res.text, "html.parser")
   results = soup.find_all("div",class_="NewsContent")#.find_all('a')
   for r in results[:10]:
       headline= r.text.replace('Prospectus','').replace('Application Link','')
       headline=headline.replace('Circular','').replace('Download','').replace('\n','').strip()
       link=r.find('a').get('href').replace(' ','%20')
       news_articles.append((name,headline,link))
   success.append(name)
except Exception as e:
   failure.append((name,e))
   pass

# HNBGU
try:
   name="HNBGU"
   base_url= "http://hnbgu.ac.in"
   url = "http://hnbgu.ac.in/"
   res = requests.get(url)
   soup = BeautifulSoup(res.text, "html.parser")
   results = soup.find("div",class_="views-element-container block block-views block-views-blockappointment-block-1").find_all('a')
   for r in results[:10]:
       headline= r.text.strip()
       link=base_url+r.get('href')
       news_articles.append((name,headline,link))
   success.append(name)
except Exception as e:
   failure.append((name,e))
   pass

# NIT Raipur
try:
   name="NIT Raipur"
   base_url= "http://www.nitrr.ac.in"
   url = "http://www.nitrr.ac.in/events.php"
   res = requests.get(url)
   soup = BeautifulSoup(res.text, "html.parser")
   iframe_src = "notice1.php"
   r = requests.Session().get(f"http://www.nitrr.ac.in/{iframe_src}")
   soup = BeautifulSoup(r.content, "html.parser")
   results = soup.find_all("h3",class_="entry-title entry-title_mod-a")
   for result in results[:10]:
           headline= result.text
           link=result.find('a').get('href')
           if 'http' in link:
               link=link
           else:
               link= base_url+link[2:]
           news_articles.append((name,headline,link))
   success.append(name)
except Exception as e:
   failure.append((name,e))
   pass

# WBUHS
try:
    name="WBUHS"
    url = "https://wbuhs.ac.in/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find_all("div",class_="resp-tabs-container")
    for result in results:
        result=result.find_all('a')
        for r in result:
            headline= r.text.strip()
            link=r.get('href')
            news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# BFUHS
try:
    name="BFUHS"
    base_url="https://bfuhs.ac.in/CollegesNotices/"
    url = "https://bfuhs.ac.in/CollegesNotices/collegesnotices.asp"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find('table',class_="style25").find_all('a')
    for result in results[2:10]:
            headline= result.text.strip()
            link=result.get('href')
            if 'http' in link:
                    link=link.replace(' ','%20')
            else:
                link= base_url+link.replace(' ','%20')
            news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# KGMU
try:
   name="KGMU"
   base_url = "http://kgmu.org/"
   url = "http://kgmu.org/kgmu_notice_board.php"
   res = requests.get(url,verify=False)
   soup = BeautifulSoup(res.text, "html.parser")
   results = soup.find('table',class_="norblack").find_all('a')
   for result in results:
       headline= result.text.strip()
       link=base_url+result.get('href').replace(' ','%20')
       news_articles.append((name, headline, link))
   success.append(name)
except Exception as e:
   failure.append((name,e))
   pass

# IIT Goa
try:
    name="IIT Goa"
    url = "https://iitgoa.ac.in/news/"
    res = requests.get(url,verify=False)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find('ul',class_="list").find_all('a')
    for result in results:
        headline= result.text.strip()
        link=result.get('href').replace(' ','%20')
        if 'https' not in link:
            link=base_url+link
        news_articles.append((name, headline, link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# Punjab University
try:
    name="Punjab University"
    base_url='https://www.ubs.puchd.ac.in/'
    url = "https://www.ubs.puchd.ac.in/show-noticeboard.php?nbid=4"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    results = soup.find("table").find_all("tr")
    for result in results:
        result=result.find_all("td")[2:]
        for r in result:
            headline=r.text.strip()
            link=base_url+r.a.get("href")
            news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# IIM Sirmaur
try:
    name="IIM Sirmaur"
    base_url = "https://www.iimsirmaur.ac.in"
    url = "https://www.iimsirmaur.ac.in/iims/announcements"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find_all("div", class_="panel-body")
    for result in results[:10]:
        headline=result.find("h1").text.replace("\t\t\t\t\t\r\n\t\t\t\t\t\t","").strip()[11:]
        link=base_url+result.find("a").get("href")
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# KNRUHS
try:
    name="KNRUHS"
    base_url = "http://knruhs.telangana.gov.in/"
    url = "http://knruhs.telangana.gov.in/all-notifications"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    table = soup.find('table', class_= "all-notification-table")
    results = table.find_all("tr")

    for result in results[1:11]:
        cols = result.find_all('td')
        headline = cols[2].text
        link = cols[3].find('a').get("href").replace(' ','%20')
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# VMOU
try:
    base = "https://www.vmou.ac.in"
    url = "https://www.vmou.ac.in/home"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("div", id ="quicktabs-tabpage-quicktab_home_announcements-3").find("div", class_ = "view-content")
    for result in results.find_all("tr"):
        headline = result.find("td").text.strip()
        link = base+result.find("td").find("a")["href"].strip()
        news_articles.append(('VMOU', headline, link))
    success.append('VMOU')
except Exception as e:
    failure.append(('VMOU',e))
    pass
# Manipur university
try:
    name="Manipur university"
    base_url = "https://www.manipuruniv.ac.in/"
    url = "https://www.manipuruniv.ac.in/notice"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("div", class_="newsDetailsList").find_all("a")
    for result in results[:10]:
        headline=result.text[2:].replace('.','').strip()
        link=result.get("href")
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# CMCH Vellore
try:
    name="CMCH Vellore"
    base_url = "https://www.cmch-vellore.edu/"
    url = "https://www.cmch-vellore.edu/News.aspx"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("table", id="content_contentRight_gvSpecialEdition").find_all("a")
    for result in results:
        headline=result.text
        link=result.get("href").replace(' ','%20')
        if "http" not in link:
            link=base_url+link
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# BHU
try:
    base_url = "https://www.bhu.ac.in"
    url = "https://www.bhu.ac.in/notification/"
    source = requests.get(url)
    soup = BeautifulSoup(source.text, "html.parser")
    results = soup.find_all("tr")[2].find_all("li")
    for result in results:
        headline = result.find("a").text.strip()
        link = base_url+result.find("a")["href"].strip()
        news_articles.append(('BHU', headline, link))
    success.append('BHU')
except Exception as e:
    failure.append(('BHU', e))
    pass



#DCAC(checked)


try:
    name='DCAC'
    url='http://dcac.du.ac.in/Pages/News/allnews.php'
    res=requests.get(url)
    soup=BeautifulSoup(res.text,'html5lib')
    results=soup.find('div',class_='aboutext').find_all('a')
    for result in results:
        headline=result.text.replace('Click here.','').strip()
        link=result.get('href')
        news_articles.append((name,headline,link))      
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass


#MCASC(done)

try:
    name='MCASC'
    url='http://moderncollegepune.edu.in/notices/'
    res=requests.get(url)
    soup=BeautifulSoup(res.text,'html5lib')
    results=soup.find('div',class_='container-fluid no-padding').find_all('a')
    for result in results[1:]:
        headline=result.text
        link=result.get('href')
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass


#NALSAR(done)


try:
    name='NALSAR'
    url='http://www.nalsar.ac.in/admission'
    res=requests.get(url)
    soup=BeautifulSoup(res.text,'html5lib')
    results=soup.find('div',class_='zone zone-content clearfix container-12').find_all('a')
    for result in results[2:]:
        headline=result.text
        link=result.get('href')
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))  
    pass



#Rashtriya Sanskrit Sansthan(done)

try:
   name='Rashtriya Sanskrit Sansthan'
   url='http://www.sanskrit.nic.in/'
   res=requests.get(url)
   soup=BeautifulSoup(res.text,'html5lib')
   results=soup.find('div',class_='contentbox').find_all('a')
   for result in results[:10]:
       headline=result.text.replace('\n','')
       link=url+result.get('href')
       news_articles.append((name,headline,link))
   success.append(name)
except Exception as e:
    failure.append((name,e))
    pass



#Uttaranchal University(done)


try:
    name='Uttaranchal University'
    url='https://uttaranchaluniversity.ac.in/'
    res=requests.get(url)
    soup=BeautifulSoup(res.text,'html5lib')
    results=soup.find('marquee').find_all('a')
    for result in results:
        headline=result.text
        link=result.get('href')
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append(name)
    pass



#Wilson College(done)


try:
    name='Wilson College'
    url='https://www.wilsoncollege.edu/'
    res=requests.get(url)
    soup=BeautifulSoup(res.text,'html5lib')
    results=soup.find('marquee').find_all('a')
    for result in results:
        headline=result.text.replace('New','').strip()
        link=url+result.get('href')
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass


#NLSIU(done)

try:
    name='NLSIU'
    url='https://www.nls.ac.in/news-and-events/?_news_category=admission'
    res=requests.get(url)
    soup=BeautifulSoup(res.text,'html5lib')
    results=soup.find_all('div',class_='news-events__listing__block')
    for result in results:
        headline=result.find('h2').text.strip()
        link=result.find('a').get('href')
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass







#Keshav Mahavidyalaya(done)

try:
    name="Keshav Mahavidyalaya"
    url="http://keshav.du.ac.in/"
    res=requests.get(url)
    soup=BeautifulSoup(res.text,'html5lib')
    results=soup.find('div',class_='col-lg p-2').find_all('a')
    for result in results[:10]:
        headline=result.text.replace("New"," ").strip()
        link=result.get('href')
        if 'http' in link:
            link=link
            news_articles.append((name,headline,link))
        else:
            link=url+link
            news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass






#CEPT University(error)


try:
    name="CEPT University"
    url="https://cept.ac.in/"
    res=requests.get(url)
    soup=BeautifulSoup(res.text,"html5lib")
    results=soup.find('div',class_="col-md-4 col-sm-4 col-xs-12").find_all("a")
    for result in results[:4]:
        headline=result.text.replace(result.find("h4").text,"").strip()
        link=result.get("href")
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass   


#DTU(done)



try:
    name='DTU'
    url='http://www.dtu.ac.in/'
    res=requests.get(url)
    soup=BeautifulSoup(res.text,'html5lib')
    results=soup.find('div',class_='latest_tab').find('ul').find_all('li')
    for result in results:
        he=result.find_all('a',class_='colr')
        for h in he:
            headline=h.text
            link=h.get('href')
            if h.get('href')==None:  
                continue
            else:
                headline=h.text.replace('||','').replace('\xa0','')
                link=h.get('href')
                if 'http' in link:
                    link=link
                    news_articles.append((name,headline,link))
                else:
                    link=url+link
                    news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass











#Ganpat University(done)

try:
    name="Ganpat University"
    url="https://www.ganpatuniversity.ac.in/"
    res=requests.get(url)
    soup=BeautifulSoup(res.text,"html5lib")
    results=soup.find_all("div",class_="card-body")
    for result in results[:7]:
        if (result.a==None):
            continue
        else:
            link=result.a.get("href")
            head=result.find_all("h5")
            for re in head:
                headline=re.text.strip()
                news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass


#FORE School of Management(done)


try:
    name='FORE School of Management'
    url='https://www.fsm.ac.in/'
    res=requests.get(url)
    soup=BeautifulSoup(res.text,'html5lib')
    results=soup.find_all('div',class_='announcement-box')
    for result in results:
        headline=result.find('p').text
        link=result.find('a').get('href')
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass   



#Fatima College(done)


try:
    name='Fatima College'
    url='https://fatimacollegemdu.org/'
    res=requests.get(url)
    soup=BeautifulSoup(res.text,'html5lib')
    results=soup.find_all('li',class_='news-item')
    for result in results:
        if result.find('h3')==None:
            continue
        else:
            headline=result.find('h3').text.replace('\xa0',' ')
            if result.find('a')==None:
                continue
            else:
               link=result.find('a').get('href')
               news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass


#Khalsa College(done)

try:
    name='Khalsa College'
    url='https://khalsacollege.edu.in/'
    res=requests.get(url)
    soup=BeautifulSoup(res.text,'html5lib')
    results=soup.find_all(class_='tab_content')
    for result in results:
        head=result.find_all('li')
        for r in head[:10]:
            headline=r.text.strip().replace('New','').replace('\t','')
            link=url+r.find('a').get('href')
            news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass



#Kalindi College


try:
    name='Kalindi College'
    url='https://www.kalindicollege.in/'
    res=requests.get(url)
    soup=BeautifulSoup(res.text,'html5lib')
    results=soup.find(class_='box-body home_notice').find_all(class_='notices-row')
    for result in results[:20]:
        headline=result.find('p').text
        link=result.find('a').get('href')
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass








#Hans Raj College


try:
    name='Hans Raj College'
    url='https://www.hansrajcollege.ac.in/announcements/students'
    res=requests.get(url)
    soup=BeautifulSoup(res.text,'html5lib')
    results=soup.find(class_='content-area').find_all('p')
    for result in results:
        headline=result.find('a').text.strip()
        link=result.find('a').get('href')
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass







#Gossner college

try:
    name ="Gossner college"
    url = "http://gcran.org/wp/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("marquee").find_all("a")
    for result in results[:9]:
        headline=result.text.strip()
        link=result.get("href")
        news_articles.append((name,headline,link))   
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass









#Karnavati University 

try:
    name='karnavati university'
    url = 'https://karnavatiuniversity.edu.in/'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    results = soup.find('ul', class_ = 'scroll-bar-list2').find_all('li')
    for result in results:
        headline = result.text.replace("\n"," ").strip()
        link = result.find('a').get('href')
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass



#St Francis College for Women

try:
    name='St Francis College for Women'
    url = 'https://www.sfc.ac.in/'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    results = soup.find_all('marquee')[2:]
    for result in results:
        head=result.find_all("a")
        for re in head:
            headline=re.text.strip()
            link=url+re.get("href")
            news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass





#Santipur college

try:
    name='Santipur college'
    url = 'http://www.santipurcollege.in/Notice-board.aspx'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    results = soup.find('tbody').find_all('tr')
    for result in results[:10]:
        headline = result.find('td').find_next_sibling('td').find_next_sibling('td').text
        link = result.find('a').get('href')
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass


#RIE Ajmer


try:
    name='RIE Ajmer'
    url='http://www.rieajmer.raj.nic.in/'
    res=requests.get(url)
    soup=BeautifulSoup(res.text,'html5lib')
    results=soup.find('marquee').find_all('li')
    for result in results:
        headline=result.text.replace(result.find('a').text,'')
        link=url+result.find('a').get('href')
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass   











#University College

try:
    name='University college'
    url = 'http://universitycollege.ac.in/'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    results = soup.find_all('div', id = 'news-area')
    for result in results:
        headline = result.find('a').text.strip()
        link = result.find('a').get('href')
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass






#Andhra University, School of Distance Education

try:
    name='Andhra University, School of Distance Education'
    base_url='https://andhrauniversity.edu.in/'
    url = 'https://andhrauniversity.edu.in/admissions/school-of-distance-education.html'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    results = soup.find('ul', class_ = 'news').find_all('li')
    for result in results:
        headline = result.find('a').text[12:].replace(":"," ").strip()
        link = base_url + result.find('a').get('href')
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass



#Delhi Pharmaceutical Sciences and Research University

try:
    name='Delhi Pharmaceutical Sciences and Research University'
    url = 'https://dpsru.edu.in/list-of-whats-new/'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    results = soup.find('div', class_ = 'site-content').find_all('div', class_ = 'col-md-12 what_new')
    for result in results[:10]:
        headline = result.find('a').text.strip()
        link = result.find('a').get('href')
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass






#Rabindranath Tagore University

try:
    name='Rabindranath Tagore University'
    base_url = 'https://rntu.ac.in/'
    url = 'https://rntu.ac.in/about/Letest-News'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    results = soup.find('ul', class_ = 'list-aggregate').find_all('li')
    for result in results:
        headline = result.find('a').text
        link = result.find('a').get('href')   
        if "http" in link:
            link=link
        else:
            link=base_url+link     
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass




#DCAC(checked)


try:
    name='DCAC'
    url='http://dcac.du.ac.in/Pages/News/allnews.php'
    res=requests.get(url)
    soup=BeautifulSoup(res.text,'html5lib')
    results=soup.find('div',class_='aboutext').find_all('a')
    for result in results:
        headline=result.text.replace('Click here.','').strip()
        link=result.get('href')
        news_articles.append((name,headline,link))      
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass





#MCASC(done)




try:
    name='MCASC'
    url='http://moderncollegepune.edu.in/notices/'
    res=requests.get(url)
    soup=BeautifulSoup(res.text,'html5lib')
    results=soup.find('div',class_='container-fluid no-padding').find_all('a')
    for result in results[1:]:
        headline=result.text
        link=result.get('href')
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass


#NALSAR(done)


try:
    name='NALSAR'
    url='http://www.nalsar.ac.in/admission'
    res=requests.get(url)
    soup=BeautifulSoup(res.text,'html5lib')
    results=soup.find('div',class_='zone zone-content clearfix container-12').find_all('a')
    for result in results[2:]:
        headline=result.text
        link=result.get('href')
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))  
    pass







#Uttaranchal University(done)


try:
    name='Uttaranchal University'
    url='https://uttaranchaluniversity.ac.in/'
    res=requests.get(url)
    soup=BeautifulSoup(res.text,'html5lib')
    results=soup.find('marquee').find_all('a')
    for result in results:
        headline=result.text
        link=result.get('href')
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass



#Wilson College(done)


try:
    name='Wilson College'
    url='https://www.wilsoncollege.edu/'
    res=requests.get(url)
    soup=BeautifulSoup(res.text,'html5lib')
    results=soup.find('marquee').find_all('a')
    for result in results:
        headline=result.text.replace('New','').strip()
        link=url+result.get('href')
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass


#NLSIU(done)

try:
    name='NLSIU'
    url='https://www.nls.ac.in/news-and-events/?_news_category=admission'
    res=requests.get(url)
    soup=BeautifulSoup(res.text,'html5lib')
    results=soup.find_all('div',class_='news-events__listing__block')
    for result in results:
        headline=result.find('h2').text.strip()
        link=result.find('a').get('href')
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass







#Keshav Mahavidyalaya(done)

try:
    name="Keshav Mahavidyalaya"
    url="http://keshav.du.ac.in/"
    res=requests.get(url)
    soup=BeautifulSoup(res.text,'html5lib')
    results=soup.find('div',class_='col-lg p-2').find_all('a')
    for result in results[:10]:
        headline=result.text.replace("New"," ").strip()
        link=result.get('href')
        if 'http' in link:
            link=link
            news_articles.append((name,headline,link))
        else:
            link=url+link
            news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass




#CEPT University(error)


try:
    name="CEPT University"
    url="https://cept.ac.in/"
    res=requests.get(url)
    soup=BeautifulSoup(res.text,"html5lib")
    results=soup.find('div',class_="col-md-4 col-sm-4 col-xs-12").find_all("a")
    for result in results[:4]:
        headline=result.text.replace(result.find("h4").text,"").strip()
        link=result.get("href")
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass   


#DTU(done)



try:
    name='DTU'
    url='http://www.dtu.ac.in/'
    res=requests.get(url)
    soup=BeautifulSoup(res.text,'html5lib')
    results=soup.find('div',class_='latest_tab').find('ul').find_all('li')
    for result in results:
        he=result.find_all('a',class_='colr')
        for h in he:
            headline=h.text
            link=h.get('href')
            if h.get('href')==None:  
                continue
            else:
                headline=h.text.replace('||','').replace('\xa0','')
                link=h.get('href')
                if 'http' in link:
                    link=link
                    news_articles.append((name,headline,link))
                else:
                    link=url+link
                    news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass











#Ganpat University(done)

try:
    name="Ganpat University"
    url="https://www.ganpatuniversity.ac.in/"
    res=requests.get(url)
    soup=BeautifulSoup(res.text,"html5lib")
    results=soup.find_all("div",class_="card-body")
    for result in results[:7]:
        if (result.a==None):
            continue
        else:
            link=result.a.get("href")
            head=result.find_all("h5")
            for re in head:
                headline=re.text.strip()
                news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass


#FORE School of Management(done)


try:
    name='FORE School of Management'
    url='https://www.fsm.ac.in/'
    res=requests.get(url)
    soup=BeautifulSoup(res.text,'html5lib')
    results=soup.find_all('div',class_='announcement-box')
    for result in results:
        headline=result.find('p').text
        link=result.find('a').get('href')
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass   



#Fatima College(done)


try:
    name='Fatima College'
    url='https://fatimacollegemdu.org/'
    res=requests.get(url)
    soup=BeautifulSoup(res.text,'html5lib')
    results=soup.find_all('li',class_='news-item')
    for result in results:
        if result.find('h3')==None:
            continue
        else:
            headline=result.find('h3').text.replace('\xa0',' ')
            if result.find('a')==None:
                continue
            else:
               link=result.find('a').get('href')
               news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass


#Khalsa College(done)

try:
    name='Khalsa College'
    url='https://khalsacollege.edu.in/'
    res=requests.get(url)
    soup=BeautifulSoup(res.text,'html5lib')
    results=soup.find_all(class_='tab_content')
    for result in results:
        head=result.find_all('li')
        for r in head[:10]:
            headline=r.text.strip().replace('New','').replace('\t','')
            link=url+r.find('a').get('href')
            news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass



#Kalindi College


try:
    name='Kalindi College'
    url='https://www.kalindicollege.in/'
    res=requests.get(url)
    soup=BeautifulSoup(res.text,'html5lib')
    results=soup.find(class_='box-body home_notice').find_all(class_='notices-row')
    for result in results[:20]:
        headline=result.find('p').text
        link=result.find('a').get('href')
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass





#Hans Raj College


try:
    name='Hans Raj College'
    url='https://www.hansrajcollege.ac.in/announcements/students'
    res=requests.get(url)
    soup=BeautifulSoup(res.text,'html5lib')
    results=soup.find(class_='content-area').find_all('p')
    for result in results:
        headline=result.find('a').text.strip()
        link=result.find('a').get('href')
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass








#Gossner college

try:
    name ="Gossner college"
    url = "http://gcran.org/wp/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("marquee").find_all("a")
    for result in results[:9]:
        headline=result.text.strip()
        link=result.get("href")
        news_articles.append((name,headline,link))   
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass








#Karnavati University 

try:
    name='karnavati university'
    url = 'https://karnavatiuniversity.edu.in/'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    results = soup.find('ul', class_ = 'scroll-bar-list2').find_all('li')
    for result in results:
        headline = result.text.replace("\n"," ").strip()
        link = result.find('a').get('href')
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass



#St Francis College for Women

try:
    name='St Francis College for Women'
    url = 'https://www.sfc.ac.in/'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    results = soup.find_all('marquee')[2:]
    for result in results:
        head=result.find_all("a")
        for re in head:
            headline=re.text.strip()
            link=url+re.get("href")
            news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass





#Santipur college

try:
    name='Santipur college'
    url = 'http://www.santipurcollege.in/Notice-board.aspx'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    results = soup.find('tbody').find_all('tr')
    for result in results[:10]:
        headline = result.find('td').find_next_sibling('td').find_next_sibling('td').text
        link = result.find('a').get('href')
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass


#RIE Ajmer


try:
    name='RIE Ajmer'
    url='http://www.rieajmer.raj.nic.in/'
    res=requests.get(url)
    soup=BeautifulSoup(res.text,'html5lib')
    results=soup.find('marquee').find_all('li')
    for result in results:
        headline=result.text.replace(result.find('a').text,'')
        link=url+result.find('a').get('href')
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass   









#University College

try:
    name='University college'
    url = 'http://universitycollege.ac.in/'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    results = soup.find_all('div', id = 'news-area')
    for result in results:
        headline = result.find('a').text.strip()
        link = result.find('a').get('href')
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass






#Andhra University, School of Distance Education

try:
    name='Andhra University, School of Distance Education'
    base_url='https://andhrauniversity.edu.in/'
    url = 'https://andhrauniversity.edu.in/admissions/school-of-distance-education.html'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    results = soup.find('ul', class_ = 'news').find_all('li')
    for result in results:
        headline = result.find('a').text[12:].replace(":"," ").strip()
        link = base_url + result.find('a').get('href')
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass



#Delhi Pharmaceutical Sciences and Research University

try:
    name='Delhi Pharmaceutical Sciences and Research University'
    url = 'https://dpsru.edu.in/list-of-whats-new/'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    results = soup.find('div', class_ = 'site-content').find_all('div', class_ = 'col-md-12 what_new')
    for result in results[:10]:
        headline = result.find('a').text.strip()
        link = result.find('a').get('href')
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass






#Rabindranath Tagore University

try:
    name='Rabindranath Tagore University'
    base_url = 'https://rntu.ac.in/'
    url = 'https://rntu.ac.in/about/Letest-News'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    results = soup.find('ul', class_ = 'list-aggregate').find_all('li')
    for result in results:
        headline = result.find('a').text
        link = result.find('a').get('href')   
        if "http" in link:
            link=link
        else:
            link=base_url+link     
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass


#PDM University

try:
    name ='PDM University'
    url = "https://www.pdm.ac.in/latest-news"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find_all("h4")
    for result in results[:10]:
        headline=result.text.strip()
        link=result.a.get("href")
        news_articles.append((name,headline,link))   
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass












#College of Vocational Studies

try:
    name ='College of Vocational Studies'
    url = "https://www.cvs.edu.in/view-all-details.php"
    base_url="https://www.cvs.edu.in/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("div", class_="about-menu").find_all("li")
    for result in results[:10]:
        headline=result.a.text.strip()
        link=result.a.get("href")
        if "http" in link:
            link=link
        else:
            link=base_url+link
        news_articles.append((name,headline,link))   
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass



#Kalyani Mahavidyalaya


try:
    name ='Kalyani Mahavidyalaya'
    url = "http://kalyanimahavidyalaya.co.in/notice.aspx"
    base_url="http://kalyanimahavidyalaya.co.in/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find_all("div", class_="box")
    for result in results[:9]:
        headline=result.text.strip()
        link=base_url+result.a.get("href").replace(" ","%20")
        news_articles.append((name,headline,link))   
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass
#Patna College

try:
    name ='Patna College'
    url = "http://www.patnacollege.org/"
    base_url="http://www.patnacollege.org/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("marquee", direction="up").find_all("a")
    for result in results[:9]:
        headline=result.text.strip()
        link=base_url+result.get("href")
        news_articles.append((name,headline,link))   
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass



#VIPS

try:
    name ='VIPS'
    url = "https://vips.edu/admission-information/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find_all("p")
    for result in results[:19]:
        headline=result.text.strip()
        link=result.a.get("href")
        news_articles.append((name,headline,link))   
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass





#Sri Sri University

try:
    name ='Sri Sri University'
    url = "https://srisriuniversity.edu.in/"
    base_url="https://srisriuniversity.edu.in/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("div", class_="news-container").find_all("a")
    for result in results[:10]:
        headline=result.text.strip()
        link=result.get("href")
        news_articles.append((name,headline,link))   
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass








#Kirori Mal College


try:
    name ='Kirori Mal College'
    url = "http://kmc.du.ac.in/category/latest-news/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find_all("h3", class_="entry-title")
    for result in results:
        headline=result.text.strip()
        link=result.a.get("href")
        news_articles.append((name,headline,link))   
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass
#Jesus and Mary College

try:
    name ='Jesus and Mary College'
    url = "https://www.jmc.ac.in/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("ul", style="text-align: center;").find_all("a")
    for result in results:
        headline=result.text.strip()
        link=result.get("href").replace(" ","%20")
        news_articles.append((name,headline,link))   
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass  



#National Law University


try:
    name ='National Law University'
    url = "https://nludelhi.ac.in/Annuoncement.aspx"
    base_url="https://nludelhi.ac.in/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find('ul',style="overflow:auto;").find_all("li",style='')
    for result in results[:10]:
        headline=result.text.strip()
        link=result.a.get("href")
        if 'http' in link:
            link=link
        else:
            link= base_url+link
        news_articles.append((name,headline,link))  
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass 




#PGDAV College

try:
    name ='PGDAV College'
    url = "http://pgdavcollege.edu.in/MenuList.aspx?MenuId=News_2324"
    base_url="http://pgdavcollege.edu.in/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("div", class_="col-sm-3").find_all("a")
    for result in results[:10]:
        headline=result.text.strip()
        link=base_url+result.get("href")
        news_articles.append((name,headline,link))   
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

#Miranda House


try:
    name ='Miranda house'
    url = "https://www.mirandahouse.ac.in/notice.php"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find_all("tr")[1:12]
    for result in results:
        headline=result.a.text.strip()    
        link=result.a.get("href")
        news_articles.append((name,headline,link))   
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass




#Satyawati College

try:
    name ='Satyawati College'
    url = "http://satyawati.du.ac.in/CIRCULARS.HTML"
    base_url="http://satyawati.du.ac.in/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find_all("tr")[1:12]
    for result in results:
        headline=result.find("td").text.strip()
        link=base_url+result.a.get("href").replace(" ","%20")
        news_articles.append((name,headline,link))   
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

    pass


#ICFAI Business School 
try:
    source=requests.get('https://ibsindia.org/').text
    url='https://ibsindia.org/'
    soup=BeautifulSoup(source,'html.parser')
    div=soup.find('div',class_="wedobox")
    text=div.h2.text
    link=div.a['href']
    if 'http' not in link:
        link=url+link
        text=text.lstrip()
        text=text.rstrip()
        link=link.lstrip()
        link=link.rstrip()
    news_articles.append(('ICFAI Business School',text,link))
    success.append('ICFAI Business School')
except Exception as e:
    failure.append(('ICFAI Business School',e))
    pass

#Management Development Institute 

try:
    source=requests.get('https://www.mdi.ac.in/').text
    url='https://www.mdi.ac.in/'
    soup=BeautifulSoup(source,'html.parser')
    div=soup.find('div',class_="mainright")
    text=div.a.text
    link=div.a['href']
    if 'http' not in link:
        link=url+link
        text=text.lstrip()
        text=text.rstrip()
        link=link.lstrip()
        link=link.rstrip()
    news_articles.append(('Management Development Institute',text,link))
    ul=div.find('ul')
    for a in ul.find_all('a'):
        text=a.text
        link=a['href']
        if 'http' not in link:
            link=url+link
        text=text.lstrip()
        text=text.rstrip()
        link=link.lstrip()
        link=link.rstrip()
        news_articles.append(('Management Development Institute',text,link))
    success.append('Management Development Institute')
except Exception as e:
    failure.append(('Management Development Institute',e))
    pass


#IIM Ranchi

try:

    soup=BeautifulSoup(source,'html.parser')
    div=soup.find('div',class_="infirmation-list gfont")
    li=div.find_all('li')
    text=li[1].a.text
    link=li[1].a['href']
    news_articles.append(('IIM Ranchi',text,link))
    text=li[2].a.text
    link=li[2].a['href']
    news_articles.append(('IIM Ranchi]',text,link))
    text=li[4].a.text
    link=li[4].a['href']
    news_articles.append(('IIM Ranchi',text,link))    
    text=li[5].a.text
    link=li[5].a['href']
    news_articles.append(('IIM Ranchi',text,link))
    text=li[6].a.text
    link=li[6].a['href']
    news_articles.append(('IIM Ranchi',text,link))
    success.append('IIM Ranchi]')
except Exception as e:
    failure.append(('IIM Ranchi',e))
    pass

#Institute of Management Studies Noida 

try:
    source=requests.get('https://imsnoida.com/').text
    url='https://imsnoida.com/'
    soup=BeautifulSoup(source,'html.parser')
    marquee=soup.find('marquee')
    text=marquee.a.text
    link=marquee.a['href']
    if 'http' not in link:
        link=url+link
        text=text.lstrip()
        text=text.rstrip()
        link=link.lstrip()
        link=link.rstrip()
    news_articles.append(('Institute of Management Studies Noida',text,link))
    success.append('Institute of Management Studies Noida')
except Exception as e:
    failure.append(('Institute of Management Studies Noida',e))
    pass



#Narsee Monjee Institute of Management Studies 

try:
    source=requests.get('https://www.nmimsbengaluru.org/').text
    url='https://www.nmimsbengaluru.org/'
    soup=BeautifulSoup(source,'html.parser')
    div=soup.find('div',class_="col-xs-12 col-sm-12 col-md-3 padb20")
    for a in div.find_all('a'):
        text=a.text
        link=a['href']
        if 'http' not in link:
            link=url+link
        text=text.lstrip()
        text=text.rstrip()
        link=link.lstrip()
        link=link.rstrip()
        news_articles.append(('Narsee Monjee Institute of Management Studies',text,link))
    success.append('Narsee Monjee Institute of Management Studies')
except Exception as e:
    failure.append(('Narsee Monjee Institute of Management Studies',e))
    pass

#Institute of Management Technology

try:
    source=requests.get('https://www.imtnagpur.ac.in/').text
    url='https://www.imtnagpur.ac.in/'
    soup=BeautifulSoup(source,'html.parser')

    ul=soup.find('ul',class_="follow-us")
    text=ul.a.text
    link=ul.a['href']
    text=text.lstrip()
    text=text.rstrip()
    link=link.lstrip()
    link=link.rstrip()
    if 'http' not in link:
         link=url+link
    news_articles.append(('Institute of Management Technology',text,link))
    success.append('Institute of Management Technology')
except Exception as e:
    failure.append(('Institute of Management Technology',e))
    pass

#IFIM Business School

try:
    source=requests.get('https://www.jagsom.com/').text
    url='https://www.jagsom.com/'
    soup=BeautifulSoup(source,'html.parser')
    ul=soup.find('ul',class_="list-inline mb-0")
    for a in ul.find_all('a'):
        text=a.text
        if a['href']=="#":
            link=url
        else:
            link=a['href']
        text=text.lstrip()
        text=text.rstrip()
        link=link.lstrip()
        link=link.rstrip()
        if 'http' not in link:
            link=url+link
        news_articles.append(('IFIM Business School',text,link))
    success.append('IFIM Business School')
except Exception as e:
    failure.append(('IFIM Business School',e))
    pass

#VIT Business School

try:
    source=requests.get('https://vit.ac.in/schools/vitbs').text
    url='https://vit.ac.in/schools/vitbs'
    soup=BeautifulSoup(source,'html.parser')
    div=soup.find('div',class_="col-md-8")
    p=div.find('p')
    for a in p.find_all('a'):
        text=a.text
        link=a['href']
        text=text.lstrip()
        text=text.rstrip()
        link=link.lstrip()
        link=link.rstrip()
        if 'http' not in link:
            link=url+link
        news_articles.append(('VIT Business School',text,link))
    success.append('VIT Business School')
except Exception as e:
    failure.append(('VIT Business School',e))
    pass

# #ICFAI Business School
# try:
    
#     source=requests.get('https://ibsindia.org/ibs-kolkata/').text
#     url='https://ibsindia.org/ibs-kolkata/'
#     soup=BeautifulSoup(source,'html.parser')
#     div=soup.find('div',class_="top-scroll")
#     a=div.find_all('a')
#     text=a[1].text
#     link=a[1]['href']
#     text=text.lstrip()
#     text=text.rstrip()
#     link=link.lstrip()
#     link=link.rstrip()
#         if 'http' not in link:
#             link=url+link
#         news_articles.append(('ICFAI Business School',text,link))
#     success.append('ICFAI Business School')
# except Exception as e:
#     failure.append(('ICFAI Business School',e))
#     pass


#N. L. Dalmia Institute of Management Studies and Research

try:
    source=requests.get('https://www.nldalmia.in/').text
    url='https://www.nldalmia.in/'
    soup=BeautifulSoup(source,'html.parser')
    div=soup.find('div',class_="microsoft-marquee container")
    for a in div.find_all('a'):
        text=a.text
        link=a['href']
        text=text.lstrip()
        text=text.rstrip()
        link=link.lstrip()
        link=link.rstrip()
        text= " ".join(text.split())
        if 'http' not in link:
            link=url+link
        news_articles.append(('N. L. Dalmia Institute of Management Studies and Research',text,link))
    success.append('N. L. Dalmia Institute of Management Studies and Research')
except Exception as e:
    failure.append(('N. L. Dalmia Institute of Management Studies and Research',e))
    pass

# #IIT Kharagpur
# try:
#     source=requests.get('http://www.iitkgp.ac.in/').text
#     url='http://www.iitkgp.ac.in/'
#     soup=BeautifulSoup(source,'html.parser')
#     marquee=soup.find('marquee')
#     for a in marquee.find_all('a'):
    #     text=a.text
    #     link=a['href']
    #     if 'http' not in link:
    #         link=url+link
    #     text=text.lstrip()
    #     text=text.rstrip()
    #     link=link.lstrip()
    #     link=link.rstrip()
    #     news_articles.append(('IIT Kharagpur',text,link))
#     success.append('IIT Kharagpur')
# except Exception as e:
#     failure.append(('IIT Kharagpur',e))
#     pass


#Thapar Institute of Engineering and Technology

try:

    source=requests.get('https://www.thapar.edu/aboutus/news').text
    url='https://www.thapar.edu/aboutus/news'
    soup=BeautifulSoup(source,'html.parser')
    div=soup.find('div',class_='hghlt-link')
    for a in div.find_all('a'):
        text=a.text
        link=a['href']
        text=text.lstrip()
        text=text.rstrip()
        link=link.lstrip()
        link=link.rstrip()
        news_articles.append(('Thapar Institute of Engineering and Technology',text,link))
    success.append('Thapar Institute of Engineering and Technology')
except Exception as e:
    failure.append(('Thapar Institute of Engineering and Technology',e))
    pass

#University of Petroleum and Energy Studies

try:
    source=requests.get('https://www.upes.ac.in/').text
    url='https://www.upes.ac.in/'
    soup=BeautifulSoup(source,'html.parser')
    a=soup.find('a',target="_blank",href="https://admission.upes.ac.in/apply")
    text=a.span.text
    link=a['href']
    news_articles.append(('University of Petroleum and Energy Studies',text,link))
    success.append('University of Petroleum and Energy Studies')
except Exception as e:
    failure.append(('University of Petroleum and Energy Studies',e))
    pass

#Pandit Deendayal Petroleum University, School of Technology

try:

    source=requests.get('http://sot.pdpu.ac.in/').text
    url='http://sot.pdpu.ac.in/'
    soup=BeautifulSoup(source,'html.parser')
    div=soup.find('div',id="contentin")
    text=div.u.text
    link=div.a['href']
    if 'http' not in link:
        link=url+link
    news_articles.append(('Pandit Deendayal Petroleum University, School of Technology',text,link))
    success.append('Pandit Deendayal Petroleum University, School of Technology')
except Exception as e:
    failure.append(('Pandit Deendayal Petroleum University, School of Technology',e))
    pass

#Chhotu Ram Rural Institute Of Technology

try:

    source=requests.get('http://www.crritonline.com/').text
    url='http://www.crritonline.com/'
    soup=BeautifulSoup(source,'html.parser')
    div=soup.find('div',class_='modal-body')
    text=div.h2.text
    link=div.a['href']
    if 'http' not in link:
        link=url+link
    news_articles.append(('Chhotu Ram Rural Institute Of Technology',text,link))
    success.append('Chhotu Ram Rural Institute Of Technology')
except Exception as e:
    failure.append(('Chhotu Ram Rural Institute Of Technology',e))
    pass  




#AMC Engineering College

try:

    source=requests.get('https://www.amcgroup.edu.in/AMCEC/index.php').text
    url='https://www.amcgroup.edu.in/AMCEC/index.php'
    soup=BeautifulSoup(source,'html.parser')
    div=soup.find_all('div',class_='pull-right')
    text=div[3].a.text
    link=div[3].a['href']
    news_articles.append(('AMC Engineering College',text,link))
    success.append('AMC Engineering College')
except Exception as e:
    failure.append(('AMC Engineering College',e))
    pass

#Panimalar Engineering College

try:

    source=requests.get('https://www.panimalar.ac.in/').text
    url='https://www.panimalar.ac.in/'
    soup=BeautifulSoup(source,'html.parser')
    li=soup.find('li',class_="admission")
    text=li.a.text
    link=li.a['href']
    if 'http' not in link:
        link=url+link
    news_articles.append(('Panimalar Engineering College',text,link))
    success.append('Panimalar Engineering College')
except Exception as e:
    failure.append(('Panimalar Engineering College',e))
    pass

#HKBK College of Engineering

try:

    source=requests.get('https://www.hkbk.edu.in/').text
    url='https://www.hkbk.edu.in/'
    soup=BeautifulSoup(source,'html.parser')
    div=soup.find('div',class_="home-banner-links-fixed")
    for a in div.ul.find_all('a'):
        text=a.text
        link=a['href']
        text=text.lstrip()
        text=text.rstrip()
        link=link.lstrip()
        link=link.rstrip()
        if 'http' not in link:
            link=url+link
        news_articles.append(('HKBK College of Engineering',text,link))
    success.append('HKBK College of Engineering')
except Exception as e:
    failure.append(('HKBK College of Engineering',e))
    pass    



#Asansol Engineering College

try:
    source=requests.get('https://aecwb.edu.in/').text
    url='https://aecwb.edu.in/'
    soup=BeautifulSoup(source,'html.parser')
    div=soup.find('div',id='enquiryAdmDv1')
    text=div.a.text
    link=div.a['href']
    if 'http' not in link:
        link=url+link
        text=text.lstrip()
        text=text.rstrip()
        link=link.lstrip()
        link=link.rstrip()
        news_articles.append(('Asansol Engineering College',text,link))
    success.append('Asansol Engineering College')
except Exception as e:
    failure.append(('Asansol Engineering College',e))
    pass




#AIMS Patna

try:
    source=requests.get('https://aiimspatna.edu.in/').text
    url='https://aiimspatna.edu.in/'
    soup=BeautifulSoup(source,'html.parser')
    div=soup.find('div',class_="about-content important")
    a= div.find_all('a')
    text=a[3].text
    link=a[3]['href']
    if 'http' not in link:
        link=url+link
        text=text.lstrip()
        text=text.rstrip()
        link=link.lstrip()
        link=link.rstrip()
        news_articles.append(('AIMS Patna',text,link))
    text=a[4].text
    link=a[3]['href']
    if 'http' not in link:
        link=url+link
        text=text.lstrip()
        text=text.rstrip()
        link=link.lstrip()
        link=link.rstrip()
        news_articles.append(('AIMS Patna',text,link))
    success.append('AIMS Patna')
except Exception as e:
    failure.append(('AIMS Patna',e))
    pass



#Saveetha Institute of Medical And Technical Sciences

try:
    source=requests.get('https://www.saveetha.com/').text
    url='https://www.saveetha.com/'
    soup=BeautifulSoup(source,'html.parser')
    div=soup.find('div',class_="header-nav")
    a=div.find_all('a')
    text=a[3].text
    link=a[3]['href']
    if 'http' not in link:
        link=url+link
        text=text.lstrip()
        text=text.rstrip()
        link=link.lstrip()
        link=link.rstrip()
        news_articles.append(('Saveetha Institute of Medical And Technical Sciences',text,link))
    success.append('Saveetha Institute of Medical And Technical Sciences')
except Exception as e:
    failure.append(('Saveetha Institute of Medical And Technical Sciences',e))
    pass

#Christian Medical College

try:
    source=requests.get('https://www.cmcludhiana.in/').text
    url='https://www.cmcludhiana.in/'
    soup=BeautifulSoup(source,'html.parser')
    div=soup.find('div',class_="news-updates")
    a=div.find_all('a')
    text=a[1].text
    link=a[1]['href']
    if 'http' not in link:
        link=url+link
        text=text.lstrip()
        text=text.rstrip()
        link=link.lstrip()
        link=link.rstrip()
        news_articles.append(('Christian Medical College',text,link))
    success.append('Christian Medical College')
except Exception as e:
    failure.append(('Christian Medical College',e))
    pass

# #Saveetha Medical College
# try:

#     source=requests.get('http://www.saveethamedicalcollege.com/',headers=headers).text
#     url='http://www.saveethamedicalcollege.com/'
#     soup=BeautifulSoup(source,'html.parser')
#     div=soup.find_all('div',class_="t3-megamenu")


#     li=div[0].find_all('li',class_="dropdown mega")
#         text=li[2].a.text
#         link=li[2].a['href']
#         if 'http' not in link:
#             link=url+link
#             text=text.lstrip()
#             text=text.rstrip()
#             link=link.lstrip()
#             link=link.rstrip()
#             news_articles.append(('Saveetha Medical College',text,link))
#     success.append('Saveetha Medical College')
# except Exception as e:
#     failure.append(('Saveetha Medical College',e))
    # pass




# #National Institute of Mental Health and Neuro Sciences
# try:
#     source=requests.get('https://nimhans.ac.in/').text
#     url='https://nimhans.ac.in/'
#     soup=BeautifulSoup(source,'html.parser')
#     section=soup.find('section',class_="wp-show-posts")
#     text=section.a.text
#     link=section.a['href']
#     if 'http' not in link:
#         link=url+link
#         text=text.lstrip()
#         text=text.rstrip()
#         link=link.lstrip()
#         link=link.rstrip()
#         news_articles.append(('National Institute of Mental Health and Neuro Sciences',text,link))
#     success.append('National Institute of Mental Health and Neuro Sciences')
# except Exception as e:
#     failure.append(('National Institute of Mental Health and Neuro Sciences',e))
#     pass


#Symbiosis College of Arts and Commerce

try:
    source=requests.get('https://symbiosiscollege.edu.in/').text
    soup=BeautifulSoup(source,'html.parser')

    div=  soup.find_all('div',class_='box2')
    #h=article.find('header',class_="entry-header")
    for p in div[0].find_all('p'): 
        link=p.a['href']
        text=p.text.lstrip()
        text=text.rstrip()
        link=link.lstrip()
        link=link.rstrip()
        news_articles.append(('Symbiosis College of Arts and Commerce',text,link))
    success.append('Symbiosis College of Arts and Commerce')
except Exception as e:
    failure.append(('Symbiosis College of Arts and Commerce',e))
    pass




#Symbiosis Institute of Business Management
 
try:

    source=requests.get('https://www.sibm.edu/').text
    soup=BeautifulSoup(source,'html.parser')
    div=  soup.find('div',class_='container-fluid')
    div=div.find('div',class_="demo5")
    for li in div.find_all('li'):
        link=li.a['href']
        text=li.a.text
        link=link.lstrip()
        link=link.rstrip()
        text=text.lstrip()
        text=text.rstrip()
        news_articles.append(('Symbiosis Institute of Business Management',text,link))
    success.append('Symbiosis Institute of Business Management')
except Exception as e:
    failure.append(('Symbiosis Institute of Business Management',e))
    pass


#Symbiosis Law School
try:


    source=requests.get('https://www.slsnagpur.edu.in/').text
    soup=BeautifulSoup(source,'html.parser')
    div=soup.find('div',class_='side-div mt-2')
    for a in div.find_all('a',class_='button1 text-light'):
        link=a['href']
        text=a.text
        link=link.lstrip()
        link=link.rstrip()
        text=text.lstrip()
        text=text.rstrip()

        news_articles.append(('Symbiosis Law School',text,link))
    success.append('Symbiosis Law School')
except Exception as e:
    failure.append(('Symbiosis Law School',e))
    pass

#ILS Law College

try:
    source=requests.get('https://ilslaw.edu/').text
    soup=BeautifulSoup(source,'html.parser')
    div=soup.find('ul',class_='cell-center-list')
    for li in div.find_all('li'):
        link=li.a['href']
        text=li.a.text
        link=link.lstrip()
        link=link.rstrip()
        text=text.lstrip()
        text=text.rstrip()
        news_articles.append(('ILS Law College',text,link))
    success.append('ILS Law College')
except Exception as e:
    failure.append(('ILS Law College',e))
    pass

#Tamil Nadu Agricultural University

try:
   
    source=requests.get('https://tnau.ac.in/').text
    soup=BeautifulSoup(source,'html.parser')
    div=soup.find_all('div',class_='vc_row wpb_row vc_row-fluid')
    for a in div[1].find_all('a'):
        text=a.text
        link=a['href']
        link=link.lstrip()
        link=link.rstrip()
        text=text.lstrip()
        text=text.rstrip()
        news_articles.append(('Tamil Nadu Agricultural University',text,link))
    success.append('Tamil Nadu Agricultural University')
except Exception as e:
    failure.append(('Tamil Nadu Agricultural University',e))
    pass

#Tamil Nadu Open University
try:
    source=requests.get('https://tnou.ac.in/').text
    soup=BeautifulSoup(source,'html.parser')
    div=soup.find('div',class_='news')
    for a in div.find_all('a'):
        text=a.text
        link=a['href']
        link=link.lstrip()
        link=link.rstrip()
        text=text.lstrip()
        text=text.rstrip()
        news_articles.append(('Tamil Nadu Open University',text,link))
    success.append('Tamil Nadu Open University')
except Exception as e:
    failure.append(('Tamil Nadu Open University',e))
    pass

#Techno India University

try:
    source=requests.get('https://www.technoindiauniversity.ac.in/').text
    soup=BeautifulSoup(source,'html.parser')
    div=soup.find('section',class_='team section')
    text=div.a.text
    link=div.a['href']
    link=link.lstrip()
    link=link.rstrip()
    text=text.lstrip()
    text=text.rstrip()
    news_articles.append(('Techno India University',text,link))
    success.append('Techno India University')
except Exception as e:
    failure.append(('Techno India University',e))
    pass

#TERI School of Advanced Studies
try:
    source=requests.get('https://terisas.ac.in/').text
    soup=BeautifulSoup(source,'html.parser')
    div = soup.find('button',class_='btn-txt')
    text=div.text
    link=div.a['href']
    link=link.lstrip()
    link=link.rstrip()
    text=text.lstrip()
    text=text.rstrip()
    news_articles.append(('TERI School of Advanced Studies',text,link))
    success.append('TERI School of Advanced Studies')
except Exception as e:
    failure.append(('TERI School of Advanced Studies',e))
    pass

#Terna Medical College

try:
    source=requests.get('https://ternamedical.org/').text
    soup=BeautifulSoup(source,'html.parser')
    div=soup.find('div',class_='wpb_column vc_column_container vc_col-sm-6 vc_col-has-fill')
    div=div.find('div',class_='wpb_raw_code wpb_raw_js')
    for a in div.find_all('a'):
        text=a.text
        link=a['href']
        link=link.lstrip()
        link=link.rstrip()
        text=text.lstrip()
        text=text.rstrip()
        news_articles.append(('Terna Medical College',text,link))
    success.append('Terna Medical College')
except Exception as e:
    failure.append(('Terna Medical College',e))
    pass

#Tezpur University

try:

    source=requests.get('http://www.tezu.ernet.in/').text
    soup=BeautifulSoup(source,'html.parser')
    div=soup.find('div',class_='minifeatureitem')
    for li in div.ul.find_all('li'):
        text=li.text
        link=li.a['href']
        link=link.lstrip()
        link=link.rstrip()
        text=text.lstrip()
        text=text.rstrip()
        news_articles.append(('Tezpur University',text,link))
    success.append('Tezpur University')
except Exception as e:
    failure.append(('Tezpur University',e))
    pass


#The American College

try:
    source=requests.get('https://americancollege.edu.in/').text
    soup=BeautifulSoup(source,'html.parser')
    div=soup.find_all('div',class_='gdlr-core-pbf-column-content clearfix gdlr-core-js gdlr-core-sync-height-content')
    text=div[1].span.text
    link=div[1].a['href']
    link=link.lstrip()
    link=link.rstrip()
    text=text.lstrip()
    text=text.rstrip()
    news_articles.append(('The American College',text,link))
    success.append('The American College')
except Exception as e:
    failure.append(('The American College',e))
    pass

#Thakur College of Science and Commerce
try:
    source=requests.get('https://www.tcsc.edu.in/').text
    url='https://www.tcsc.edu.in/'
    soup=BeautifulSoup(source,'html.parser')
    div=soup.find_all('div',class_='col-sm mb-2')

    for a in div[2].find_all('a'):
        text=a.text
        link=a['href']
        if 'http' not in link:
            link=url+link
            link=link.lstrip()
            link=link.rstrip()
            text=text.lstrip()
            text=text.rstrip()
        news_articles.append(('Thakur College of Science and Commerce',text,link))
    success.append('Thakur College of Science and Commerce')
except Exception as e:
    failure.append(('Thakur College of Science and Commerce',e))
    pass

#Tilka Manjhi Bhagalpur University

try:
    source=requests.get('http://tmbuniv.ac.in/').text
    soup=BeautifulSoup(source,'html.parser')
    marquee=soup.find('marquee')
    for a in marquee.find_all('a'):
        text=a.text
        link=a['href']
        text=text.rstrip()
        text=text.lstrip()
        link=link.rstrip()
        link=link.lstrip()
        news_articles.append(('Tilka Manjhi Bhagalpur University',text,link))
    success.append('Tilka Manjhi Bhagalpur University')
except Exception as e:
    failure.append(('Tilka Manjhi Bhagalpur University',e))
    pass

#Uka Tarsadia University

try:
    source=requests.get('http://utu.ac.in/').text
    url='http://utu.ac.in/'
    soup=BeautifulSoup(source,'html.parser')
    div=soup.find('div',class_='opening-hourse admin')
    text=div.a.text
    link=div.a['href']
    text=text.rstrip()
    text=text.lstrip()
    link=link.rstrip()
    link=link.lstrip()
    link=url+link
    news_articles.append(('Uka Tarsadia University',text,link))
    success.append('Uka Tarsadia University')
except Exception as e:
    failure.append(('Uka Tarsadia University',e))
    pass

#Uluberia College

try:
    source=requests.get('https://www.uluberiacollege.in/').text
    url='https://www.uluberiacollege.in/'
    soup=BeautifulSoup(source,'html.parser')
    div=soup.find('div',class_='clearfix latestnewsInner')
    text=div.a.text
    link=div.a['href']
    link=link.lstrip()
    link=link.rstrip()
    text=text.lstrip()
    text=text.rstrip()
    news_articles.append(('Uluberia College',text,link))
    success.append('Uluberia College')
except Exception as e:
    failure.append(('Uluberia College',e))
    pass



#University of Allahabad

try:

    source=requests.get('https://www.allduniv.ac.in/').text
    url='https://www.allduniv.ac.in/'
    soup=BeautifulSoup(source,'html.parser')
    div=soup.find('header')
    a=div.find_all('a')
    text=a[2].text
    link=a[2]['href']
    link=link.lstrip()
    link=link.rstrip()
    text=text.lstrip()
    text=text.rstrip()
    news_articles.append(('University of Allahabad',text,link))
    success.append('University of Allahabad')
except Exception as e:
    failure.append(('University of Allahabad',e))
    pass

#University of Burdwan
try:
    source=requests.get('http://www.buruniv.ac.in/').text
    url='http://www.buruniv.ac.in/'
    soup=BeautifulSoup(source,'html.parser')
    div=soup.find('div',id='f1')
    text=div.a.text
    link=div.a['href']
    link=link.lstrip()
    link=link.rstrip()
    text=text.lstrip()
    text=text.rstrip()
    news_articles.append(('University of Burdwan',text,link))


    div=soup.find('div',id='f4')
    text=div.a.text
    link=div.a['href']
    link=link.lstrip()
    link=link.rstrip()
    text=text.lstrip()
    text=text.rstrip()
    news_articles.append(('University of Burdwan',text,link))
    success.append('University of Burdwan')
except Exception as e:
    failure.append(('University of Burdwan',e))
    pass

#University of Calcutta

try:
    source=requests.get('https://www.caluniv.ac.in/').text
    url='https://www.caluniv.ac.in/'
    soup=BeautifulSoup(source,'html.parser')
    ul=soup.find_all('ul',class_='colm_list_prt')
    li=ul[2].find_all('li')
    text=li[5].text
    link=li[5].a['href']
    link=link.lstrip()
    link=link.rstrip()
    text=text.lstrip()
    text=text.rstrip()
    link=url+link
    news_articles.append(('University of Calcutta',text,link))
    success.append('University of Calcutta')
except Exception as e:
    failure.append(('University of Calcutta',e))
    pass

#Vardhman Mahaveer Open University

try:
    source=requests.get('https://www.vmou.ac.in/').text
    url='https://www.vmou.ac.in/'
    soup=BeautifulSoup(source,'html.parser')
    table=soup.find_all('tbody')
    tr=table[2].find_all('tr')
    text=tr[1].a.text
    link=tr[1].a['href']
    link=link.lstrip()
    link=link.rstrip()
    text=text.lstrip()
    text=text.rstrip()
    news_articles.append(('Vardhman Mahaveer Open University',text,link))
    success.append('Vardhman Mahaveer Open University')
except Exception as e:
    failure.append(('Vardhman Mahaveer Open University',e))
    pass

#Vardhman Mahavir Medical College

try:
    source=requests.get('http://www.vmmc-sjh.nic.in/Default_College.aspx').text
    url='http://www.vmmc-sjh.nic.in/'
    soup=BeautifulSoup(source,'html.parser')
    div=soup.find('div',id='fixed_admission_div')
    for li in div.find_all('li'):
        text=li.a.text
        link=url+li.a['href']
        link=link.lstrip()
        link=link.rstrip()
        text=text.lstrip()
        text=text.rstrip()
        news_articles.append(('Vardhman Mahavir Medical College',text,link))
    success.append('Vardhman Mahavir Medical College')
except Exception as e:
    failure.append(('Vardhman Mahavir Medical College',e))
    pass


#Vels Institute of Science, Technology & Advanced Studies

try:
    source=requests.get('http://www.velsuniv.ac.in/').text
    url='http://www.velsuniv.ac.in/'
    soup=BeautifulSoup(source,'html.parser')
    div=soup.find('div',class_="apply-now")
    text=div.a.text
    link=div.a['href']
    link=link.lstrip()
    link=link.rstrip()
    text=text.lstrip()
    text=text.rstrip()
    news_articles.append(('Vels Institute of Science, Technology & Advanced Studies',text,link))
    success.append('Vels Institute of Science, Technology & Advanced Studies')
except Exception as e:
    failure.append(('Vels Institute of Science, Technology & Advanced Studies',e))
    pass

#Vishwakarma Institute of Technology
try:
    source=requests.get('https://www.vit.edu/').text
    url='https://www.vit.edu/'
    soup=BeautifulSoup(source,'html.parser')
    div=soup.find('div',class_='latestnewsWrap')
    text=div.h3.text
    link=div.a['href']
    link=link.lstrip()
    link=link.rstrip()
    text=text.lstrip()
    text=text.rstrip()
    link=link.lstrip('/')
    link=url+link
    news_articles.append(('Vishwakarma Institute of Technology',text,link))
    success.append('Vishwakarma Institute of Technology')
except Exception as e:
    failure.append(('Vishwakarma Institute of Technology',e))
    pass

#Vishwakarma University

try:

    source=requests.get('https://www.vupune.ac.in/').text
    url='https://www.vupune.ac.in/'
    soup=BeautifulSoup(source,'html.parser')
    marquee=soup.find('marquee')
    a = marquee.find_all('a')
    text=a[1].text
    link=a[1]['href']
    link=link.lstrip()
    link=link.rstrip()
    text=text.lstrip()
    text=text.rstrip()
    news_articles.append(('Vishwakarma University',text,link))
    success.append('Vishwakarma University')
except Exception as e:
    failure.append(('Vishwakarma University',e))
    pass

#Acharya Institute of Technology

try:
    source=requests.get('https://www.acharya.ac.in/').text
    url='https://www.acharya.ac.in/'
    soup=BeautifulSoup(source,'html.parser')
    div=soup.find_all('div',class_='row')
    text=div[1].a.text
    link=div[1].a['href']
    news_articles.append(('Acharya Institute of Technology',text,link))
    success.append('Acharya Institute of Technology')
except Exception as e:
    failure.append(('Acharya Institute of Technology',e))
    pass


#xime
try:
    base_url = "http://www.xime.org/"
    url = "http://www.xime.org/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find_all("div", class_="col-sm-12")
    for result in results[1:]:
        headline = result.marquee.text.replace("\n","").replace("=>","")
        link= result.a.get("href").strip()
        news_articles.append(('xime',headline,link))
    success.append('xime')
except Exception as e:
    failure.append(('xime', e))
    pass

#ximb
try:
    base_url = "https://ximb.edu.in/"
    url = "https://ximb.edu.in/news-and-events/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("div", class_="main_list_wrapper")
    for result in results.find_all("div", class_="col-lg-4 col-md-6 col-12"):
        headline = result.h2.text.replace("\n","")
        link = result.a.get("href").strip()
        news_articles.append(('ximb', headline, link))
    success.append('ximb')
except Exception as e:
    failure.append(('ximb', e))
    pass

#imik
try:
    base_url = "https://www.imik.edu.in/"
    url = "https://www.imik.edu.in/news-events/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("div", class_="col-lg-9 p-3 box-shadow-4 border-radius-0 news_listing")
    for result in results.find_all("div", class_="col-md-9 col-lg-9"):
        headline = result.a.text
        link = result.a.get("href").strip()
        news_articles.append(('imik', headline, link))
    success.append('imik')
except Exception as e:
    failure.append(('imik', e))
    pass



#jntua
try:
    base_url = "https://www.jntua.ac.in/"
    url = "https://www.jntua.ac.in/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("div", class_="tab-content")
    for result in results.find_all("a"):
        headline = result.text
        link= result.get("href").strip()
        news_articles.append(('jntua',headline,link))
    success.append('jntua')
except Exception as e:
    failure.append(('jntua',e))
    pass

#narula
try:
    base_url = "https://www.nit.ac.in/"
    url = "https://www.nit.ac.in/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("div", class_="b-ol-list-text-container")
    for result in results.find_all("a"):
        headline = result.text
        link = base_url + result.get("href").strip().replace(" ","")
        news_articles.append(('narula', headline, link))
    success.append('narula')
except Exception as e:
    failure.append(('narula', e))
    pass

#vnit
try:
    base_url = "https://vnit.ac.in/"
    url = "https://vnit.ac.in/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("div", class_="scroll-box")
    for result in results.find_all("a"):
        headline = result.text
        link= result.get("href").strip()
        news_articles.append(('vnit',headline,link))
    success.append('vnit')
except Exception as e:
    failure.append(('vnit',e))
    pass

#psitche
try:
    base_url = "https://psitche.ac.in/che.in/"
    url = "https://psitche.ac.in/che.in/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("div", class_="col-lg-8")
    for result in results.find_all("a"):
        headline = result.text
        link = base_url + result.get("href").strip()
        news_articles.append(('psitche', headline, link))
    success.append('psitche')
except Exception as e:
    failure.append(('psitche', e))
    pass

#gbu
try:
    base_url = "https://www.gbu.ac.in/"
    url = "https://www.gbu.ac.in/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("ul", class_="list-group list-group-flush")


    for result in results.find_all("li"):
        headline = result.a.text.strip()
        link= result.a.get("href").strip()
        if 'http' not in link:
            link=base_url+link
        news_articles.append(('gbu',headline,link))
    success.append('gbu')
except Exception as e:
    failure.append(('gbu',e))
    pass

#cujammu
try:
    base_url = "http://www.cujammu.ac.in/"
    url = "http://www.cujammu.ac.in//Default.aspx?artid=0&type=printallevents&prvtyp=site&option=s"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("div", class_="boxes-size")

    for result in results.find_all("a"):
        headline = result.text.strip()
        link = result.get("href").strip()
        news_articles.append(('cujammu', headline, link))
    success.append('cujammu')
except Exception as e:
    failure.append(('cujammu', e))
    pass

#bodoland
try:
    base_url = "https://www.bodolanduniversity.ac.in/"
    url = "https://www.bodolanduniversity.ac.in/"
    res = requests.get(url, verify=False)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("div", id="div1", class_="targetDiv")

    for result in results.find_all("a"):
        headline = result.text.strip()        
        link = base_url + result.get("href").strip()
        news_articles.append(('bodoland', headline, link))
    success.append('bodoland')
except Exception as e:
    failure.append(('bodoland', e))
    pass

#kufos
try:
    base_url = "http://kufos.ac.in/"
    url = "http://kufos.ac.in/"
    res = requests.get(url, verify=False)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("marquee", class_="kufos-marquee", style=" margin-top: 1px;")

    for result in results.find_all("a"):
        headline = result.text.strip()        
        link = base_url + result.get("href").strip()
        news_articles.append(('kufos', headline, link))
    success.append('kufos')
except Exception as e:
    failure.append(('kufos', e))
    pass

#iitbombay
try:
    base_url = "https://www.iitb.ac.in/"
    url = "https://www.iitb.ac.in/en/all-news"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("div", class_="view-content")
    for result in results.find_all("a"):
        headline = result.text
        link= base_url + result.get("href").strip()
        news_articles.append(('iitb',headline,link))
    success.append('iitb')
except Exception as e:
    failure.append(('iitb',e))
    pass

#cit
try:
    base_url = "https://cit.ac.in/"
    url = "https://cit.ac.in/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("div", id="noticeContainer")
    for result in results.find_all("a"):
        headline = result.text.replace('\n','')
        link =  result.get("href").strip()
        news_articles.append(('cit', headline, link))
    success.append('cit')
except Exception as e:
    failure.append(('cit', e))
    pass

#coep
try:
    base_url = "https://www.coep.org.in/"
    url = "https://www.coep.org.in/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("table", class_="views-table cols-2").tbody
    for result in results.find_all("a"):
        headline = result.text
        link = base_url + result.get("href").strip()
        news_articles.append(('coep', headline, link))
    success.append('coep')
except Exception as e:
    failure.append(('coep', e))
    pass

#rmkec
try:
    base_url = "http://www.rmkec.ac.in/"
    url = "http://www.rmkec.ac.in/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("div", class_="popular")
    for result in results.find_all("div", class_="media"):
        headline = result.a.text
        link =  result.a.get("href").strip()
        news_articles.append(('rmkec', headline, link))
    success.append('rmkec')
except Exception as e:
    failure.append(('rmkec', e))
    pass

#nsit
try:
    base_url = "http://www.nsit.ac.in/"
    url = "http://www.nsit.ac.in/news/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("div", class_="container col-md-9")
    for result in results.find_all("div", class_="media-body"):
        headline = result.h4.text
        link= result.a.get("href").strip()
        if 'http' not in link:
            link=base_url+link
        news_articles.append(('nsit',headline,link))
    success.append('nsit')
except Exception as e:
    failure.append(('nsit',e))
    pass

#mpsc
try:
    base_url="https://mpsc.gov.in/"
    url = "https://mpsc.gov.in/announcement_and_circular?m=4"
    res = requests.get(url, verify=False)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("table",id='datatable')
    for result in results.find_all("tr")[1:11]:
        headline = result.span.text.strip()
        link= base_url + result.a.get('href').strip()
        news_articles.append(('mpsc',headline,link))
    success.append('mpsc')
except Exception as e:
    failure.append(('mpsc',e))
    pass

#iimcal
try:
    base_url = "https://www.iimcal.ac.in/"
    url = "https://www.iimcal.ac.in/news"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("ul", class_="views-listing")
    for result in results.find_all("a"):
        headline = result.text
        link = result.get("href").strip()
        if 'http' not in link:
            link=base_url+link
        news_articles.append(('iimcal', headline, link))
    success.append('iimcal')
except Exception as e:
    failure.append(('iimcal', e))
    pass

#iiswbm
try:
    base_url = "https://www.iiswbm.edu/"
    url = "https://www.iiswbm.edu/latest-iiswbm/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("div", class_="row_block-box2 padding-left-right35")
    for result in results.find_all("a"):
        headline = result.text
        link =  result.get("href").strip()
        if 'http' not in link:
            link=base_url+link
        news_articles.append(('iiswbm', headline, link))
    success.append('iiswbm')
except Exception as e:
    failure.append(('iiswbm', e))
    pass

#fore
try:
    base_url = "https://www.fsm.ac.in/"
    url = "https://www.fsm.ac.in/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("div", class_="announcement-left")
    for result in results.find_all("a"):
        headline = result.text
        link =  result.get("href").strip()
        if 'http' not in link:
            link=base_url+link
        news_articles.append(('fore', headline, link))
    success.append('fore')
except Exception as e:
    failure.append(('fore', e))
    pass

#nitdgp
try:
    base_url = "https://nitdgp.ac.in/"
    url = "https://nitdgp.ac.in/p/admission-2021-1"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("div", class_="card-body")
    for result in results.find_all("li"):
        headline = result.a.text
        link= result.a.get("href").strip().replace(" ","%20")
        if 'http' in link:
            link = link
        else:
            link = base_url + link
        news_articles.append(('nitdgp',headline,link))
    success.append('nitdgp')
except Exception as e:
    failure.append(('nitdgp', e))
    pass

#narula
try:
    base_url = "https://www.nit.ac.in/"
    url = "https://www.nit.ac.in/news-events.php"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("div", class_="b-ol-list-text-container")
    for result in results.find_all("a"):
        headline = result.text
        link = base_url + result.get("href").strip().replace(" ","")
        news_articles.append(('narula', headline, link))
    success.append('narula')
except Exception as e:
    failure.append(('narula', e))
    pass

#JBIMS
try:
    url = "https://jbims.edu/category/notices/"
    res = requests.get(url,verify=False)
    soup = BeautifulSoup(res.text, "html.parser")
    head = soup.find('div',class_='col-md-8 blog-content').find_all('a')
    for h in head:
        headline = h.get_text().strip()[:999]
        links = h.get('href')
        news_articles.append(('JBIMS',headline,links))
    success.append(('JBIMS'))
except Exception as e:
    failure.append(('JBIMS',e))
    pass

#TAPMI
try:
    url = "https://www.tapmi.edu.in/newsroom/"
    baseurl = 'https://www.tapmi.edu.in/'
    res = requests.get(url,verify=False)
    soup = BeautifulSoup(res.text, "html.parser")
    head = soup.find_all('h2',class_='entry-title')
    for h in head:
        headline = h.get_text().strip()[:999]
        link =  h.find('a').get('href')
        news_articles.append(('TAPMI',headline,link))
    success.append(('TAPMI'))
except Exception as e:
    failure.append(('TAPMI',e))
    pass

#CU Chandigarh
try:
    url = 'https://news.cuchd.in/'
    #baseurl = 'http://www.sanskrit.nic.in/'
    res = requests.get(url)
    soup=BeautifulSoup(res.text,'html.parser')
    headline = soup.find('div',class_='grid-posts').find_all(class_='post-title')
    for news in headline:
        head = news.get_text().strip()[:999]
        link = news.find('a').get('href')
        news_articles.append(('CU',head,link))
    success.append('CU')
except Exception as e:
    failure.append(('CU',e))
    pass


#Kakatiya
try:
    url = 'https://kakatiya.ac.in/'
    res = requests.get(url)
    soup=BeautifulSoup(res.text,'html.parser')
    newss = soup.find('div',id='myTabContent',class_='tab-content').find_all('a',target='_blank',class_='homepagelinks')
    for news in newss:
        headline = news.get_text().strip()[:999]
        links = news.get('href')
        news_articles.append(('Kakatiya',headline,links))
    success.append(('Kakatiya'))
except Exception as e:
    failure.append(('Kakatiya',e))
    pass



#MAFSU
try:
    url = 'http://www.mafsu.in/#news-tab'
    baseurl = 'http://www.mafsu.in/'
    res = requests.get(url)
    soup=BeautifulSoup(res.text,'html.parser')
    newss = soup.find_all('a',target='_blank',style='color:Black; font-size:12px;')

    for news in newss:
        headline = news.get_text().strip()[:999]
        links =  news.get('href')
        if 'http' not in links:
            links=baseurl+links
        news_articles.append(('MAFSU',headline,links))
    success.append(('MAFSU'))
except Exception as e:
    failure.append(('MAFSU',e))
    pass

#SDSUV
try:
    url = 'https://www.sdsuv.ac.in/latest-news/'
    res = requests.get(url)
    soup=BeautifulSoup(res.text,'html.parser')
    newss = soup.find('div',class_='ResultDiv',style='width: 100%;').find_all('li')
    for news in newss:
        headline = news.get_text().strip()[:999]
        links = news.find('a').get('href')
        news_articles.append(('SDS University',headline,links))
    success.append('SDS University')
except Exception as e:
    failure.append(('SDS University',e))
    pass

#NFSU

try:
    url = 'https://www.nfsu.ac.in/news'
    res = requests.get(url)
    soup=BeautifulSoup(res.text,'html.parser')
    newss = soup.find_all('div',class_='gdlr-core-blog-full-head-right')
    for news in newss:
        headline = news.get_text().strip()[:999]
        links = news.find('a').get('href')
        news_articles.append(('NFSU University',headline,links))
    success.append('NFSU University')
except Exception as e:
    failure.append(('NFSU',e))
    pass

#NITT
try:
    url = 'https://www.nitt.edu/'
    baseurl = 'https://www.nitt.edu/'
    res = requests.get(url)
    soup=BeautifulSoup(res.text,'html.parser')
    link = soup.find_all('a',target='_new31')
    for l in link:
        l1 = l.get_text().strip()[:999]
        m1 = baseurl + l.get('href')
        news_articles.append(('NITT',l1,m1))
    success.append(('NITT'))
except Exception as e:
    failure.append(('NITT',e))
    pass

#VIT
try:
    url = 'https://www.vit.edu/index.php/news/latest-news'
    baseurl = 'https://www.vit.edu/'
    res = requests.get(url)
    soup=BeautifulSoup(res.text,'html.parser')
    head = soup.find_all('h3',class_='catItemTitle')
    links = soup.find_all('div',class_='catItemIntroText')
    for h in head:
        h1 = h.get_text().strip()[:999]
    for l in links:
        link = baseurl + l.find('a').get('href')
        news_articles.append(('VIT',h1,link))
    success.append(('VIT'))
except Exception as e:
    failure.append(('VIT',e))
    pass

#Hithaldia
try:
    url = 'https://hithaldia.ac.in/category/notice-board/'
    res = requests.get(url)
    soup=BeautifulSoup(res.text,'html.parser')
    head = soup.find_all('h2',class_='entry-title')

    for h in head:
        h1 = h.get_text().strip()[:999]
        link = h.find('a').get('href')
        news_articles.append(('Hithaldia',h1,link))
    success.append(('Hithaldia'))
except Exception as e:
    failure.append(('Hithaldia',e))
    pass

#JIS College
try:
    url = 'https://www.jiscollege.ac.in/notice-board.php'
    baseurl = 'https://www.jiscollege.ac.in/'
    res = requests.get(url)
    soup=BeautifulSoup(res.text,'html.parser')
    head = soup.find('div',class_='timeline-left').find_all('a',target='_blank')
    
    for h in head:
        h1 = h.get_text().strip()[:999]
        link = baseurl + h.get('href')
        news_articles.append(('JIS College',h1,link))
    success.append(('JIS College'))
except Exception as e:
    failure.append(('JIS College',e))
    pass


#Galgotia University
try:
    url = 'https://galgotiacollege.edu/notice-board'
    baseurl = 'https://www.jiscollege.ac.in/'
    res = requests.get(url)
    soup=BeautifulSoup(res.text,'html.parser')
    head = soup.find_all('div',class_='noticeTxt')

    for h in head:
        h1 = h.find('h5').get_text().strip()[:999]
        link = h.find('a').get('href')
        news_articles.append(('Galgotia University',h1,link))
    success.append(('Galgotia University'))
except Exception as e:
    failure.append(('Galgotia University',e))
    pass

try:
    url = 'https://svcolleges.edu.in/'
    baseurl = 'https://svcolleges.edu.in/'
    res = requests.get(url)
    soup=BeautifulSoup(res.text,'html.parser')
    head= soup.find_all('div',class_='col-9 section8_content')
    for h in head:
        h1 = h.find('h5').get_text().strip()[:999]
        links = baseurl + h.find('a').get('href')
        news_articles.append(('SV Colleges',h1,links))
    success.append(('SV Colleges'))
except Exception as e:
    failure.append(('SV Colleges',e))
    pass

#IIITN
try:
    url = 'https://iiitn.ac.in/news.php'
    baseurl = 'https://iiitn.ac.in/'
    res = requests.get(url)
    soup=BeautifulSoup(res.text,'html.parser')
    head= soup.find('ul',class_='catagorie-list').find_all('a',target='_blank')
    for h in head:
        h1 = h.get_text().strip()[:999]
        link = baseurl + h.get('href')
        news_articles.append(('IIITN',h1,link))
    success.append(('IIITN'))
except Exception as e:
    failure.append(('IIITN',e))
    pass

#UEM
try:
    url = 'https://uem.edu.in/uem-kolkata/tag/bulletin-board/'
    baseurl = 'https://uem.edu.in'
    res = requests.get(url)
    soup=BeautifulSoup(res.text,'html.parser')

    head = soup.find('div',class_='col-md-8').find_all('a')
    for h in head:
        h1 = h.get_text().strip()[:999]
        link = baseurl + h.get('href')
        news_articles.append(('UEM',h1,link))
    success.append(('UEM'))
except Exception as e:
    failure.append(('UEM',e))
    pass

#SPJIMR
try:
    url = 'https://www.spjimr.org/newsroom'
    baseurl = 'https://www.spjimr.org'
    res = requests.get(url)
    soup=BeautifulSoup(res.text,'html.parser')

    head = soup.find_all('div',class_='news-teaser-box')
    for h in head:
        h1 = h.get_text().strip()[:999]
        link = baseurl + h.find('a').get('href')
        news_articles.append(('SPJIMR',h1,link))
    success.append(('SPJIMR'))
except Exception as e:
    failure.append(('SPJIMR',e))
    pass

#WBJEE-CMS
try:
    
    url = "https://wbjeeb.nic.in/WBJEECMS/Page/Page?PageId=1&LangId=P"
    res = requests.get(url,verify=False)
    soup = BeautifulSoup(res.text, "html.parser")
    head = soup.find_all('span',class_='newspara',style='font-weight:bold')
    for h in head:
        headline = h.get_text().strip()[:999]
        link = h.find('a').get('href')
        news_articles.append(('WBJEE-CMS',headline,link))
    success.append(('WBJEE-CMS'))
except Exception as e:
    failure.append(('WBJEE-CMS',e))
    pass

#WBJEE-BoardCMS
try:
    url = "https://wbjeeb.nic.in/WBJEEBBoardCMS/Page/Page?PageId=1&LangId=P"
    res = requests.get(url,verify=False)
    soup = BeautifulSoup(res.text, "html.parser")
    head = soup.find_all('span',class_='newspara',style='font-weight:bold')
    for h in head:
        headline = h.get_text().strip()[:999]
        link = h.find('a').get('href')
        news_articles.append(('WBJEE-BoardCMS',headline,link))
    success.append(('WBJEE-BoardCMS'))
except Exception as e:
    failure.append(('WBJEE-BoardCMS',e))
    pass

#WBJEE-JENPASUG
try:
    url = "https://wbjeeb.nic.in/EXMJENPASUGCMS/Page/Page?PageId=1&LangId=P"
    res = requests.get(url,verify=False)
    soup = BeautifulSoup(res.text, "html.parser")
    head = soup.find_all('span',class_='newspara',style='font-weight:bold')
    for h in head:
        headline = h.get_text().strip()[:999]
        link = h.find('a').get('href')
        news_articles.append(('WBJEE-JENPASUG',headline,link))
    success.append(('WBJEE-JENPASUG'))
except Exception as e:
    failure.append(('WBJEE-JENPASUG',e))
    pass

#WBJEE-JELET
try:
    url = "https://wbjeeb.nic.in/EXMJELETCMS/Page/Page?PageId=1&LangId=P"
    res = requests.get(url,verify=False)
    soup = BeautifulSoup(res.text, "html.parser")
    head = soup.find_all('span',class_='newspara',style='font-weight:bold')
    for h in head:
        headline = h.get_text().strip()[:999]
        link = h.find('a').get('href')
        news_articles.append(('WBJEE-JELET',headline,link))
    success.append(('WBJEE-JELET'))
except Exception as e:
    failure.append(('WBJEE-JELET',e))
    pass

#WBJEE-JECA
try:
    url = "https://wbjeeb.nic.in/EXMJECACMS/Page/Page?PageId=1&LangId=P"
    res = requests.get(url,verify=False)
    soup = BeautifulSoup(res.text, "html.parser")
    head = soup.find_all('span',class_='newspara',style='font-weight:bold')
    for h in head:
        headline = h.get_text().strip()[:999]
        link = h.find('a').get('href')
        news_articles.append(('WBJEE-JECA',headline,link))
    success.append(('WBJEE-JECA'))
except Exception as e:
    failure.append(('WBJEE-JECA',e))
    pass

#WBJEE-ANM&GNM
try:
    url = "https://wbjeeb.nic.in/EXMANMGNMCMS/Page/Page?PageId=1&LangId=P"
    res = requests.get(url,verify=False)
    soup = BeautifulSoup(res.text, "html.parser")
    head = soup.find_all('span',class_='newspara',style='font-weight:bold')
    for h in head:
        headline = h.get_text().strip()[:999]
        link = h.find('a').get('href')
        news_articles.append(('WBJEE-ANM&GNM',headline,link))
    success.append(('WBJEE-ANM&GNM'))
except Exception as e:
    failure.append(('WBJEE-ANM&GNM',e))
    pass

#WBJEE-JEMScN
try:
    url = "https://wbjeeb.nic.in/EXMJEMSCNCMS/Page/Page?PageId=1&LangId=P"
    res = requests.get(url,verify=False)
    soup = BeautifulSoup(res.text, "html.parser")
    head = soup.find_all('span',class_='newspara',style='font-weight:bold')
    for h in head:
        headline = h.get_text().strip()[:999]
        link = h.find('a').get('href')
        news_articles.append(('WBJEE-JEMScN',headline,link))
    success.append(('WBJEE-JEMScN'))
except Exception as e:
    failure.append(('WBJEE-JEMScN',e))
    pass

#WBJEE-JEPBN
try:
    url = "https://wbjeeb.nic.in/EXMJEPBNCMS/Page/Page?PageId=1&LangId=P"
    res = requests.get(url,verify=False)
    soup = BeautifulSoup(res.text, "html.parser")
    head = soup.find_all('span',class_='newspara',style='font-weight:bold')
    for h in head:
        headline = h.get_text().strip()[:999]
        link = h.find('a').get('href')
        news_articles.append(('WBJEE-JEPBN',headline,link))
    success.append(('WBJEE-JEPBN'))
except Exception as e:
    failure.append(('WBJEE-JEPBN',e))
    pass

#OJEE (Edited)
try:
    url = "https://ojee.nic.in/ojeecms/Page/Page?PageId=1&LangId=P"
    baseurl = "https://www.srmist.edu.in/"
    res = requests.get(url,verify=False)
    soup = BeautifulSoup(res.text, "html.parser")
    head = soup.find('div',class_='col-lg-3 col-md-6 col-sm-12 col-xs-12').find_all('a')
    for h in head:
        headline = h.get_text().strip()[:999]
        links = h.get('href')
        news_articles.append(('OJEE',headline,links))
    
    success.append(('OJEE'))
except Exception as e:
    failure.append(('OJEE',e))
    pass


#dauniv_Non_CET
try:
    base_url = "https://www.dauniv.ac.in/"
    url = "https://www.dauniv.ac.in/NON-CET-Programmes2021"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("div", class_="main-content-div ordinance-div")
    for result in results.find_all("a"):
        headline = result.text.replace("\n","").replace("\t","").strip()
        link= result.get("href").strip()
        if 'http' not in link:
            link=base_url+link
        news_articles.append(('dauniv-non-cet',headline,link))
    success.append('dauniv-non-cet')
except Exception as e:
    failure.append(('dauniv-non-cet',e))
    pass

#dauniv-det
try:
    base_url = "https://www.dauniv.ac.in/"
    url = "https://www.dauniv.ac.in/det"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("div", class_="main-content-div")
    for result in results.find_all("a"):
        headline = result.text.replace("\n","").replace("\t","").strip()
        link= result.get("href").strip()
        if 'http' not in link:
            link=base_url+link
        news_articles.append(('dauniv-det',headline,link))
    success.append('dauniv-det')
except Exception as e:
    failure.append(('dauniv-det',e))
    pass

# makaut
try:
    base_url = "https://makautwb.ac.in/"
    url = "https://makautwb.ac.in/page.php?id=340"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("div", class_="col-md-9").find_all("a")
    for result in results:
        headline = result.text.strip()
        link= base_url+result.get("href").strip()
        news_articles.append(('makaut',headline,link))
        
    success.append('makaut')
except Exception as e:
    failure.append(('makaut',e))
    pass

#NIT Andhra (edited)
try:
    base_url = "http://www.nitandhra.ac.in"
    url = "http://www.nitandhra.ac.in/main/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("div" , class_="container body-container").find_all("a")
    for result in results:
        headline=result.text.strip()
        link=result.get("href").replace(" ", "%20")
        if "http" in link:
            link=link
        else:
            link=url+link
        news_articles.append(('nit andhra',headline,link)) 
       
    success.append('nit andhra') 
except Exception as e:
    failure.append(('nit andhra',e))
    pass


# iit guwahati
try:
    base_url = "https://www.iitg.ac.in/"
    url = "https://www.iitg.ac.in/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("div", class_="tab-pane fade in active").find_all("li")
    for result in results:
        headline = result.find('a').text.strip()
        link= result.a.get("href").strip()
        if 'http' not in link:
            link=base_url+link
        news_articles.append(('iit guwahati',headline,link))  
    success.append('iit guwahati')
except Exception as e:
    failure.append(('iit guwahati',e))
    pass

# iiit bhubaneswar
try:
    name ='IIIT Bhubaneswar'
    base_url= "https://www.iiit-bh.ac.in/"
    url = "https://www.iiit-bh.ac.in/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find_all("p", class_="CDt4Ke zfr3Q")
    for result in results :
        result=result.find_all('a')
        for r in result:
            headline = r.text
            link = r.get('href')
            if 'http' not in link:
                link=base_url+link
            news_articles.append((name,headline,link))   
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass



# bput
try:
    url = 'http://www.bput.ac.in/news.php'
    base_url='http://www.bput.ac.in/'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    results = soup.find_all('tr')
    for result in results:
        headline = result.find('a').text
        link = result.find('a').get('href')
        if 'http' not in link:
            link=base_url+link
        news_articles.append(('bput',headline,link))
    success.append('bput')
except Exception as e:
    failure.append(('bput',e))
    pass

# MMMUT
try:
    name="MMMUT"
    base_url = "http://www.mmmut.ac.in/"
    url = "http://www.mmmut.ac.in/AllNews"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find('div',class_="w_content pt-20 mt-0").find_all('a')
    for result in results[2:15:2]:
        headline = result.text.strip().replace('Download','')
        link= base_url+result.get("href")
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

#Thiruvalluvar University
try:
    name="Thiruvalluvar University"
    base_url = "https://www.tvu.edu.in"
    url = "https://www.tvu.edu.in/admission/circular/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find('ul',class_="list").find_all('a')
    for result in results:
        headline = result.text.strip()
        link= result.get("href")
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

#KRU
try:
    name="KRU"
    base_url = "https://kru.ac.in/"
    url = "https://kru.ac.in/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find_all('div',class_="title_small_post")
    for result in results:
        headline = result.text.strip().replace('Download','')
        link= result.find('a').get("href")
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# Vikram Univ
try:
    name="Vikram Univ"
    base_url = "https://vikramuniv.ac.in/"
    url = "https://vikramuniv.ac.in/index.php/en/information-notification/academic-notice"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find_all('td',class_="list-title")
    for result in results:
        headline = result.text.strip()
        link= base_url+result.find('a').get("href")
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

#JNU
try:
    name="JNU"
    base_url = "http://www.jnu.ac.in/"
    url = "http://www.jnu.ac.in/notices"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find('table',class_="views-table views-view-table cols-4").find_all('td',headers="view-title-table-column")
    for result in results:
        headline = result.text.strip()
        link=result.find('a').get("href")
        if 'http' in link:
            link= link
        else:
            link= base_url+link
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# IISER TVM

try:
    name="IISER TVM"
    base_url = "https://www.iisertvm.ac.in/"
    url = "https://www.iisertvm.ac.in/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find_all('div',class_="card_row")
    for result in results[4:]:
        result=result.find_all('a')
        for r in result:
            headline = r.text
            link=r.get("href")
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass


#Central University of Punjab
try:
    name="Central University of Punjab"
    url = "http://cup.edu.in/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find_all('div',class_="field field--name-body field--type-text-with-summary field--label-hidden field__item")
    for result in results[:2]:
        result= result.find_all('a')
        for r in result:
                headline=r.text
                link = r.get('href')
                if 'http' in link:
                        link= link
                else:
                    link= url+link
                news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

#MSIT
try:
    name="MSIT"
    base_url= "https://www.msit.in"
    url = "https://www.msit.in/latest_news"
    res = requests.get(url,verify = False)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("div", class_="tab-content").find_all('a')
    for result in results:
        headline= result.text
        link= base_url+result.get('href')
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

#IITRPR
try:
    name="IITRPR"
    base_url= "https://www.iitrpr.ac.in/"
    url = "https://www.iitrpr.ac.in/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find_all('p',align="justify")
    for result in results:
        headline= result.text
        link= result.find('a').get('href')
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass


#New Horizon College of Engineering-NHCE
try:
    name="NHCE"
    base_url= "https://newhorizonindia.edu"
    url = "https://newhorizonindia.edu/nhengineering/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find_all('h4',class_="title")
    for result in results:
        headline= result.text.strip()
        link= result.find('a').get('href')
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

#IIMU
try:
    name="IIMU"
    base_url= "https://www.iimu.ac.in"
    url = "https://www.iimu.ac.in/media/news"
    res = requests.get(url,verify=False)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find_all('div',class_="evetntitle")
    for result in results:
        result=result.find_all('a')
        for r in result:
            headline= r.text.strip()
            link= r.get('href')
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

#XISS
try:
    name="XISS"
    base_url= "http://www.xiss.ac.in/"
    url = "http://www.xiss.ac.in/#"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("div", class_="news-section").find_all('a')
    for result in results:
        headline = result.text
        link= result.get("href").strip()
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

#SSUHS
try:
    name="SSUHS"
    url = "http://ssuhs.in/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("ul", class_="news-list").find_all('a')
    for result in results:
        headline = result.text
        link= url+result.get("href").replace('./','').strip()
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# KPSC
try:
    name = "Kerala psc"
    base_url = 'https://www.keralapsc.gov.in'
    url = 'https://www.keralapsc.gov.in/latest'
    #time.sleep(3)
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    results = soup.find('tbody').find_all('tr')
    for result in results[:10]:
        headline = result.find('td', headers="view-title-table-column").text.strip().replace('Download', '')
        link = base_url + result.find('a').get('href')
        news_articles.append((name, headline, link))
    success.append(name)
except Exception as e:
    failure.append((name, e))
    pass

# RPSC
try:
    name = "RPSC"
    base_url = 'https://rpsc.rajasthan.gov.in/'
    url = "https://rpsc.rajasthan.gov.in/examdashboard"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    results = soup.find_all('table', class_="examCalTable")
    for result in results:
        result = result.find_all('tr')
        for r in result:
            headline = r.span.text
            link = r.find('a').get('href')
            if 'javascript' in link:
                continue
            else:
                link = base_url + link
            news_articles.append((name, headline, link))
    success.append(name)
except Exception as e:
    failure.append((name, e))
    pass

# TNPSC
try:
    name = "TNPSC"
    base_url = 'https://www.tnpsc.gov.in/'
    url = 'https://www.tnpsc.gov.in/English/Notification.aspx'
    res = requests.get(url, verify=False)
    soup = BeautifulSoup(res.text, 'html.parser')
    results = soup.find_all('a', class_="viewlink")
    for result in results[:10]:
        headline = result.text
        link = base_url + (result.get('href'))[2:]
        news_articles.append((name, headline, link))
    success.append(name)
except Exception as e:
    failure.append((name, e))
    pass

# MPPEB
try:
    name = "MPPEB"
    base_url = 'http://peb.mp.gov.in/advertisement/'
    url = 'http://peb.mp.gov.in/advertisement/Important_message_candidate.htm'
    res = requests.get(url, verify=False)
    soup = BeautifulSoup(res.text, 'html.parser')
    results = soup.find_all('tr')
    for result in results[1:11]:
        headline = result.find('font').text.replace('Click Here', '').replace('\n', '').strip()
        link = base_url + result.find('font', face="Times New Roman").a.get('href')
        news_articles.append((name, headline, link))
    success.append(name)
except Exception as e:
    failure.append((name, e))
    pass
# GPSC
try:
    name = "GPSC"
    base_url = 'https://gpsc.gujarat.gov.in'
    url = 'https://gpsc.gujarat.gov.in/newseventlist'
    res = requests.get(url, verify=False)
    soup = BeautifulSoup(res.text, 'html.parser')
    results = soup.find('ul', id="ctl13_Newli").find_all('li')
    for result in results[:10]:
        headline = result.text.strip()
        link = base_url + result.a.get('href')
        news_articles.append((name, headline, link))
    success.append(name)
except Exception as e:
    failure.append((name, e))
    pass

# KSET
try:
    name = "KSET"
    url = "http://kset.uni-mysore.ac.in/"
    res = requests.get(url, verify=False)
    soup = BeautifulSoup(res.text, 'html.parser')
    results = soup.find_all('div', class_="media-body")
    for result in results[:4]:
        headline = result.text[14:].replace('NEW', '').replace('Click here', '').strip()
        link = url + result.find('a').get('href')
        news_articles.append((name, headline, link))
    success.append(name)
except Exception as e:
    failure.append((name, e))
    pass

# PSC
try:
    name = "PSC"
    url = 'http://www.psc.cg.gov.in'
    res = requests.get(url, verify=False)
    soup = BeautifulSoup(res.text, 'html.parser')
    results = soup.find_all('a', class_="style409")
    for result in results:
        headline = result.text
        link = url + result.get('href')[2:]
        news_articles.append((name, headline, link))
    success.append(name)
except Exception as e:
    failure.append((name, e))
    pass

#iim jammu
try:
    name="iim jammu"
    base_url = "http://www.iimj.ac.in"
    url = "http://www.iimj.ac.in/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("ul", class_="list5").find_all("li")
    for result in results:
        headline = result.find("a").text.strip()
        link=result.a.get("href")
        if "http" in link:
            link=link
        else:
            link=base_url+link
        news_articles.append((name,headline,link))
        
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

#cluster university jammu
try:
    name="cu jammu"
    base_url = "https://www.clujammu.in/"
    url = "https://www.clujammu.in/index.php"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("table", class_="table table-bordered table-condensed table-hover table-striped").find("tbody")
    for result in results.find_all("b")[:10]:
        headline=result.text.strip()
        link=base_url+result.a.get("href").replace(' ','%20').strip()
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass


#mamc
try:
    name="mamc"
    base_url = "https://www.mamc.ac.in/"
    url = "https://www.mamc.ac.in/News/allnews"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("div", class_="col-sm-12").find_all("li")
    for result in results[:10]:
        headline = result.text.strip()
        link=result.a.get("href")
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

#grau
try:
    name="grau punjab"
    base_url = "http://www.graupunjab.org"
    url = "http://www.graupunjab.org/rotat.html"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find_all("a")
    for result in results[:10]:
        headline=result.text.strip()
        link=base_url+result.get("href")[1:]
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# Ayurved University
try:
    name = "Ayurved University"
    base_url = "https://ayurveduniversity.edu.in"
    url = "https://ayurveduniversity.edu.in/index1.php"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find('ul', id="vertical-ticker").find_all('a')
    for result in results[:10]:
        headline = result.text
        link = result.get("href")
        if 'http' in link:
            link = link[6:]
        else:
            link = base_url + link[8:]
        news_articles.append((name, headline, link))
    success.append(name)
except Exception as e:
    failure.append((name, e))
    pass

# AIIMS Bhubaneshwar
try:
    name = "AIIMS Bhubaneshwar"
    base_url = "https://aiimsbhubaneswar.nic.in/"
    url = "https://aiimsbhubaneswar.nic.in/whatsNew.aspx"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find('ul', class_="list-unstyled whatNewStyle").find_all('a')
    for result in results[:10]:
        headline = result.text.replace('\r\n', '').strip()
        link = base_url + result.get("href")
        news_articles.append((name, headline, link))
    success.append(name)
except Exception as e:
    failure.append((name, e))
    pass


# Telangana Univeristy
try:
    name = "Telangana University"
    url = 'http://www.telanganauniversity.ac.in/'
    res = requests.get(url, verify=False)
    soup = BeautifulSoup(res.text, 'html.parser')
    results = soup.find_all('marquee', direction="up")
    for result in results:
        result = result.find_all('a')
        for r in result:
            headline = r.text.replace('\n', '').strip()
            link = r.get('href').replace(' ', '%20')
            if 'http' in link:
                  link=link
            else:
                link = url + link
            news_articles.append((name, headline, link))
    success.append(name)
except Exception as e:
    failure.append((name, e))
    pass

# Satyabhama
try:
    name = "Satyabhama"
    url = "https://www.sathyabama.ac.in/"
    res = requests.get(url, verify=False)
    soup = BeautifulSoup(res.text, 'html.parser')
    results = soup.find('marquee', class_="view-content").find_all('a')
    for result in results:
        headline = result.text
        link = url + result.get('href')
        news_articles.append((name, headline, link))
    success.append(name)
except Exception as e:
    failure.append((name, e))
    pass

# mait
try:
    base_url = 'https://mait.ac.in'
    url = 'https://mait.ac.in/'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    results = soup.find_all('div', class_ = 'crs_div')
    for result in results:
        headline = result.find('a').text
        link = base_url + result.find('a').get('href')
        news_articles.append(('mait',headline,link))
    success.append('mait')
except Exception as e:
    failure.append(('mait',e))
    pass

# iim lucknow
try:
    url = 'https://www.iiml.ac.in/news-and-announcement'
    base_url='https://www.iiml.ac.in/'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    results = soup.find('tbody', id = 'myTable').find_all('tr')
    for result in results:
        headline = result.find('a').text
        link = result.find('a').get('href')
        if 'http' not in link:
            link=base_url+link
        news_articles.append(('iim lucknow',headline,link))
    success.append('iim lucknow')
except Exception as e:
    failure.append(('iim lucknow',e))
    pass


# aiims bhopal
try:
    url = 'https://aiimsbhopal.edu.in/index_controller/circulerNotice#SHTM'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    results = soup.find('tbody').find_all('tr')
    for result in results:
        headline = result.find('td').text
        link = result.find('a').get('href')
        news_articles.append(('aiims bhopal',headline,link))
    success.append('aiims bhopal')
except Exception as e:
    failure.append(('aiims bhopal',e))
    pass

# lhmc
try:
    base_url = 'http://lhmc-hosp.gov.in/'
    url = 'http://lhmc-hosp.gov.in/index4.php?lang=1&level=0&linkid=73&lid=73'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    results = soup.find('div', class_ = 'file_type_list').find_all('li', class_ = 'sublink')
    for result in results:
        headline = result.find('a').text
        link = base_url + result.find('a').get('href')
        news_articles.append(('lhmc',headline,link))
    success.append('lhmc')
except Exception as e:
    failure.append(('lhmc',e))
    pass

# amch
try:
    base_url = 'https://amch.edu.in'
    url = 'https://amch.edu.in/'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    results = soup.find_all('div', class_ = 'a-block')
    for result in results:
        headline = result.find('a').text
        link = base_url + result.find('a').get('href')
        news_articles.append(('amch',headline,link))
    success.append('amch')
except Exception as e:
    failure.append(('amch',e))
    pass

#IIITG
try:
    name="IIIT Guwahati"
    url="http://www.iiitg.ac.in/"
    res = requests.get(url,verify=False)
    soup = BeautifulSoup(res.text,'html.parser')
    results = soup.find('div',style="padding:0;").find_all('a')
    for result in results:
        headline=result.text.replace('\n','').strip()
        link=result.get('href')
        if 'http' in link:
            link=link
        else:
            link= url+link
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

#AEC
try:
    name="AEC"
    base_url='https://aec.edu.in/'
    url="https://aec.edu.in/?p=Updates"
    res = requests.get(url)
    soup = BeautifulSoup(res.text,'html.parser')
    results = soup.find('table').find_all('div',class_="notice notice-success")
    for result in results[:10]:
        headline=result.strong.text.replace('\n','').strip()
        link=base_url+result.a.get('href').replace(' ','%20')
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

#PUMBA
try:
    name="PUMBA"
    url="https://www.pumba.in/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text,'html.parser')
    results = soup.find('marquee').find_all('a')
    for result in results[:10]:
        headline=result.text.strip()
        link=url+result.get('href').replace(' ','%20')
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# AIIMS JODHPUR
try:
    name="AIIMS Jodhpur"
    url="https://www.aiims.edu/en.html"
    res = requests.get(url)
    soup = BeautifulSoup(res.text,'html.parser')
    results = soup.find_all('div',id="news-container")
    for result in results[1:2]:
        result=result.find_all('a')
        for r in result:
            headline=r.text.strip()
            link=r.get('href').replace(' ','%20')
            news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

#NIFTEM
try:
    name="NIFTEM"
    url="http://niftem.ac.in/newsite/?page_id=1159"
    res = requests.get(url)
    soup = BeautifulSoup(res.text,'html.parser')
    results = soup.find('table').find_all('tr')
    for result in results[1:8]:
        headline=result.text[3:].replace('View','').strip()
        link=result.a.get('href')
        if '#' in link:
            link='http://niftem.ac.in/newsite/?page_id=1159#'
        else:
            link=link
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# SPCE (edited)
try:
    name="SPCE"
    base_url='https://www.spce.ac.in/'
    url = "https://www.spce.ac.in/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    resul = soup.find_all("div", class_="list-type2")[6]
    results = resul.find_all('li')
    for result in results:
        headline=result.text
        link=base_url+result.a.get("href").replace(" ", "%20")
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# dibru
try:
    url = 'https://dibru.ac.in/admission2021n/'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    results = soup.find_all('p')
    for result in results:
        headline = result.find('a').text
        link = result.find('a').get('href')
        news_articles.append(('dibrugarh university',headline,link))
    success.append('dibrugarh university')
except Exception as e:
    failure.append(('dibrugarh university',e))
    pass

#Punjab University
try:
    base_url = "https://puchd.ac.in/"
    url = "https://news.puchd.ac.in/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text,"html.parser")
    results = soup.find('table').find_all('div',itemtype="http://schema.org/Article")
    for result in results:
        headline=result.find('div',itemprop="name").text.strip()
        link= url+result.a.get('href').replace('%E2%80%92','-')
        news_articles.append(('Punjab University',headline,link))
    success.append(name)
except Exception as e:
    failure.append(('Punjab University',e))
    pass

#TMU
try:
    name="TMU"
    url = "https://www.tmu.ac.in/tmu/announcement"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find_all("section",class_="toggle" )
    for result in results:
            headline = result.find('span',style="padding-left:5px").text
            link= result.a.get("href")
            news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

#NIT RR

try:
    name="NIT Raipur"
    base_url= "http://www.nitrr.ac.in/"
    url = "http://www.nitrr.ac.in/admission.php#menu4"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find_all('div',class_="panel-body")
    for result in results[:4] :
        result=result.find_all('a')
        for r  in result:
            headline = r.text.strip()
            link= base_url+r.get('href').replace(' ','%20')
            news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

#BFUHS
try:
    name="BFUHS"
    base_url="https://bfuhs.ac.in/"
    url = "https://bfuhs.ac.in/#"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find('td',width="92%").find_all('a')
    for result in results:
        headline= result.text.strip()
        link=result.get('href').replace(' ','%20')
        if headline=='':
            continue
        elif 'http' in link:
            link=link.strip()
        else:
            link = base_url+link.strip()
            news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

#NEIGRIHMS
try:
    name="NEIGRIHMS"
    base_url = "http://www.neigrihms.gov.in/"
    url = "http://www.neigrihms.gov.in/examsnotification.html"
    res = requests.get(url,verify=False)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find('div',align="left").find_all('a')
    for result in results:
        headline= result.text.strip()
        if headline=='':
            continue
        link=base_url+result.get('href').replace(' ','%20')
        news_articles.append((name, headline, link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

#AIIMS Raipur
try:
    name="AIIMS Raipur"
    base_url = "https://www.aiimsraipur.edu.in"
    url = "https://www.aiimsraipur.edu.in/user/student-admissions.php"
    res = requests.get(url,verify=False)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find('tbody').find_all('tr')

    for result in results[:10]:
        headline= result.text.replace('Link','').replace('Download','').replace('\n','').strip()[1:]
        link=result.find('a',target="_blank").get('href').replace(' ','%20')
        if 'http' in link :
            link=link
        else:
            link=base_url+link[2:]
        news_articles.append((name, headline, link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

#NIT Karnataka
try:
    name ='NIT Karnataka'
    base_url= "https://www.nitk.ac.in/"
    url = "https://www.nitk.ac.in/announcements"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find_all("tr")
    for result in results[:10]:
        headline=result.a.text.strip()
        link=base_url+result.find("a", target="_blank").get("href")
        news_articles.append((name,headline,link))   
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

#iim sirmaur(announcements)
try:
    name="iim sirmaur"
    base_url = "https://www.iimsirmaur.ac.in/"
    url = "https://www.iimsirmaur.ac.in/iims/announcements"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find_all("div", class_="panel-body")
    for result in results[:10]:
            headline=result.find("h1").text.replace("\t\t\t\t\t\r\n\t\t\t\t\t\t","").strip()
            link=base_url+result.find("a").get("href")
            news_articles.append((name,headline,link))
        
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

#shekhawati university
try:
    base_url = "http://www.shekhauni.ac.in/"
    url = "http://www.shekhauni.ac.in/allnews.aspx"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("table", class_="table table-striped table-bordered table-hover")
    for result in results.find_all("a"):
        headline = result.text
        link= base_url+result.get("href").strip()
        news_articles.append(('shekhawati university',headline,link))
    success.append('shekhawati university')
except Exception as e:
    failure.append(('shekhawati university',e))
    pass

# ycmou
try:
    name="ycmou"
    url = "https://ycmou.ac.in/news"
    base_url = 'https://ycmou.ac.in/'
    res = requests.get(url,verify=False)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find_all("tr")[1:]
    for result in results:
        headline=result.find_all("td")[1].text
        link=result.find('a').get("href")
        news_articles.append((name,headline,link))
    success.append((name))
except Exception as e:
    failure.append((name,e))
    pass



# SOL

try:
    name="sol"
    url = "https://web.sol.du.ac.in/info/archive-notices-information"
    base_url = 'https://web.sol.du.ac.in/'
    res = requests.get(url,verify=False)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("ul", class_="marked-list").find_all("a")
    for result in results[:9]:
        headline=result.text.strip()
        link=result.get("href").replace(" ", "%20")
        news_articles.append((name,headline,link))
    success.append((name))
except Exception as e:
    failure.append((name,e))
    pass

# BRAOU

try:
    name="braou"
    url = "http://www.braou.ac.in/LatestUpdatesInfo.aspx"
    base_url = 'http://www.braou.ac.in/'
    res = requests.get(url,verify=False)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("ul", id="Jumbotron_ulGetLatestupdates").find_all("a")
    for result in results[:9]:
        headline=result.text.strip()
        link=result.get("href").replace(" ", "%20")
        news_articles.append((name,headline,link))
    success.append((name))
except Exception as e:
    failure.append((name,e))
    pass

# UPRTOU
try:
    name="uprtou"
    url = "http://14.139.237.190/news_layout_page.php?id=admission"
    base_url = 'http://www.uprtou.ac.in/'
    res = requests.get(url,verify=False)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("ul", class_="navigation").find_all("a")
    for result in results[:9]:
        headline=result.text.strip()
        link=result.get("href")
        if "http" in link:
            link=link
        else:
            link="http://14.139.237.190/"+link
        news_articles.append((name,headline,link))
    success.append((name))
except Exception as e:
    failure.append((name,e))
    pass


# LOYOLA
try:
    name="loyola college"
    url = "https://www.loyolacollege.edu/events/current_events"
    base_url = 'https://www.loyolacollege.edu/'
    res = requests.get(url,verify=False)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find_all("tr")[1:6]
    for result in results:
        if ("result.a"==None):
            continue
        else:
            result=result.find_all("a")
            for r in result:
                headline=r.text.replace("\xa0", " ").replace("\n", "").strip()
                link=base_url+r.get("href")
                news_articles.append((name,headline,link))
    success.append((name))
except Exception as e:
    failure.append((name,e))
    pass


# Sastra
try:
    name="sastra"
    url = "https://www.sastra.edu/headlines-archives.html"
    base_url = 'https://www.sastra.edu'
    res = requests.get(url,verify=False)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find_all("tr")[1:]
    for result in results:
        headline=result.a.text.strip()
        link=base_url+result.a.get("href")
        news_articles.append((name,headline,link))
    success.append((name))
except Exception as e:
    failure.append((name,e))
    pass

#VMOU
try:
    name ='VMOU '
    url = "https://www.vmou.ac.in/notice/admissions"
    base_url="https://www.vmou.ac.in"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("table", class_="views-table cols-0").find_all("tr")
    for result in results:
        headline=result.a.text.strip()
        link=base_url+result.a.get("href")
        news_articles.append((name,headline,link))   
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# Hansraj college

try:
    name ='hansraj college'
    url = "https://www.hansrajcollege.ac.in/announcements"
    base_url="https://www.hansrajcollege.ac.in/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find_all("tr")[1:11]
    for result in results:
        headline=result.find("td").text.strip()
        link=result.find("a").get("href")
        news_articles.append((name,headline,link))   
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass
    


# Gargi college

try:
    name ='gargi college'
    url = "https://gargicollege.in/notice/"
    base_url="https://gargicollege.in/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find_all("tr")[1:11]
    for result in results:
        link=result.a.get('href')
        result=result.find_all("td")
        for r in result[1:2]:
            headline = r.text
            link=link
            news_articles.append((name,headline,link))   
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# Asutosh college
try:
    name ='asutosh college'
    url = "https://asutoshcollege.in/new-web/"
    base_url="https://asutoshcollege.in/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("marquee", direction="up").find_all("li")
    for result in results:
        headline=result.text.replace(": Click Here","").strip()
        link=url+result.a.get("href").replace(" ", "%20")
        news_articles.append((name,headline,link))   
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# Fergusson college
try:
    name ='fergusson college'
    url = "https://www.fergusson.edu/news/index"
    base_url="https://www.fergusson.edu/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("marquee").find_all("a")
    for result in results:
        headline=result.text.replace('*','').strip()
        link=result.get("href")
        news_articles.append((name,headline,link))   
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# Miranda house
try:
    name ='Miranda house'
    url = "https://www.mirandahouse.ac.in/notice.php"
    base_url="https://www.mirandahouse.ac.in/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find_all("tr")[1:11]
    for result in results:
        headline=result.a.text.strip()    
        link=result.a.get("href")
        news_articles.append((name,headline,link))   
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass


# Vivekananda college
try:
    name ='Vivekananda college'
    url = "https://vivekanandacollege.edu.in/notice-board/"
    base_url="https://vivekanandacollege.edu.in"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("div", class_="entry-content").find_all("li")
    for result in results[:9]:
        headline=result.a.text.strip()
        link=result.a.get("href")
        news_articles.append((name,headline,link))   
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass


# ftii
try:
    name ='ftii'
    url = "https://www.ftii.ac.in/announcement"
    base_url="https://www.ftii.ac.in/announcement"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find_all("tr")[1:]
    for result in results[:9]:
        headline=result.a.text.strip()
        link=result.a.get("href")
        news_articles.append((name,headline,link))   
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass


# kalindi college
try:
    name ='kalindi college'
    url = "https://www.kalindicollege.in/notice/#general"
    base_url="https://www.kalindicollege.in/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find_all("tr")[1:11]
    for result in results:
        link=result.a.get('href')
        result=result.find_all("td")
        for r in result[1:2]:
            headline = r.text
            link=link
        news_articles.append((name,headline,link))   
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# satyawati college
try:
    name ='satyawati college'
    url = "http://satyawati.du.ac.in/CIRCULARS.HTML"
    base_url="http://satyawati.du.ac.in/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find_all("tr")[1:11]
    for result in results:
        headline=result.find("td").text.strip()
        link=base_url+result.a.get("href").replace(" ","%20")
        news_articles.append((name,headline,link))   
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# srcc
try:
    name ='srcc'
    url = "https://www.srcc.edu/announcements"
    base_url="https://www.srcc.edu/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find_all("div", class_="annoncementList")
    for result in results[:9]:
        headline=result.a.text.strip()
        link=base_url+result.a.get("href").replace(" ", "%20")
        news_articles.append((name,headline,link))   
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# bangabasi college

try:
    name ='bangabasi college'
    url = "https://www.bangabasi.ac.in/"
    base_url="https://www.bangabasi.ac.in/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find_all("div", class_="n-body")[1].find_all("a")
    for result in results:
        headline=result.text.strip()
        link=base_url+result.get("href").replace(" ", "%20")
        news_articles.append((name,headline,link))   
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# patna women college
try:
    name ='patna women college'
    url = "https://patnawomenscollege.in/notice-board/"
    base_url="https://patnawomenscollege.in/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find_all("tr")[2:12]
    for result in results:
        link=result.a.get("href")
        result=result.find_all("td")[1:2]
        for r in result:
            headline=r.text
            link=link
        news_articles.append((name,headline,link))   
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# rajdhani college

try:
    name ='rajdhani college'
    url = "https://www.rajdhanicollege.ac.in/"
    base_url="https://www.rajdhanicollege.ac.in/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("div", id="General").find_all("a")
    for result in results[:9]:
        headline=result.text.strip()
        link=base_url+result.get("href")
        news_articles.append((name,headline,link))   
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# apsurewa
try:
    url = 'http://apsurewa.ac.in/notification/category/news-and-notifications?&offset='
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    results = soup.find('div', class_ = 'col-md-8 workarea margin-b-20').find_all('div', class_ = 'row')[1:]
    for result in results:
        headline = result.find('a').text
        link = result.find('a').get('href')
        news_articles.append(('apsurewa',headline,link))
    success.append('apsurewa')
except Exception as e:
    failure.append(('apsurewa',e))
    pass

# aurobindo university
try:
    url = 'http://aurobindo.du.ac.in/'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    results = soup.find('ul', class_ = 'list').find_all('li')
    for result in results:
        headline = result.find('a').text
        link = url + result.find('a').get('href')
        news_articles.append(('aurobindo university',headline,link))
    success.append('aurobindo university')
except Exception as e:
    failure.append(('aurobindo university',e))
    pass


# tnou
try:
    url = 'https://tnou.ac.in/news-and-events/'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    results = soup.find('ul', class_ = 'news-list').find_all('li')
    for result in results:
        headline = result.find('h4').text
        link = result.find('a').get('href')
        news_articles.append(('tnou',headline,link))
    success.append('tnou')
except Exception as e:
    failure.append(('tnou',e))
    pass

# marivanios college
try:
    url = 'https://www.marivanioscollege.com/'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    results = soup.find('div', class_ = 'col-sm-12 col-md-4').find_all('div', class_ = 'event media mt-0 no-bg no-border')
    for result in results:
        headline = result.find('a').text
        link = result.find('a').get('href')
        news_articles.append(('marivanios college',headline,link))
    success.append('marivanios college')
except Exception as e:
    failure.append(('marivanios college',e))
    pass

#  ranaghat college
try:
    url = 'http://www.ranaghatcollege.org.in/'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    results = soup.find('tr').find_all('p')
    for result in results:
        try:
            headline = result.find('a').text
            link = url + result.find('a').get('href')
        except:
            None
        news_articles.append(('ranaghat college',headline,link))
    success.append('ranaghat college')
except Exception as e:
    failure.append(('ranaghat college',e))
    pass

# uluberia college
try:
    url = 'https://www.uluberiacollege.in/site/all_notice/1'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    results = soup.find('div', class_ = 'table-responsive').find_all('tr')[1:]
    for result in results:
        headline = result.find('td').find_next_sibling('td').text
        link = result.find('a').get('href')
        news_articles.append(('uluberia college',headline,link))
    success.append('uluberia college')
except Exception as e:
    failure.append(('uluberia college',e))
    pass

# tnau

try:
    name ='tnau'
    url = "https://tnau.ac.in/news-events/"
    base_url="https://tnau.ac.in"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("div", class_="wpb_wrapper").find_all("a")
    for result in results:
        headline=result.text.strip()
        link=result.get("href")
        news_articles.append((name,headline,link))   
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# ramjas college

try:
    name ='ramjas college'
    url = "https://ramjas.du.ac.in/college/web/index.php"
    base_url="https://ramjas.du.ac.in/"
    res = requests.get(url, verify=False)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("div", class_="panel-content").find_all("a")
    for result in results[:9]:
        headline=result.text.strip()
        link=result.get("href")
        if "http" in link:
            link=link
        else:
            link=base_url+link
        news_articles.append((name,headline,link))   
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# kirori mal
try:
    name ='kirori mal'
    url = "http://kmc.du.ac.in/category/latest-news/"
    base_url="http://kmc.du.ac.in"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find_all("h3", class_="entry-title")
    for result in results:
        headline=result.text.strip()
        link=result.a.get("href")
        news_articles.append((name,headline,link))   
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# motilal nehru

try:
    name ='motilal nehru'
    url = "http://www.mlncdu.ac.in/news.html"
    base_url="http://www.mlncdu.ac.in/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("ul", type="square").find_all("a")
    for result in results[:9]:
        headline=result.text.strip()
        link=base_url+result.get("href")
        news_articles.append((name,headline,link))   
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# NLU
try:
    name ='NLU'
    url = "https://nludelhi.ac.in/Annuoncement.aspx"
    base_url="https://nludelhi.ac.in/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find('ul',style="overflow:auto;").find_all("li",style='')
    for result in results[:9]:
        headline=result.text.strip()
        link=result.a.get("href")
        if 'http' in link:
            link=link
        else:
            link= base_url+link
        news_articles.append((name,headline,link))   
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# jecrcu

try:
    name ='jecrcu'
    url = "https://jecrcuniversity.edu.in/announcement"
    base_url="https://jecrcuniversity.edu.in/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find_all("h3")
    for result in results[:9]:
        headline=result.text.strip()
        link=result.a.get("href")
        news_articles.append((name,headline,link))   
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# pgdav

try:
    name ='pgdav'
    url = "http://pgdavcollege.edu.in/MenuList.aspx?MenuId=News_2324"
    base_url="http://pgdavcollege.edu.in/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("div", class_="col-sm-3").find_all("a")
    for result in results[:9]:
        headline=result.text.strip()
        link=base_url+result.get("href")
        news_articles.append((name,headline,link))   
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# Shyam lal college

try:
    name ='Shyam lal college'
    url = "http://www.slc.du.ac.in/"
    base_url="http://www.slc.du.ac.in/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("marquee", class_="new_maquee").find_all("div" , class_="headline")
    for result in results[:9]:
        headline=result.a.text.strip()
        link=result.a.get("href")
        if "http" in link:
            link=link
        else:
            link=base_url+link
        news_articles.append((name,headline,link))   
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# fddi india

try:
    name ='fddi india'
    url = "https://www.fddiindia.com/importants-updates.php"
    base_url="https://www.fddiindia.com/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("div" , class_="students-affairs-ul").find_all("li")
    for result in results:
        headline=result.a.text.strip()
        link=result.a.get("href")
        if "http" in link:
            link=link
        else:
            link=base_url+link
        news_articles.append((name,headline,link))   
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass


# jesus and mary
try:
    name ='jesus and mary'
    url = "https://www.jmc.ac.in/"
    base_url="https://www.jmc.ac.in/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("ul", style="text-align: center;").find_all("a")
    for result in results:
        headline=result.text.strip()
        link=result.get("href").replace(" ","%20")
        news_articles.append((name,headline,link))   
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# skuast kashmir
try:
    url = 'https://skuastkashmir.ac.in/DisplayAllNews.aspx?id=9'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    results = soup.find_all('div', class_ = 'event-ite w-dyn-item')
    for result in results:
        headline = result.find('a').text
        link = result.find('a').get('href')
        news_articles.append(('skuast kashmir',headline,link))
    success.append('skuast kashmir')
except Exception as e:
    failure.append(('skuast kashmir',e))
    pass


# NIEPMD

try:
    name ='NIEPMD'
    url = "https://www.niepmd.tn.nic.in/admission17.php"
    base_url="https://www.niepmd.tn.nic.in/"
    res = requests.get(url, verify=False)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("div", class_="mainContent").find_all("li")[2:]
    for result in results:
        headline=result.a.text.strip()
        link=base_url+result.a.get("href")
        news_articles.append((name,headline,link))   
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# bankura college

try:
    name ='bankura college'
    url = "http://www.bankurachristiancollege.in/notice.aspx"
    base_url="http://www.bankurachristiancollege.in/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("marquee").find_all("a")
    for result in results:
        headline=result.text.strip()
        link=base_url+result.get("href")
        news_articles.append((name,headline,link))   
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass


# cvs

try:
    name ='cvs'
    url = "https://www.cvs.edu.in/view-all-details.php"
    base_url="https://www.cvs.edu.in/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("div", class_="about-menu").find_all("li")
    for result in results[:9]:
        headline=result.a.text.strip()
        link=result.a.get("href")
        if "http" in link:
            link=link
        else:
            link=base_url+link
        news_articles.append((name,headline,link))   
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# kalyani mahavidyalay

try:
    name ='kalyani mahavidyalay'
    url = "http://kalyanimahavidyalaya.co.in/notice.aspx"
    base_url="http://kalyanimahavidyalaya.co.in/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find_all("div", class_="box")
    for result in results[:9]:
        headline=result.text.strip()
        link=base_url+result.a.get("href").replace(" ","%20")
        news_articles.append((name,headline,link))   
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass


# patna college

try:
    name ='patna college'
    url = "http://www.patnacollege.org/"
    base_url="http://www.patnacollege.org/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("marquee", direction="up").find_all("a")
    for result in results[:9]:
        headline=result.text.strip()
        link=base_url+result.get("href")
        news_articles.append((name,headline,link))   
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# vips

try:
    name ='vips'
    url = "https://vips.edu/admission-information/"
    base_url="https://vips.edu/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find_all("p")
    for result in results[:19]:
        headline=result.text.strip()
        link=result.a.get("href")
        news_articles.append((name,headline,link))   
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# sri sri univ
try:
    name ='sri sri univ'
    url = "https://srisriuniversity.edu.in/"
    base_url="https://srisriuniversity.edu.in/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("div", class_="news-container").find_all("a")
    for result in results[:9]:
        headline=result.text.strip()
        link=result.get("href")
        news_articles.append((name,headline,link))   
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# indian maritime univ
try:
    name ='indian maritime univ'
    url = "https://www.imu.edu.in/"
    base_url="https://www.imu.edu.in/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("div", class_="demof notification").find_all("a")
    for result in results[:9]:
        headline=result.text.strip()
        link=result.get("href")
        if 'http' not in link:
            link=base_url+link
        news_articles.append((name,headline,link))   
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# arsd college
try:
    name ='arsd college'
    url = "https://www.arsdcollege.ac.in/index.php/announcement-2/"
    base_url="https://www.arsdcollege.ac.in/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find_all("tr")[1:11]
    for result in results:
        headline=result.td.text.strip()
        link=result.a.get("href")
        news_articles.append((name,headline,link))   
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass


# iehe
try:
    name ='iehe'
    url = "https://www.iehe.ac.in/Index.aspx?ID=En"
    base_url="https://www.iehe.ac.in/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("table", class_="TBNews").find_all("a")
    for result in results[:9]:
        headline=result.text.replace("\xa0", "").strip()
        link=base_url+result.get("href")
        news_articles.append((name,headline,link))   
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# ram mohan college
try:
    name ='ram mohan college'
    url = "https://www.rammohancollege.ac.in/"
    base_url="https://www.rammohancollege.ac.in/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find_all("div", class_="notice-content")[1].find_all("a")
    for result in results[:9]:
        headline=result.text[11:].strip()
        link =base_url+result.get('href').replace('\n','').replace('\t','').replace(' ','%20')
        news_articles.append((name,headline,link))   
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# NID
try:
    name ='NID'
    url = "https://www.nid.edu/home"
    base_url="https://www.nid.edu/home"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find_all("div", class_="content-slider pb-4")
    for result in results:
        headline=result.h3.text.strip()
        link=result.a.get("href")
        news_articles.append((name,headline,link))   
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass



# usol
try:
    base_url = 'https://usol.puchd.ac.in/'
    url = 'https://usol.puchd.ac.in/show-noticeboard.php?nbid=4'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    results = soup.find_all('tr')
    for result in results:
        headline = result.find('a').text
        link = base_url + result.find('a').get('href')
        news_articles.append(('usol',headline,link))
    success.append('usol')
except Exception as e:
    failure.append(('usol',e))
    pass

# ndri
try:
    url = 'http://ndri.res.in/'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    results = soup.find('div', class_ = 'marquee-announcement').find_all('li')
    for result in results:
        headline = result.find('a').text
        link = result.find('a').get('href')
        news_articles.append(('ndri',headline,link))
    success.append('ndri')
except Exception as e:
    failure.append(('ndri',e))
    pass


# bmcc
try:
    url = 'https://www.bmcc.ac.in/?page_id=2532'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    results = soup.find('div', class_ = 'wpb_wrapper').find_all('p')
    for result in results:
        headline = result.find('a').text
        link = result.find('a').get('href')
        news_articles.append(('bmcc',headline,link))
    success.append('bmcc')
except Exception as e:
    failure.append(('bmcc',e))
    pass

# bkgc
try:
    url = 'https://bkgc.in/site/view_all_notice/1'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    results = soup.find_all('tr')[1:]
    for result in results:
        headline = result.find('td').find_next_sibling('td').text
        link = result.find('a').get('href')
        if link=='#':
            continue
        news_articles.append(('bkgc',headline,link))
    success.append('bkgc')
except Exception as e:
    failure.append(('bkgc',e))
    pass

# st xaviers kolkata
try:
    base_url = 'http://sxuk.edu.in/'
    url = 'https://sxuk.edu.in/admission_notice.php'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    results = soup.find('div', class_ = 'block-news col-md-12 col-sm-12 col-xs-12').find_all('a')
    for result in results:
        headline = result.text
        headline=headline.strip()
        link = result.get('href')
        if 'http' not in link:
            link=base_url+link
        news_articles.append(('st xaviers kolkata',headline,link))
    success.append('st xaviers kolkata')
except Exception as e:
    failure.append(('st xaviers kolkata',e))
    pass

# St Aloysius
try:
    name ='St Aloysius'
    url = "https://staloysiuscollege.ac.in/en-in/page-1/"
    base_url="https://staloysiuscollege.ac.in/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("div", class_="upl-list").find_all("a")
    for result in results[:9]:
        headline=result.text[1:].strip()
        link=result.get("href")
        news_articles.append((name,headline,link))   
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# ILS Law college
try:
    name ='ILS Law college'
    url = "https://ilslaw.edu/announcements/"
    base_url="https://ilslaw.edu/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find_all("h2")
    for result in results[:9]:
        headline=result.a.text.strip()
        link=result.a.get("href")
        news_articles.append((name,headline,link))   
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# IITM Pune
try:
    name ='IITM Pune'
    url = "https://www.tropmet.res.in/latest_view_news.php"
    base_url="https://www.tropmet.res.in/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find_all("tr")[1:11]
    for result in results:
        result=result.find_all("td")[1:2]
        for r in result:

            headline=r.a.text.strip()
            link=base_url+r.a.get("href")
        news_articles.append((name,headline,link))   
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# RIE Mysore
try:
    name ='RIE Mysore'
    url = "http://www.riemysore.ac.in/news"
    base_url="http://www.riemysore.ac.in/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("div", class_="item-list").find_all("li")
    for result in results:
        headline=result.a.text.strip()
        link=base_url+result.a.get("href")
        news_articles.append((name,headline,link))   
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# AKU Bihar
try:
    name ='AKU Bihar'
    url = "http://akubihar.ac.in/Administration/AnnouncementsNotices.aspx"
    base_url="http://akubihar.ac.in/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find_all("a", class_="news_a")
    for result in results[:9]:
        headline=result.text.strip()
        link=result.get("href").replace(" ","%20")
        news_articles.append((name,headline,link))   
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# Kerela Agriculture univ
try:
    name ='Kerela Agriculture univ'
    url = "http://www.kau.in/announcements"
    base_url="http://www.kau.in/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("table",class_="views-table cols-0").find_all("a")
    for result in results[:9]:
        headline=result.text.strip()
        link=base_url+result.get("href")
        news_articles.append((name,headline,link))   
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass


# ddce utkal
try:
    name ="ddce utkal"
    url = "http://ddceutkal.ac.in/"
    base_url="http://ddceutkal.ac.in/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find_all("li", class_="pdf")
    for result in results[:9]:
        headline=result.text.strip()
        link=base_url+result.a.get("href")
        news_articles.append((name,headline,link))   
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# SPM
try:
    name ="SPM"
    url = "http://spm.du.ac.in/index.php?option=com_content&view=article&id=49&Itemid=183&lang=en"
    base_url="http://spm.du.ac.in/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("div", itemprop="articleBody").find_all("li")
    for result in results[:9]:
        headline=result.text.replace("\xa0"," ").strip()
        link=base_url+result.a.get("href")
        news_articles.append((name,headline,link))   
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass


# B Borooah college
try:
    name ="B Borooah college"
    url = "https://www.bborooahcollege.ac.in/allnotice.php"
    base_url="https://www.bborooahcollege.ac.in/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find_all("li", class_="text-primary")
    for result in results[:9]:
        headline=result.text[:-16].replace("\xa0"," ").strip()
        link=base_url+result.a.get("href")
        news_articles.append((name,headline,link))   
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass


# Dr.BR ambedkar college
try:
    name ="Dr.BR ambedkar college"
    url = "https://www.drbrambedkarcollege.ac.in/admission-update-2021-2022"
    base_url="https://www.drbrambedkarcollege.ac.in/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("table", class_="views-table cols-4").find_all("a")
    for result in results[:9]:
        headline=result.text.strip()
        link=result.get("href")
        news_articles.append((name,headline,link))   
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# Gossner college
try:
    name ="Gossner college"
    url = "http://gcran.org/wp/"
    base_url="http://gcran.org/wp/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("marquee").find_all("a")
    for result in results[:9]:
        headline=result.text.strip()
        link=result.get("href")
        news_articles.append((name,headline,link))   
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# st johns college
try:
    name ="st johns college"
    url = "https://stjohnscollegeagra.in/"
    base_url="https://stjohnscollegeagra.in/"
    res = requests.get(url, verify=False)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("div", class_="notices-list").find_all("a")
    for result in results[:9]:
        headline=result.text.strip()
        link=base_url+result.get("href")
        news_articles.append((name,headline,link))   
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# rajguru college
try:
    name ="rajguru college"
    url = "http://www.rajgurucollege.com/Notice.aspx"
    base_url="http://www.rajgurucollege.com/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("ul", class_="list-group text-left").find_all("li")
    for result in results[:9]:
        headline=result.a.text.strip()
        link=base_url+result.a.get("href").replace(" ", "%20")
        news_articles.append((name,headline,link))   
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass


#Telangana University
try:

    source=requests.get('http://www.telanganauniversity.ac.in/').text
    source_url='http://www.telanganauniversity.ac.in/'
    soup=BeautifulSoup(source,'html.parser')
    strong=soup.find_all('strong')
    text=strong[1].a.text

    link=(strong[1].a['href'])


    link=link.lstrip()
    link=link.rstrip()
    text=text.lstrip()
    text=text.rstrip()
    text=" ".join(text.split())
    link=link.replace(' ','%20')
    if 'http' not in link:
        link=source_url+link
    news_articles.append(('Telangana University',text,link))
    success.append('Telangana University')
except Exception as e:
    failure.append(('Telangana University',e))
    pass

#NIT Goa

try:
    source=requests.get('http://www.nitgoa.ac.in/').text
    url='http://www.nitgoa.ac.in/'
    soup=BeautifulSoup(source,'html.parser')
    ul=soup.find('ul',style="height: 350px;")
    li=ul.find_all('li')
    text=li[10].a.text
    link=li[10].a['href']
    link=url+link
    news_articles.append(('NIT Goa',text,link))
    text=li[15].a.text
    link=li[15].a['href']
    link=url+link
    news_articles.append(('NIT Goa',text,link))
    success.append('NIT Goa')
except Exception as e:
    failure.append(('NIT Goa',e))
    pass

print('Successful Scrapers -', success)
print('Failed Scrapers -', failure)
df = pd.DataFrame(news_articles)
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
data = pd.concat([data,df])
print("After append")
print(f"df shape {df.shape}")
print(f"data shape: {data.shape}")
data.drop_duplicates(subset = ['title'], inplace = True)
data.to_csv('/root/New_Scrapers/Cd_scrapers/cd_main.csv', index = False)