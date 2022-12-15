import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
# from dotenv import load_dotenv
from bs4 import BeautifulSoup
from datetime import datetime
from zoneinfo import ZoneInfo
import requests
import os
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import time
from selenium.webdriver.common.by import By

news_articles = []
success = []
failure = []

# load_dotenv()
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




# CAT
try:
    base_url = 'https://iimcat.ac.in/'
    driver.get(base_url)
    time.sleep(2)
    page_source=driver.page_source
    soup = BeautifulSoup(page_source,'html.parser')
    newss = soup.find_all('marquee')
    for news in newss:
        headline = news.get_text()
        if headline == '' or None:
            continue
        news_articles.append(('CAT',headline[:999], 'https://iimcat.ac.in/'))
    success.append('CAT')
except Exception as e:
    failure.append(('CAT', e))
    pass


# GATE
try:                                                    
    base_url = 'http://gate.iitd.ac.in/'
    driver.get(base_url)
    time.sleep(2)
    page_source=driver.page_source
    soup = BeautifulSoup(page_source,'html.parser')
    newss = soup.find_all(class_='impMessage')
    for news in newss:
        headline = news.get_text()
        if headline == '' or None:
            continue
        try:
            link = news.select('a')[0].get('href')
            if link[:4] == 'http':
                pass
            else:
                link = base_url+link
        except:
            link = None
        news_articles.append(('GATE',headline[:999], link))
    success.append('GATE')
except Exception as e:
    failure.append(('GATE', e))
    pass


# IGNOU
try:
    base_url = 'http://www.ignou.ac.in'  
    driver.get(base_url)
    time.sleep(2)
    page_source=driver.page_source
    soup = BeautifulSoup(page_source,'html.parser')
    newss = soup.find(id='alerts').find('ul').find_all('li')
    for news in newss:
        headline = news.get_text().replace('\n', '').strip()
        try:
            link = news.find('a').get('href')
            if link[:4] == 'http':
                pass
            else:
                link = base_url+link
        except:
            link = base_url
        if (headline == '' or None):
            continue
        else:
            news_articles.append(('IGNOU',headline[:999], link))
    success.append('IGNOU-1')
except Exception as e:
    failure.append(('IGNOU-1', e))
    pass
 


# DHE Odisha
try:
    url='https://dhe.odisha.gov.in/latest-news'
    base_url='https://dhe.odisha.gov.in'
    # driver.get(url)
    res = requests.get(url, verify=False)
    soup = BeautifulSoup(res.text, "html.parser")
    # print(soup.prettify())
    results=soup.find('table', class_="cols-3").find('tbody').find_all('tr')
    # print(results)
    for result in results:
        headline = result.find('td', {'class':'views-field views-field-title'}).get_text()
        link = base_url+result.find('td', {'class':'views-field views-field-nothing'}).find('a')['href']
        news_articles.append(('DHE Odisha', headline, link))
    success.append('DHE Odisha')
except Exception as e:
    failure.append(('DHE Odisha',e))
    pass


# MBSE
try:
    url = 'https://www.mbse.edu.in/'
    driver.get(url)
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    results = soup.find('marquee', {'class':'newsmarquee'}).find_all('li')
    for result in results[:15]:
        headline = result.find('a').text[11:].strip()
        link= result.find('a').get('href').strip()
        news_articles.append(('MBSE',headline,link))
    success.append('MBSE')
except Exception as e:
    failure.append(('MBSE',e))
    pass
 


#Alagappa University Directorate of Distance Education(done)
try:
    name="Alagappa University Directorate of Distance Education "
    url="https://alagappauniversity.ac.in/nodificationAll.php"
    base_url="https://alagappauniversity.ac.in/"
    driver.get(url)
    time.sleep(2)
    soup=BeautifulSoup(driver.page_source,"html.parser")
    results=soup.find("div",class_="col-md-10 col-xl-12 notifications").find_all("a")
    for result in results[2:]:
        link=result.get("href")
        headline=result.text.strip()
        if "http" in link:
            link=link
            news_articles.append((name,headline,link))            
        else:
            link=base_url+link
            news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass
 


#Army Institute of Law
 
try:
    name='Army Institute of Law'
    url='https://www.ail.ac.in/'
    driver.get(url)
    time.sleep(2)
    soup=BeautifulSoup(driver.page_source,'html.parser')
    results=soup.find('marquee').find_all('a')
    for result in results:
        headline=result.text.replace('\n','').replace('\xa0','')
        link=url+result.get('href')
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass
 


#Ram Lal A0d College
 
try:
    name='Ram Lal A0d College'
    url='https://rlacollege.edu.in/'
    driver.get(url)
    time.sleep(2)
    soup=BeautifulSoup(driver.page_source,"html.parser")
    results=soup.find_all("marquee")
    for result in results[1:]:
        head=result.find_all("a")
        for re in head[:10]:
            headline=re.text.strip()
            link=url+re.get("href")
    news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

#Krishna Kanta Handiqui State Open University
 
try:
    name="Krishna Kanta Handiqui State Open University"
    base_url="http://www.kkhsou.in/"
    url="http://www.kkhsou.in/web_new/index.php"
    driver.get(url)
    time.sleep(2)
    soup=BeautifulSoup(driver.page_source,"html.parser")
    results=soup.find_all("marquee")
    for result in results[1:2]:
        head=result.find_all("a")
        for re in head:
            headline=re.text
            link=base_url+re.get("href")
            news_articles.append((name,headline,link))
    success.append(name)  
except Exception as e:
    failure.append((name,e))
    pass


#Elphinstone College
 
try:
    name="Elphinstone College"
    url="https://www.elphinstone.ac.in/"
    driver.get(url)
    time.sleep(2)
    soup=BeautifulSoup(driver.page_source,"html.parser")
    results=soup.find("div",class_="tab_content",id='tab1').find_all("a")
    for result in results[:3]:
        headline=result.text.strip()
        link=result.get("href")
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass
 


#Ramjas College
 
try:
    name='Ramjas College'
    url='https://ramjas.du.ac.in/college/web/index.php'
    base_url='https://ramjas.du.ac.in/'
    driver.get(url)
    time.sleep(2)
    soup=BeautifulSoup(driver.page_source,'html.parser')
    results=soup.find(class_='panel-content').find_all('li')
    for result in results:
        headline=result.text.strip()
        link=base_url+result.find('a').get('href')
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass


 
#samsi college
 
try:
    name ='samsi college'
    url = "https://www.samsicollege.ac.in/samsi_college/view-list.php?action=Admission%20Notice"
    
    driver.get(url)
    time.sleep(2)
    soup=BeautifulSoup(driver.page_source, 'html.parser')
    results=soup.find("div",class_="header-info text-left").find_all("a")
    for result in results:
        headline=result.b.text.strip()
        link=result.get("href")
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass
 

#Mulund College of Commerce
 
try:
    name ='Mulund College of Commerce'
    url = "https://mccmulund.ac.in/new1/noticeBoard.php?t=4"
    base_url="https://mccmulund.ac.in/new1/"
    driver.get(url)
    time.sleep(2)
    soup=BeautifulSoup(driver.page_source, 'html.parser')
    results = soup.find_all("div", class_="notice")
    for result in results:
        headline=result.h4.text.strip()
        link=result.a.get("href")
        if "http" in link:
            link=link
            news_articles.append((name,headline,link))
        else:
            link=base_url+link.replace(" ", "%20")
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass


#St John's College
 
try:
    name ="St John's College"
    url = "https://stjohnscollegeagra.in/"
    base_url="https://stjohnscollegeagra.in/"
    driver.get(url)
    time.sleep(2)
    soup=BeautifulSoup(driver.page_source, 'html.parser')
    results = soup.find("div", class_="notices-list").find_all("a")
    for result in results[:9]:
        headline=result.text.strip()
        link=base_url+result.get("href")
        news_articles.append((name,headline,link))  
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass
 

#city college
 
try:
    name='city college'
    url = 'http://www.citycollegekolkata.org/'
    driver.get(url)
    time.sleep(2)
    soup=BeautifulSoup(driver.page_source, 'html.parser')
    results = soup.find('sectionn', class_ = 'tab-content').find_all('tr')
    for result in results[:10]:
        headline = result.find('a').text.strip()
        link = url + result.find('a').get('href')
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

#Jawaharlal Nehru Centre for Advanced Scientific Research
 
 
 
try:
    name="Jawaharlal Nehru Centre for Advanced Scientific Research"
    url="https://www.jncasr.ac.in/"
    driver.get(url)
    time.sleep(2)
    soup=BeautifulSoup(driver.page_source,"html.parser")
    results=soup.find_all("div",class_="media-body pl-2")
    for result in results:
        headline=result.a.text.strip()
        link=url+result.a.get("href")
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass
try:
    name ='PAU'
    url = "https://pau.edu/"
    base_url="https://pau.edu/"
    driver.get(url)
    time.sleep(2)
    soup=BeautifulSoup(driver.page_source, 'html.parser')
    results = soup.find_all("tr", style="background-color: #f7f7f7; border-bottom: 1px dashed #c0c0c0")
    for result in results:
        headline=result.a.text.strip()
        link=result.a.get("href")
        news_articles.append((name,headline,link))   
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# bhaskacharya

#headline and link variable not properly defined
try:
    name ='bhaskacharya'
    url = "https://bcas.du.ac.in/news-notices/"
    base_url="https://bcas.du.ac.in/"
    driver.get(url)
    time.sleep(2)
    soup=BeautifulSoup(driver.page_source, 'html.parser')
    results = soup.find_all("tr")[1:11]
    for result in results:
        result=result.find_all("td")[1:2]
        for r in result:
            headline=r.text.strip()
            link=r.a.get("href")
        news_articles.append((name,headline,link))   
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass


# chanchal college
try:
    name ='chanchal college'
    url = "http://chanchalcollege.ac.in/admission/"
    base_url="http://chanchalcollege.ac.in/"
    driver.get(url)
    time.sleep(2)
    soup=BeautifulSoup(driver.page_source, 'html.parser')
    results = soup.find_all("p", class_="sgjvs_widget_title")
    for result in results:
        headline=result.a.text.strip()
        link=result.a.get("href")
        news_articles.append((name,headline,link))   
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass


# Gobardanga
try:
    name ='Gobardanga'
    url = "http://www.ghcollege.ac.in/"
    base_url="http://www.ghcollege.ac.in/"
    driver.get(url)
    time.sleep(2)
    soup=BeautifulSoup(driver.page_source, 'html.parser')
    results = soup.find_all("div", class_="notice-area")[1:]
    for result in results:
        result=result.find_all("a")[1:11]
        for r in result:
            headline=r.text[:-10].replace("\n","").strip()
            link=base_url+r.get("href").replace('\n','').replace('\t','').replace(' ','%20')
            news_articles.append((name,headline,link))   
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass






# Chakdaha college

try:
    name ='Chakdaha college'
    url = "https://chakdahacollege.ac.in/"
    base_url="https://chakdahacollege.ac.in/"
    driver.get(url)
    time.sleep(2)
    soup=BeautifulSoup(driver.page_source, 'html.parser')
    results = soup.find_all("li", class_="news-item")
    for result in results:
        headline=result.tr.text[18:].replace("Read More","").strip()
        link=base_url+result.a.get("href")
        news_articles.append((name,headline,link))   
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# mody univ

try:
    name ='mody univ'
    url = "https://www.modyuniversity.ac.in/"
    base_url="https://www.modyuniversity.ac.in/"
    driver.get(url)
    time.sleep(2)
    soup=BeautifulSoup(driver.page_source, 'html.parser')
    results = soup.find("ul", class_="list list-icons list-icons-style-2").find_all("a")
    for result in results:
        headline=result.text.strip()
        link=result.get("href")
        news_articles.append((name,headline,link))   
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# LAdy irwin
try:
    name ='LAdy irwin'
    url = "https://ladyirwin.edu.in/"
    base_url="https://ladyirwin.edu.in/"
    driver.get(url)
    time.sleep(2)
    soup=BeautifulSoup(driver.page_source, 'html.parser')
    results = soup.find_all("p", class_="ne")
    for result in results[:9]:
        headline=result.a.text.strip()
        link=result.a.get("href")
        news_articles.append((name,headline,link))   
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass


# Panskura banamali

try:
    name ='Panskura banamali'
    url = "https://panskurabanamalicollege.org/"
    base_url="https://panskurabanamalicollege.org/"
    driver.get(url)
    time.sleep(2)
    soup=BeautifulSoup(driver.page_source, 'html.parser')
    results = soup.find("marquee").find_all("a")
    for result in results[:9]:
        headline=result.text.replace("||","").strip()
        link=result.get("href").replace(" ", "%20")
        if "http" in link:
            link=link
        else:
            link=base_url+link
        news_articles.append((name,headline,link))   
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass


# lakshmibai college
#too much trust
try:
    

    url='https://lakshmibaicollege.in/index.php/home/allnews'
    driver.get(url)
    time.sleep(2)
    soup=BeautifulSoup(driver.page_source, 'html.parser')
    results = soup.find('div', id = 'alice1').find_all('tr')[1:]
    for result in results:
        headline = result.find('td').find_next_sibling('td').text
        link = result.find('a').get('href')
        news_articles.append(('lakshmibai college',headline,link))
    success.append('lakshmibai college')
except Exception as e:
    failure.append(('lakshmibai college',e))
    pass




# shaheed bhagat singh college

try:
    name ='shaheed bhagat singh college'
    url = "https://www.sbsc.in/view-all.php"
    base_url="https://www.sbsc.in/"
    driver.get(url)
    time.sleep(2)
    soup=BeautifulSoup(driver.page_source, 'html.parser')
    results = soup.find("div", class_="col-lg-12").find_all("a")
    for result in results[:9]:
        headline=result.text.strip()
        link=base_url+result.get("href")
        news_articles.append((name,headline,link))   
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# jai hind college

try:
    name ='jai hind college'
    url = "https://www.jaihindcollege.com/"
    base_url="https://www.jaihindcollege.com/"
    driver.get(url)
    time.sleep(2)
    soup=BeautifulSoup(driver.page_source, 'html.parser')
    results = soup.find("ul", id="tweets").find_all("a")
    for result in results[:9]:
        headline=result.text.strip()
        link=base_url+result.get("href")
        news_articles.append((name,headline,link))   
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# deshbandhu college
try:
    name ='deshbandhu college'
    url = "https://www.deshbandhucollege.ac.in/"
    base_url="https://www.deshbandhucollege.ac.in/"
    driver.get(url)
    time.sleep(2)
    soup=BeautifulSoup(driver.page_source, 'html.parser')
    results = soup.find_all("marquee", class_="new_maquee")[1].find_all("a")
    for result in results:
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


# tndalu

try:
    name ='tndalu'
    url = "https://www.tndalu.ac.in/notifications.html"
    base_url="https://www.tndalu.ac.in/"
    driver.get(url)
    time.sleep(2)
    soup=BeautifulSoup(driver.page_source, 'html.parser')
    results = soup.find("div", class_="col-lg-12").find_all("a")
    for result in results[:9]:
        headline=result.b.text.strip()
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

# guru nanak college

try:
    name ='guru nanak college'
    url = "https://gurunanakcollege.edu.in/"
    base_url="https://gurunanakcollege.edu.in/"
    driver.get(url)
    time.sleep(2)
    soup=BeautifulSoup(driver.page_source, 'html.parser')
    results = soup.find("marquee", direction="left").find_all("a")
    for result in results:
        headline=result.text.replace("|", "").strip()
        link=result.get("href")
        news_articles.append((name,headline,link))   
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# integral univ

try:
    name ='integral univ'
    url = "https://iul.ac.in/noticeboard.aspx?ActivePanel=Admission"
    base_url="https://iul.ac.in/"
    driver.get(url)
    time.sleep(2)
    soup=BeautifulSoup(driver.page_source, 'html.parser')
    results = soup.find_all("ul", class_="ul-icons")[2:]
    for result in results:
        result=result.find_all("a")
        for r in result:
            headline=r.text.strip()
            link=r.get("href").replace(" ", "%20")
            news_articles.append((name,headline,link))   
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# maitreyi

try:
    name ='maitreyi'
    url = "http://maitreyi.ac.in/AllNewsDetails.aspx"
    base_url="http://maitreyi.ac.in/"
    driver.get(url)
    time.sleep(2)
    soup=BeautifulSoup(driver.page_source, 'html.parser')
    results = soup.find_all("li", style="list-style: none; font-family:Calibri; font-size:12px;")
    for result in results[:9]:
        headline=result.find("p").text.strip()
        link=base_url+result.a.get("href").replace(" ","%20")
        news_articles.append((name,headline,link))   
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# sunrise university
try:
    name ='sunrise university'
    url = "https://www.sunriseuniversity.in/notification"
    base_url="https://www.sunriseuniversity.in/"
    driver.get(url)
    time.sleep(2)
    soup=BeautifulSoup(driver.page_source, 'html.parser')
    results=soup.find("div", class_="news-listing").find_all("a")
    for result in results:
        headline=result.text.replace("...", "").strip()
        link=result.get("href")
        news_articles.append((name,headline,link))   
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# iacs
#review
try:
    name ='iacs'
    url = "http://iacs.res.in/news-update-archieve.html"
    base_url="http://iacs.res.in/"
    driver.get(url)
    time.sleep(2)
    soup=BeautifulSoup(driver.page_source, 'html.parser')
    results = soup.find_all("tr")[1:11]
    
    for result in results:
        link=result.a.get('href').replace(" ", "%20")
        if "http" in link:
            link=link
        else:
            link=base_url+link
        result=result.find_all("td")
        for r in result[1:2]:
            headline = r.text
            link=link
        news_articles.append((name,headline,link))   
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# nsd

try:
    name ='nsd'
    url = "https://nsd.gov.in/delhi/index.php/news-updates/"
    base_url="https://nsd.gov.in/delhi/"
    driver.get(url)
    time.sleep(2)
    soup=BeautifulSoup(driver.page_source, 'html.parser')
    results = soup.find_all("h1")
    for result in results:
        headline=result.text.strip()
        link=result.a.get("href")
        news_articles.append((name,headline,link))   
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass


# fridu
try:
    name ='fridu'
    url = "http://fridu.edu.in/"
    base_url="http://fridu.edu.in/"
    driver.get(url)
    time.sleep(2)
    soup=BeautifulSoup(driver.page_source, 'html.parser')
    results = soup.find("div", class_="notices").find_all("a")
    for result in results[:9]:
        headline=result.text.strip()
        link=result.get("href")
        news_articles.append((name,headline,link))   
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# Manipal University
try:
    name ='Manipal university'
    url = "https://manipal.edu/mu/news-events.html?q=manipal:news"
    base_url="https://manipal.edu"
    driver.get(url)
    time.sleep(2)
    soup=BeautifulSoup(driver.page_source, 'html.parser')
    results = soup.find("div", class_="grid clearfix")
    for result in results:
        headline=result.h3.text.strip()
        link=base_url+result.get("href")
        news_articles.append((name,headline,link))   
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass


# Uttrakhand open university
try:
    name ='uttrakhand open univ '
    url = "https://uou.ac.in/announcement"
    base_url="https://uou.ac.in/"
    driver.get(url)
    time.sleep(2)
    soup=BeautifulSoup(driver.page_source, 'html.parser')
    results = soup.find("div",id="content").find_all('li',class_="view-list-item")
    for result in results[:9]:
        headline=result.a.text.strip()
        link=base_url+result.a.get("href")
        news_articles.append((name,headline,link))   
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# BAOU
try:
    name="baou"
    url = "https://baou.edu.in/news-announcements"
    base_url = 'https://baou.edu.in/'
    driver.get(url)
    time.sleep(2)
    soup=BeautifulSoup(driver.page_source, 'html.parser')
    results = soup.find_all("tr", class_="qupaper")
    for result in results[:9]:
        headline=result.a.text.strip()
        link=url+result.a.get("href")
        news_articles.append((name,headline,link))
    success.append((name))
except Exception as e:
    failure.append((name,e))
    pass

# samsi college
try:
    name ='samsi college'
    url = "https://www.samsicollege.ac.in/samsi_college/view-list.php?action=Admission%20Notice"
    base_url="https://www.samsicollege.ac.in/samsi_college/"
    driver.get(url)
    time.sleep(2)
    soup=BeautifulSoup(driver.page_source, 'html.parser')
    results = soup.find_all("tr")[1:11]
    for result in results:
        link=base_url+result.a.get("href").replace(" ", "%20")
        result=result.find_all("td")[3:4]
        for r in result:
            headline=r.text.strip()
        news_articles.append((name,headline,link))   
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# marian college
try:
    name ="marian college"
    url = "https://www.mariancollege.org/admissionNotifications.php"
    base_url="https://www.mariancollege.org/"
    driver.get(url)
    time.sleep(2)
    soup=BeautifulSoup(driver.page_source, 'html.parser')
    results = soup.find("div", class_="ui-tabs-panel clearfix ui-widget-content ui-corner-bottom", id="panel-1").find_all("a")
    for result in results:
        headline=result.text.strip()
        link=base_url+result.get("href").replace(" ", "%20")
        news_articles.append((name,headline,link))   
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass


#Alagappa University Directorate of Distance Education(done)


try:
    name="Alagappa University Directorate of Distance Education "
    url="https://alagappauniversity.ac.in/nodificationAll.php"
    base_url="https://alagappauniversity.ac.in/"
    driver.get(url)
    time.sleep(2)
    soup=BeautifulSoup(driver.page_source,"html.parser")
    results=soup.find("div",class_="col-md-10 col-xl-12 notifications").find_all("a")
    for result in results[2:]:
        link=result.get("href")
        headline=result.text.strip()
        if "http" in link:
            link=link
            news_articles.append((name,headline,link))             
        else:
          link=base_url+link
          news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

#Army Institute of Law

try:
    name='Army Institute of Law'
    url='https://www.ail.ac.in/'
    driver.get(url)
    time.sleep(2)
    soup=BeautifulSoup(driver.page_source,'html.parser')
    results=soup.find('marquee').find_all('a')
    for result in results:
        headline=result.text.replace('\n','').replace('\xa0','')
        link=url+result.get('href')
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass
#Ram Lal A0d College


try:
  name='Ram Lal A0d College'
  url='https://rlacollege.edu.in/'
  driver.get(url)
  time.sleep(2)
  soup=BeautifulSoup(driver.page_source,"html.parser")
  results=soup.find_all("marquee")
  for result in results[1:]:
      head=result.find_all("a")
      for re in head[:10]:
          headline=re.text.strip()
          link=url+re.get("href")
          news_articles.append((name,headline,link))
  success.append(name)
except Exception as e:
    failure.append((name,e))
    pass
#Krishna Kanta Handiqui State Open University


try:
   name="Krishna Kanta Handiqui State Open University"
   base_url="http://www.kkhsou.in/"
   url="http://www.kkhsou.in/web_new/index.php"
   driver.get(url)
   time.sleep(2)
   soup=BeautifulSoup(driver.page_source,"html.parser")
   results=soup.find_all("marquee")
   for result in results[1:2]:
       head=result.find_all("a")
       for re in head:
           headline=re.text
           link=base_url+re.get("href")
           news_articles.append((name,headline,link))
   success.append(name)   
except Exception as e:
    failure.append((name,e))
    pass
#Elphinstone College

try:
    name="Elphinstone College"
    url="https://www.elphinstone.ac.in/"
    driver.get(url)
    time.sleep(2)
    soup=BeautifulSoup(driver.page_source,"html.parser")
    results=soup.find("div",class_="tab_content",id='tab1').find_all("a")
    for result in results[:3]:
        headline=result.text.strip()
        link=result.get("href")
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass



#Ramjas College

try:
    name='Ramjas College'
    url='https://ramjas.du.ac.in/college/web/index.php'
    base_url='https://ramjas.du.ac.in/'
    driver.get(url)
    time.sleep(2)
    soup=BeautifulSoup(driver.page_source,'html.parser')
    results=soup.find(class_='panel-content').find_all('li')
    for result in results:
        headline=result.text.strip()
        link=base_url+result.find('a').get('href')
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass


#samsi college

try:
    name ='samsi college'
    url = "https://www.samsicollege.ac.in/samsi_college/view-list.php?action=Admission%20Notice"
    driver.get(url)
    time.sleep(2)
    soup=BeautifulSoup(driver.page_source, 'html.parser')
    results=soup.find("div",class_="header-info text-left").find_all("a")
    for result in results:
        headline=result.b.text.strip()
        link=result.get("href")
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass



#Mulund College of Commerce

try:
    name ='Mulund College of Commerce'
    url = "https://mccmulund.ac.in/new1/noticeBoard.php?t=4"
    base_url="https://mccmulund.ac.in/new1/"
    driver.get(url)
    time.sleep(2)
    soup=BeautifulSoup(driver.page_source, 'html.parser')
    results = soup.find_all("div", class_="notice")
    for result in results:
        headline=result.h4.text.strip()
        link=result.a.get("href")
        if "http" in link:
            link=link
            news_articles.append((name,headline,link)) 
        else:
            link=base_url+link.replace(" ", "%20")
        news_articles.append((name,headline,link)) 
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass



#city college


try:
    name='city college'
    url = 'http://www.citycollegekolkata.org/'
    driver.get(url)
    time.sleep(2)
    soup=BeautifulSoup(driver.page_source, 'html.parser')
    results = soup.find('sectionn', class_ = 'tab-content').find_all('tr')
    for result in results[:10]:
        headline = result.find('a').text.strip()
        link = url + result.find('a').get('href')
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

#Jawaharlal Nehru Centre for Advanced Scientific Research



try:
   name="Jawaharlal Nehru Centre for Advanced Scientific Research"
   url="https://www.jncasr.ac.in/"
   driver.get(url)
   time.sleep(2)
   soup=BeautifulSoup(driver.page_source,"html.parser")
   results=soup.find_all("div",class_="media-body pl-2")
   for result in results:
       headline=result.a.text.strip()
       link=url+result.a.get("href")
       news_articles.append((name,headline,link))
   success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

#Lady Irwin College


try:
    name ='Lady Irwin College'
    url = "https://ladyirwin.edu.in/notices/"
    driver.get(url)
    time.sleep(2)
    soup=BeautifulSoup(driver.page_source, 'html.parser')
    results = soup.find_all(class_="LIC-news-holder")
    for result in results[1:2]:
        re=result.find_all('li')
        for r in re:
            he=r.find('span').text
            headline=r.a.text.strip().replace(he,' ')
            link=result.a.get("href")
            news_articles.append((name,headline,link))   
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass


#Mody University

try:
    name ='Mody University'
    url = "https://www.modyuniversity.ac.in/"
    driver.get(url)
    time.sleep(2)
    soup=BeautifulSoup(driver.page_source, 'html.parser')
    results = soup.find("ul", class_="list list-icons list-icons-style-2").find_all("a")
    for result in results:
        headline=result.text.strip()
        link=result.get("href")
        news_articles.append((name,headline,link))   
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

#Chakdaha College


try:
    name ='Chakdaha college'
    url = "https://chakdahacollege.ac.in/"
    base_url="https://chakdahacollege.ac.in/"
    driver.get(url)
    time.sleep(2)
    soup=BeautifulSoup(driver.page_source, 'html.parser')
    results = soup.find_all("li", class_="news-item")
    for result in results:
        headline=result.tr.text[18:].replace("Read More","").strip()
        link=url+result.a.get("href")
        news_articles.append((name,headline,link))   
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass


#Delhi Institute of Advanced Studies

try:
   name ='Delhi Institute of Advanced Studies'
   url = "https://dias.ac.in/"
   driver.get(url)
   time.sleep(2)
   soup=BeautifulSoup(driver.page_source, 'html.parser')
   
   results = soup.find("div", class_="whatsnewPost").find_all('a')
   results_1=soup.find_all("div", class_="whatsnewPost")
   for result in results[1:]:
       headline=result.text.strip()
       link=result.get('href')
       news_articles.append((name,headline,link))
   for result_1 in results_1[1:10]:
       headline=result_1.a.text.strip()
       link=result_1.a.get("href")
       news_articles.append((name,headline,link))  
   success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

#Shaheed Bhagat Singh College 

try:
    name ='Shaheed Bhagat Singh College'
    url = "https://www.sbsc.in/view-all.php"
    base_url="https://www.sbsc.in/"
    driver.get(url)
    time.sleep(2)
    soup=BeautifulSoup(driver.page_source, 'html.parser')
    results = soup.find("div", class_="col-lg-12").find_all("a")
    for result in results[:10]:
        headline=result.text.strip()
        link=base_url+result.get("href")
        news_articles.append((name,headline,link))   
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

#Maitreyi College


try:
    name ='Maitreyi College'
    url = "http://maitreyi.ac.in/AllNewsDetails.aspx"
    base_url="http://maitreyi.ac.in/"
    driver.get(url)
    time.sleep(2)
    soup=BeautifulSoup(driver.page_source, 'html.parser')
    results = soup.find_all("li", style="list-style: none; font-family:Calibri; font-size:12px;")
    for result in results[:10]:
        headline=result.find("p").text.strip()
        link=base_url+result.a.get("href").replace(" ","%20")
        news_articles.append((name,headline,link))   
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

#SkillOutlook
try:
    name ='Skill Outlook'
    url = "https://skilloutlook.com/admission-alert"
    #base_url="http://maitreyi.ac.in/"
    driver.get(url)
    time.sleep(2)
    soup=BeautifulSoup(driver.page_source, 'html.parser').find_all("h2",class_="posttitle")
    #results = soup.find_all("li", style="list-style: none; font-family:Calibri; font-size:12px;")
    for result in soup:
        headline=result.text.strip()
        link=result.a.get("href")
        news_articles.append((name,headline,link))   
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass



#Jai Hind College


try:
    name ='Jai Hind College'
    url = "https://www.jaihindcollege.com/"
    driver.get(url)
    time.sleep(2)
    soup=BeautifulSoup(driver.page_source, 'html.parser')
    results = soup.find("ul", id="tweets").find_all("a")
    for result in results[:10]:
        headline=result.text.strip()
        link=url+result.get("href")
        news_articles.append((name,headline,link))   
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass


#Deshbandhu College
name ='Deshbandhu College'
try:
    
    url = "https://www.deshbandhucollege.ac.in/"
    driver.get(url)
    time.sleep(2)
    soup=BeautifulSoup(driver.page_source, 'html.parser')
    results = soup.find_all("marquee", class_="new_maquee")[1].find_all("a")
    for result in results:
        headline=result.text.strip()
        link=result.get("href")
        if "http" in link:
            link=link
        else:
            link=url+link
        news_articles.append((name,headline,link))   
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

#Medical dialogues

try:
    base_url = 'https://medicaldialogues.in'
    url = 'https://medicaldialogues.in/news/education'
    name = 'Medical Dialogues'
    driver.get(url)
    time.sleep(5)
    headlines_len = len(driver.find_element(By.CLASS_NAME,'col-sm-8').find_elements(By.TAG_NAME,'p'))
    for i in range(headlines_len):
        headline = driver.find_element(By.CLASS_NAME,'col-sm-8').find_elements(By.TAG_NAME,'p')[i].text.strip()
        link = driver.find_element(By.CLASS_NAME,'col-sm-8').find_elements(By.TAG_NAME,'p')[i].find_element(By.TAG_NAME,'a').get_attribute('href')
        news_articles.append(("Medical Dialogues",headline,link))
    success.append("Medical Dialogues")

except Exception as e:
    failure.append(("Medical Dialogues",e))
    pass

#Shiksha

try:
    url = 'https://www.shiksha.com/articles-all'
    base_url = 'https://www.shiksha.com'
    
    driver.get(url)
    soup = BeautifulSoup(driver.page_source,'html.parser')
    headlines = soup.find(class_='articleList').find_all(class_='contentBox')
    for line in headlines:
        if line.find('a').text.strip().startswith('LIVE'):
            headline = line.find('a').text.strip()[4:]
        else:
            headline = line.find('a').text.strip()
        link = line.find('a')['href']
        if not link.startswith('https'):
            link = base_url + link
        news_articles.append(('Shiksha',headline,link))
    success.append('Shiksha')
except Exception as e:
    failure.append(('Shiksha',e))

driver.quit()

print('Successful Scrapers -', success)
print('Failed Scrapers -', failure)
df = pd.DataFrame(news_articles)
df.drop_duplicates(inplace = True) 
df['date'] = now.strftime("%Y-%m-%d %H:%M")
df.columns = ['source','title','link','date']

# df.to_csv('/root/New_Scrapers/Cd_scrapers/cd_newscraper_try.csv', index = False)


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
print('lol')
