from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from datetime import datetime
# from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import pandas as pd
#import pymysql
import os
import re
import csv
mainscraper = []
success = []
failure = []
options=Options()
options.headless=True

# load_dotenv()
from zoneinfo import ZoneInfo
now = datetime.now(tz=ZoneInfo('Asia/Kolkata'))
print (now.strftime("%Y-%m-%d %H:%M:%S"))

# Driver Initiated
# driver = webdriver.Firefox(options=options)

# Selenium Scrapers Started

# NTA
try:
    base_url = 'https://nta.ac.in/NoticeBoardArchive'
    res = requests.get(base_url)
    soup = BeautifulSoup(res.text, 'html.parser')
    newss = soup.find("table",{"id":'tbl'}).find_all('tr')
    for news in newss[1:]:
        if news.find('content') is None :
            headline = news.find('a').text
            link = news.find('a').get('href')
        else:
            headline = news.find('content').text
            link = base_url + news.find('a').get('href')
    
        mainscraper.append(('NTA',headline, link))
    success.append('NTA')
except Exception as e:
    failure.append(('NTA', e))
    pass


# CMAT
try:
    base_url = 'https://cmat.nta.nic.in/'
    res = requests.get(base_url)
    soup = BeautifulSoup(res.text,'html.parser')
    newss = soup.find('div',class_='vc_tta-panel-body').find_all('a')
    for news in newss:
        headline = news.text
        link = news.get('href')
        if headline == '' or None:
            continue
        mainscraper.append(('CMAT', headline[:999], link))
    success.append('CMAT')
except Exception as e:
    failure.append(('CMAT', e))
    pass
# CSIRNET
try: 
    base_url = 'https://csirnet.nta.nic.in/WebInfo/Page/Page?PageId=1&LangId=P'
    res = requests.get(base_url)
    soup = BeautifulSoup(res.text, 'html.parser')
    newss = soup.find(class_='list-unstyled components').find_all('a')
    for news in newss:
        headline = news.text
        link = news.get('href')

    mainscraper.append(('CSIRNET', headline[:999], link))
    success.append('CSIRNET')
except Exception as e:
    failure.append(('CSIRNET', e))
    pass


# GPAT
try:
    base_url = 'https://gpat.nta.nic.in/'
    res = requests.get(base_url)
    soup = BeautifulSoup(res.text,'html.parser')
    newss = soup.find('div',class_='vc_tta-panel-body').find_all('a')
    for news in newss:
        headline = news.text
        link = news.get('href')
        if headline == '' or None:
            continue
    mainscraper.append(('GPAT', headline[:999], link))
    success.append('GPAT')
except Exception as e:
    failure.append(('GPAT', e))
    pass
#OJEE
try:
    base_url = 'https://ojee.nic.in/ojeecms/Page/Page?PageId=1&LangId=P'   
    res = requests.get(base_url)
    soup = BeautifulSoup(res.text,'html.parser')
    newss = soup.find('div',class_='boxdesignNews').find_all('li')
    for news in newss:
        box = news.find('a')
        headline = box.get_text()
        link = box.get('href')
        if headline == '' or None:
            continue
        mainscraper.append(('OJEE',headline[:999], link))
    success.append('OJEE')
except Exception as e:
    failure.append(('OJEE', e))
    pass

# BITS
try:                                                                    
    base_url = 'https://www.bitsadmission.com/'
    res = requests.get(base_url)
    soup = BeautifulSoup(res.text, 'html.parser')
    newss = soup.find_all(class_='mtext')
    for news in newss:
        headline = news.get_text().strip().replace('\n', '').replace('\r', '')
        if headline == '' or None:
            continue
        mainscraper.append(('BITS', headline[:999], 'https://www.bitsadmission.com/'))
    success.append('BITS')
except Exception as e:
    failure.append(('BITS', e))
    pass

# MAT
try:
    base_url = 'https://mat.aima.in/'
    res = requests.get(base_url)
    soup = BeautifulSoup(res.text, 'html.parser')
    newss = soup.select('.announcement')
    for news in newss:
        headline = ' '.join(news.get_text().strip().split())
        if headline == '' or None:
            continue
        mainscraper.append(('MAT',headline[:999], base_url))
    success.append('MAT')
except Exception as e:
    failure.append(('MAT', e))
    pass     

# NLU
try:
    base_url = 'https://nludelhi.ac.in/'
    res = requests.get(base_url)
    soup = BeautifulSoup(res.text, 'html.parser')
    newss = soup.find_all('li')
    for news in newss:
        try:
            if news.get('style') == 'display:none':
                continue
            elif news.select('span')[0].get('id')[:28] == 'homebox_rptannouncment_Label':
                headline = news.get_text().strip()
                link = news.select('a')[0].get('href')
                link = base_url+link
                mainscraper.append(('NLU',headline[:999], link))
        except:
            continue
    success.append('NLU')
        
except:
    failure.append(('NLU', e))
    pass

# XAT
try:
    base_url = 'http://www.xatonline.in/'
    res = requests.get(base_url)
    soup = BeautifulSoup(res.text, 'html.parser')
    newss = soup.find_all('marquee')
    for news in newss:
        headline = news.get_text()
        if headline == '' or None:
            continue
        mainscraper.append(('XAT', headline[:999], base_url))
    success.append('XAT')
except Exception as e:
    failure.append(('XAT', e))
    pass

# HPBOSE
try:
    base_url = 'https://www.hpbose.org'
    res = requests.get(base_url)
    soup = BeautifulSoup(res.text, 'html.parser') 
    newss = soup.find(id='ctl00_ContentPlaceHolder1_DataList1').find_all('tr')
    for news in newss:
        headline = news.get_text().strip()
        if headline == '' or None:
            continue
        mainscraper.append(('HPBOSE',headline[:999], base_url))
    success.append('HPBOSE')
except Exception as e:
    failure.append(('HPBOSE', e))
    pass




# BSEH
try:
    base = "https://bseh.org.in/"
    url = "https://bseh.org.in/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("ul", class_ = "news-home")
    for result in results.find_all("li"):
        headline = result.text.strip()
        link= result.find("a")["href"].strip()
        mainscraper.append(('BSEH',headline,link))
    success.append('BSEH')
except Exception as e:
    failure.append(('BSEH',e))
    pass


# KSEEB
try:
    url = 'https://sslc.karnataka.gov.in/english'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    results = soup.find('marquee').find_all('p')
    for result in results:
        headline = result.get_text()
        link = result.find('a')['href'].strip()
        if 'http' in link:
            mainscraper.append(('KSEEB',headline,link))
    success.append('KSEEB')
except Exception as e:
    failure.append(('KSEEB',e))
    pass



# MBOSE
try:
    base_url = "http://www.mbose.in/"
    url = "http://www.mbose.in/more.php?category=archive_notification"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("div", class_ = "container").find_all("li")
    for result in results:
        headline = result.find("a").text.strip()
        link= base_url+result.find("a").get("href").strip()
        mainscraper.append(('MBOSE',headline,link))
    success.append('MBOSE')
except Exception as e:
    failure.append(('MBOSE',e))
    pass

# GBSHSE
try:
    url = "https://www.gbshse.info/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("div", class_ ="gdlr-core-tab-item-content-wrap clearfix").find_all("li")
    for result in results:
        headline = result.find("a").text
        link= result.find("a").get("href").strip()
        mainscraper.append(('GBSHSE',headline,link))
    success.append('GBSHSE')
except Exception as e:
    failure.append(('GBSHSE',e))
    pass

# TBSE
try:
    url = 'https://tbse.tripura.gov.in/'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    results = soup.find('ul', id ='whats-new').find_all('li')
    for result in results:
        headline = result.find('a').text.strip()
        link= url+result.find('a').get('href').strip()
        mainscraper.append(('TBSE',headline,link))
    success.append('TBSE')
except Exception as e:
    failure.append(('TBSE',e))
    pass

# MPBSE
try:
    url = 'http://mpbse.nic.in'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find('div', id ='dvcircular4')
    for result in results.find_all('li'):
        headline = result.find('a').text.strip()
        link= result.find('a').get('href').strip()
        mainscraper.append(('MPBSE',headline,link))
    success.append('MPBSE')
except Exception as e:
    failure.append(('MPBSE',e))
    pass

# CISCE
try:
    url = 'https://www.cisce.org/'
    source = requests.get(url)
    soup = BeautifulSoup(source.text, "html.parser")
    results = soup.find("div", class_ ="table-ul-nb").find_all("li", class_ ="li-content")
    for result in results:
        headline = result.find('a').text.strip()
        link = result.find('a').get('href').strip().replace(' ','%20')
        mainscraper.append(('CISCE',headline,link))
    success.append('CISCE')
except Exception as e:
    failure.append(('CISCE',e))
    pass

# driver.quit()
print('Successful Scrapers -', success)
print('Failed Scrapers -', failure)
df = pd.DataFrame(mainscraper)
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