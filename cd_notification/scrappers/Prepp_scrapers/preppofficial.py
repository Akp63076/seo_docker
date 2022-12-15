from ast import Name

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.by import By
import pandas as pd
#from dotenv import load_dotenv
from bs4 import BeautifulSoup
from datetime import datetime
from zoneinfo import ZoneInfo
import requests
import warnings
import time
# import os
import urllib3
from lxml import etree
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
warnings.filterwarnings('ignore')

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



#UP Police Prepp official

try:
    url = 'http://www.uppbpb.gov.in/'
    name = 'UP Police Prepp official'
    content = requests.get(url)
    soup = BeautifulSoup(content.text,'html.parser')
    headlines = soup.find_all('p',class_='auto-style2')
    for line in headlines:
        headline = ' '.join(line.text.strip().split())
        lnks = line.find_all('a')
        links = []
        for lnk in lnks:
            try:
                if lnk['href'][-3:] == 'pdf':
                    lnk['href'] = url + lnk['href'] 
                links.append(lnk['href'])
            except KeyError:
                pass
        link = ' '.join(links)
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

#Meghalaya Police Prepp official

try:
    url = 'https://megpolice.gov.in/recruitment'
    name = 'Meghalaya Police Prepp official'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    driver.get(url)
    time.sleep(2)
    headlines = driver.find_element(By.CLASS_NAME,'view-content').find_elements(By.CLASS_NAME,'local')
    for line in headlines:
        headline = line.text
        line.click()
        links = []
        lnks = driver.find_elements(By.CLASS_NAME,'linkfilesize2')
        for lnk in lnks:
            links.append(lnk.find_element(By.TAG_NAME,'a').get_attribute('href'))
        link = ' '.join(links)
        news_articles.append((name,headline,link))
        driver.back()
    
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

#Bihar Police Prepp official

try:
    url = 'https://www.csbc.bih.nic.in/'
    name = 'Bihar Police Prepp official'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    driver.get(url)
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source,'html.parser')
    tabs = soup.find_all('li')
    for i in range(len(tabs)):
        driver.find_elements(By.TAG_NAME,'li')[i].click()
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        headlines = soup.find_all('a',class_='wbg')
        for line in headlines[:5]:
            headline = line.text
            link = line['href']
            if not link.startswith('https'):
                link = url + link
            news_articles.append((name,headline,link))
    success.append(name)
    
except Exception as e:
    failure.append((name,e))
    pass


#BSE Odisha Prepp official

try:
    url = 'http://www.bseodisha.ac.in/latest-updates.html'
    name = 'BSE Odisha Prepp official'
    content = requests.get(url)
    soup = BeautifulSoup(content.text,'html.parser')
    headlines = soup.find('div',class_='entry-content').find_all('li')
    for line in headlines[:20]:
        headline = line.text.replace('â\x80\x93','-').strip()
        link = line.find('a')['href']
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

#SBI PO Prepp official

try:
    base_url = 'https://www.sbi.co.in'
    url = 'https://www.sbi.co.in/web/careers'
    name = 'SBI PO Prepp official'
    content = requests.get(url)
    soup = BeautifulSoup(content.text, 'html.parser')
    headlines = soup.find_all('div',class_ = 'descp')
    for line in headlines:
        links = []
        headline = ' '.join(line.text.strip().replace("\xa0"," ").split("\n"))
        link = line.find_all('a')
        for i in range(len(link)):
            if link[i]['href'].startswith('https'):
                link[i]['href'] = link[i]['href']
            else:
                link[i]['href'] = base_url + link[i]['href']
        for i in range(len(link)):
            links.append(link[i]['href'])
        all_link = ' '.join(links)    
        news_articles.append((name,headline,all_link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

#KPSC Prepp official

try:
    url = 'https://kpsc.kar.nic.in/'
    name = 'KPSC Prepp official'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    driver.get('https://kpsc.kar.nic.in/')
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source,'html.parser')
    time.sleep(2)
    headlines = soup.find_all('span',attrs={'style':'color:black'})
    for line in headlines:
        headline = line.text.split("/")[1]
        link = link = line.find('a')['href'].replace(" ","%20")
        if link.startswith("https"):
            link = link
        else:
            link = url + link
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass



#GPSC Prepp official

# try:
#     url = 'https://gpsc.gujarat.gov.in/'
#     base_url = 'https://gpsc.gujarat.gov.in/'
#     name =  'GPSC Prepp official'
#     content = requests.get(url)
#     soup = BeautifulSoup(content.text, "html") 
#     results = soup.find('div', id = 'cn_preview', class_ = 'cn_preview').find_all('div', class_ = 'cn_content')
    
#     for res in results[:10]:
#         try:
#             headline = res.find_all('p')[1].text.replace("\xa0","")
#             link = res.find('a').get('href')
#             if link.startswith('http'):
#                 link = link
#             else:
#                 link = base_url+link
#         except:
#             pass
#         news_articles.append((name, headline, link))
#     success.append(name)
# except Exception as e:
#     failure.append((name,e))
#     pass    

#Rajasthan High Court Prepp official

try:
    url = 'https://hcraj.nic.in/hcraj/recruitment.php'
    base_url = 'https://hcraj.nic.in/hcraj/'
    name =  'Rajasthan High Court Prepp official'
    content = requests.get(url)
    soup = BeautifulSoup(content.text, "html.parser") 
    results = soup.find('ul', class_ = 'my-page-ul').find_all('li')

    for res in results[:4]:
        headline = res.text    
        headline = headline.replace('\n', '')
        link = res.find( 'a').get('href')
        if link.startswith('http'):
            link = link
        else:
            link = base_url+link
            
        if link.endswith('.pdf'):
            news_articles.append((name, headline, link))
        else:
            content1 = requests.get(link)
            soup1 = BeautifulSoup(content1.text, "html.parser") 
            results1 = soup1.find('tbody').find_all('tr')
            for res in results1[:5]:
                headline = res.find_all('td')[1].text
                headline = headline.replace('\t', '').replace('\n', '')
                link = res.find_all('td')[0].find('a').get('href')
                if link.startswith('http'):
                    link = link
                else:
                    link = base_url+link
                news_articles.append((name, headline, link))          
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass            


#Ministry of home affairs Prepp official

try:
    url = 'https://www.mha.gov.in/notifications/vacancies'
    name = 'Ministry of home affairs Prepp official'
    content = requests.get(url)
    soup = BeautifulSoup(content.text, 'html.parser')
    headlines = soup.find('tbody').find_all('tr')
    for line in headlines:
        headline = line.find('td',class_ = 'views-field views-field-title').text.strip()
        link = line.find('a', attrs={'target':'_blank'})['href']
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass


# Manipur PSC Prepp official
try:
    url = 'http://mpscmanipur.gov.in/'
    base_url = 'http://mpscmanipur.gov.in/'
    name =  'Manipur PSC Prepp official'
    content = requests.get(url)
    soup = BeautifulSoup(content.text, "html") 
    results = soup.find('marquee').find_all('ul')
    for res in results:
        headline = res.find('font').text
        link = res.find('a').get('href')
        if link.startswith('http'):
            link = link
        else:
            link = base_url+link
        news_articles.append((name, headline, link))        
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass
    

#AFCAT Prepp official

try:
    url = 'https://afcat.cdac.in/AFCAT/'
    name = 'AFCAT Prepp official'
    content = requests.get(url)
    soup = BeautifulSoup(content.text, 'html.parser')
    headlines = soup.find_all('p',class_= 'font-alt mb-30 titan-title-size-1')
    for line in headlines:
        headline = ' '.join(line.text.strip().split())
        link = line.find('a')['href']
        if link.startswith('https'):
            link = link
        else:
            link = url + link
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

#Indian Post Recruitment Prepp official

try:
    base_url = 'https://www.indiapost.gov.in'
    url = 'https://www.indiapost.gov.in/VAS/Pages/Content/Recruitments.aspx?Category=Recruitment'
    name = 'Indian Post Recruitment Prepp official'
    content = requests.get(url)
    soup = BeautifulSoup(content.text, 'html.parser')
    headlines = soup.find_all('div', class_ = 'marl20')
    for line in headlines:
        headline = line.find('div').text.strip()
        link = line.find('a')['href']
        if link.startswith('https'):
            link = link
        else:
            link = base_url + link
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

#Indian Coast Guard Prepp official

try:
    url = 'https://joinindiancoastguard.gov.in/'
    name = 'Indian Coast Guard Prepp official'
    content = requests.get(url)
    soup = BeautifulSoup(content.text, 'html.parser')
    headlines = soup.find('marquee',attrs={'direction':'up'}).find_all('a')
    for line in headlines:
        headline = line.text.strip()
        link = line['href']
        if link.startswith('https'):
            link = link
        else:
            link = url + link
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# UPSC

try:
    url = 'https://www.upsc.gov.in/whats-new'
    base_url = 'https://www.upsc.gov.in'
    name = "UPSC Prepp official"
#     headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    content = requests.get(url) 
#     print(content.status_code)
    soup = BeautifulSoup(content.text, "html.parser")
    
    result1 = soup.find('ul', class_ = 'test arrows')
    headline = result1.text.replace("\n","")
    link = result1.find('a').get('href')
    if link.startswith('http'):
        link = link
    else:
        link = base_url+link
    news_articles.append((name, headline, link))

    result2 = soup.find_all('span', class_='field-content')
    for r2 in result2[:6]:
        headline = r2.text.replace("\n","")
        link = r2.find('a').get('href')
        if link.startswith('http'):
            link = link
        else:
            link = base_url+link
        news_articles.append((name, headline, link))
        
    result3 = soup.find_all('div', class_ ='field-content')
    for result in result3[:6]:
        headline = result.text.replace("\n","")
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

#Goa PSC Prepp official

try:
    url = 'https://gpsc.goa.gov.in/'
    base_url = 'https://gpsc.goa.gov.in/'
    name = "Goa PSC Prepp official"
    content = requests.get(url)
    soup = BeautifulSoup(content.text, "html.parser")
    res = soup.find_all('table', width = '50%')
    for r in res:
        tds = r.find_all('tr')
        for td in tds[1:]:
            headline = td.text
            headline = headline.split('\n')[2]
            link = td.find('a').get('onclick')
            link = link.split("'")[1]
            if link.startswith('http'):
                link=link
            else:
                link = base_url+link
            news_articles.append((name, headline, link))

    res = soup.find('marquee', onmouseover="this.stop();").find_all('a', target="_blank")
    for r in res:
        headline = r.text
        try:
            link = r.get('onclick')
            link = link.split("'")[1]
            if link.startswith('http'):
                link = link
            else:
                link = base_url+link
        except:
            link = r.get('href')
            if link.startswith('http'):
                link = link
            else:
                link = base_url+link
        news_articles.append((name, headline, link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# UGC NET Prepp official

try:
    url = 'https://ugcnet.nta.nic.in/'
    name = 'UGC NET Prepp official'
    content = requests.get(url)
    soup = BeautifulSoup(content.text, 'html.parser')
    result1 = soup.find_all('a',class_='with-urlchange')
    result2 = soup.find_all('a',attrs={'title':'download'})
    for result in result1:
        headline = result.text.strip()
        link = result['href']
        news_articles.append((name,headline,link))
    for result in result2:
        headline = result.text.strip()
        link = result['href']
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

#Mizoram PSC Prepp official

try:
    url = 'https://mpsc.mizoram.gov.in/'
    base_url = 'https://mpsc.mizoram.gov.in/'
    name =  'Mizoram PSC Prepp official'
    content = requests.get(url)
    soup = BeautifulSoup(content.text, "lxml") 
    results = soup.find('ul', class_ = 'loading-wrapper news-list icon').find_all('li')
    for res in results:
        headline = res.find('a').text
        link = res.find('a').get('href')
        if link.startswith('http'):
            link = link
        else:
            link = base_url+link
        news_articles.append((name, headline, link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass
    
#Meghalaya PSC Prepp official

try:
    url = 'https://mpsc.nic.in/'
    base_url = 'https://mpsc.nic.in/'
    name =  'Meghalaya PSC Prepp official'
    content = requests.get(url)
    soup = BeautifulSoup(content.text, "html") 
    results = soup.find_all('marquee')
    for res in results:
        var = res.find_all('li')
        for v in var[:5]:
            headline = v.text.replace('\r\n', '').replace('  ', '')
            link = v.find('a').get('href')
            if link.startswith('http'):
                link = link
            else:
                link = base_url+link
            news_articles.append((name, headline, link))        
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

#SPSC Prepp official

try:
    url = 'https://spsc.sikkim.gov.in/'
    base_url = 'https://spsc.sikkim.gov.in/'
    name =  'SPSC Prepp official'
    content = requests.get(url, verify = False)
    soup = BeautifulSoup(content.text, "html") 
    results = soup.find('ul', id = 'news').find_all('li', class_ = "list-group-item pl-3")
    for res in results:
        headline = res.find('a').text.split('\r\n')[1]
        link = res.find('a').get('href')
        if link.startswith('http'):
            link=link
        else:
            link = base_url+link
        if link.endswith('.pdf'):
            news_articles.append((name, headline, link))
        else:
            content1 = requests.get(link)
            soup1 = BeautifulSoup(content1.text, "html")
            results1 = soup1.find_all('td', class_ = 'pl-4')
            for res in results1[:3]:
                headnote = res.find('a').text 
                link = res.find('a').get('href')
                if link == '#':
                    results11 = res.find('ol').find_all('li')
                    for res1 in results11:
                        headline = headnote + ' ' + res1.find('a').text
                        headline = headline.replace('\r\n', '').replace('  ', '')
                        link = res1.find('a').get('href')
                        if link.startswith('http'):
                            link = link
                        else:
                            link = base_url+link
                        news_articles.append((name, headline, link))
                        
                else:
                     headnote = headnote.replace('\r\n', '').replace('  ', '')
                     if link.startswith('http'):
                            link = link
                     else:
                         link = base_url+link
                     news_articles.append(( name, headnote, link))              
    success.append(name)
    news_articles = set(news_articles)
except Exception as e:
    failure.append((name,e))
    pass

# NPSC Prepp official

try:
    url = 'https://npsc.nagaland.gov.in/latest-updates'
    base_url = 'https://npsc.nagaland.gov.in/latest-updates'
    name =  'NPSC Prepp official'
    content = requests.get(url)
    soup = BeautifulSoup(content.text, "html") 
    results = soup.find_all('div', class_ = 'fw-bold')
    for res in results:
        try:
            headline = res.find('a').text
            link = res.find('a').get('href')
            news_articles.append((name, headline, link))
        except:
            pass
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

#CSIR NET Prepp official

try:
    url = 'https://csirnet.nta.nic.in/'
    name = 'CSIR NET Prepp official'
    content = requests.get(url)
    soup = BeautifulSoup(content.text, 'html.parser')
    result1 = soup.find_all('a',class_='with-urlchange')
    result2 = soup.find_all('a',attrs={'title':'download'})
    for result in result1:
        headline = result.text.strip()
        link = result['href']
        news_articles.append((name,headline,link))
    for result in result2:
        headline = result.text.strip()
        link = result['href']
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

#MPPSC Prepp official

try:
    url = 'https://mppsc.mp.gov.in/'
    base_url = 'https://mppsc.mp.gov.in/'
    name =  'MPPSC Prepp official'
    content = requests.get(url, verify=False)
    soup = BeautifulSoup(content.text, "lxml") 
    results = soup.find_all('ul', class_='menu nav')
    results.pop(2)
    for r in results:
        var = r.find_all('li', class_ = 'leaf')
        for vr in var[:10]:
            headline = vr.text
            link = vr.find('a').get('href')
            if link.startswith('http'):
                    link=link
            else:
                link = base_url+link
            news_articles.append((name, headline, link))

    results1 = soup.find('marquee', onmouseover='this.stop();').find_all('li')
    for res in results1:
        headline = res.text
        link = res.find('a').get('href')
        news_articles.append((name, headline, link))

    success.append((name))
except Exception as e:
    failure.append((name,e))
    pass

#APPSC Prepp official

try:
    url = 'https://psc.ap.gov.in/(S(zws14n0sxgaixzgjwd4rgf51))/Default.aspx'
    base_url = 'https://psc.ap.gov.in/(S(zws14n0sxgaixzgjwd4rgf51))/'
    name = "APPSC Prepp official"
    content = requests.get(url)
    soup = BeautifulSoup(content.text, "html.parser")    
    results = soup.find_all('div', class_ = 'row marquee_div')
    for res in results:
        try:
            var = res.find('span', class_ = 'blinkNew')
            headline = var.text.replace('\n', '').replace('\r', '').replace('   ', '')
            link = var.find('a').get('href')
            if link.startswith('http'):
                link = link
            else:
                link = base_url+link
            news_articles.append((name, headline, link))
        except Exception as e:
            pass
    success.append(name)
    
except Exception as e:
    failure.append((name,e))
    pass

# Arunachal psc Prepp official

try:
    #Home Page
    url = 'https://appsc.gov.in/Index/institute_home/ins/RECINS001'
    name = 'Arunachal psc Prepp official'
    content = requests.get(url)
    soup = BeautifulSoup(content.text, 'html.parser')
    headlines = soup.find('ul',class_ = 'newsticker').find_all('li')
    for line in headlines:
        headline = line.text.strip()
        link = line.find('a')['href']
        news_articles.append((name,headline,link))
    #Notification Page
    url = 'https://appsc.gov.in/Index/sub_page/doc12233/Notifications'
    name = 'Arunachal psc'
    content = requests.get(url)
    soup = BeautifulSoup(content.text, 'html.parser')
    headlines = soup.find('tbody').find_all('tr')
    for line in headlines:
        headline = line.find('td',attrs={'width':'70%'}).text.strip()
        link = line.find('a')['href']
        news_articles.append((name,headline,link))
    #Results Page
    url = 'https://appsc.gov.in/Index/sub_page/doc37276/Results_'
    name = 'Arunachal psc'
    content = requests.get(url)
    soup = BeautifulSoup(content.text, 'html.parser')
    headlines = soup.find('tbody').find_all('tr')
    for line in headlines:
        headline = line.find('td',attrs={'width':'70%'}).text.strip()
        link = line.find('a')['href']
        news_articles.append((name,headline,link))
    
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass


#HPSC Prepp official

try:
    url = 'http://hpsc.gov.in/en-us/Announcements'
    base_url = 'http://hpsc.gov.in'
    name = "HPSC Prepp official"
    content = requests.get(url)
    soup = BeautifulSoup(content.text, "html.parser")    
    results = soup.find('div', id = 'dnn_ctr19159_HtmlModule_lblContent')
    results = results.find_all('td')
    for res in results[:22]:
        try:
            headline = res.find('a').text
            link = res.find('a').get('href')
            if link.startswith('http'):
                link = link
            else:
                link = base_url+link
            news_articles.append((name, headline, link))

        except:
            pass
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# RRB Chandigarh Prepp official
try:
    url = 'https://www.rrbcdg.gov.in/'
    name = 'RRB Chandigarh Prepp official'
    content = requests.get(url)
    soup = BeautifulSoup(content.text,'html.parser')
    headlines = soup.find_all('td',attrs={'style':"color:#000;vertical-align:middle;"})
    for line in headlines:
        headline = ' '.join(line.text.strip().split())
        link = line.find('a')['href'].replace(' ','%20')
        if link.startswith('https'):
            link = link
        else:
            link = url + link
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# JPSC
try:
    url = "http://jpsc.gov.in/"
    name = "JPSC Prepp official"
    res = requests.get(url,verify=False)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find("ul",  id='ulid')
    for result in results.find_all("a"):
        headline = result.text.strip()
        link= url + result.get('href').strip()
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# MPSC
try:
    url = 'https://mpsc.gov.in/'
    base_url = 'https://mpsc.gov.in/'
    name = "MPSC Prepp official"
#     headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    content = requests.get(url, verify = False)
#     print(content.status_code)
    soup = BeautifulSoup(content.text, "html.parser")
    results = soup.find_all('div', class_ = 'alert alert-secondary')
    for result in results:
        headline = result.text.replace("\n","").replace("\r","").replace("\t","")
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

# PPSC
try:
    base_url='https://www.ppsc.gov.in'
    url = 'https://www.ppsc.gov.in/'
    name = "PPSC Prepp official"
    res = requests.get(url, verify=False)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find('td', class_='newdesigntabletd_withoutborder_2')
    for result in results.find_all('a'):
        headline = result.text.strip()
        link= base_url + result.get('href').strip()
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# SSC
try:
    name="SSC Prepp official"
    base_url="https://ssc.nic.in/"
    url="https://ssc.nic.in/"
    source = requests.get('https://ssc.nic.in/',verify=False).text
    soup = BeautifulSoup(source, 'html.parser')
    table = soup.find('div', class_="scrollingNotifications_New scrollbar")
    for td in table.find_all('div', class_="eachNotification"):
            headline = td.p.a.text.strip()
            try:
                link = td.p.a.get('href')
            except:
                pass
            news_articles.append((name,headline,link))       
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# Kerala PSC
try:
    url = 'https://www.keralapsc.gov.in/latest'
    base_url = 'https://www.keralapsc.gov.in'
    name = "Kerala PSC Prepp official"
#     headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    content = requests.get(url, verify = False)
#     print(content.status_code)
    soup = BeautifulSoup(content.text, "html.parser")
    results = soup.find_all('td', class_ = 'views-field views-field-title')
    results2 = soup.find_all('td', class_ = 'views-field views-field-field-file')

    
    for result, result2 in zip(results, results2):  
        headline = result.text
        link = result2.find('a').get('href')
        if link.startswith('http'):
            link = link
        else:
            link = base_url+link  
            
        news_articles.append((name, headline, link))
    success.append(name) 
    
except Exception as e:
    failure.append((name,e))
    pass


# UPTET(1)
try:
    base_url = 'http://updeled.gov.in/'
    name = "UPTET Prepp official"
    res = requests.get(base_url,verify=False)
    soup = BeautifulSoup(res.text, 'html.parser')
    newss = soup.find_all(class_='news-item')
    for news in newss:
        headline = news.get_text().strip()
        url= news.select('a')[0].get('href')
        link = base_url+url
        if headline == '' or None:
            continue
        news_articles.append((name, headline[:999], link))
    success.append(name)
except Exception as e:
    failure.append((name, e))
    pass

# IBPS
# try:
#     base_url = 'https://ibps.in/'
#     res = requests.get(base_url,verify=False)
#     soup = BeautifulSoup(res.text, 'html.parser')
#     newss = soup.find_all('marquee')[0].find_all('a')
#     for news in newss:
#         headline = news.get_text()
#         link = news.get('href')
#         if headline == '' or None:
#             continue
#         news_articles.append(('IBPS', headline[:999], link))
#     success.append('IBPS')
# except Exception as e:
#     failure.append(('IBPS', e))
#     pass

#Bank Of India
try:
    source=requests.get('https://bankofindia.co.in/career',verify = False).text
    url='https://bankofindia.co.in'
    name = "Bank Of India Prepp official"
    soup=BeautifulSoup(source,'html.parser')
    url1="https://bankofindia.co.in/career"
    div=soup.find('div',class_="listing col-sm-12")
    for a in div.find_all('a'):
        text=a.text
        link=a['href']
        text=text.lstrip()
        text=text.rstrip()
        link=link.lstrip()
        link=link.lstrip('. .')
        link=link.rstrip()
        #text= " ".join(text.split())
        if 'http' not in link:
             link=url+link
        if 'javascript' in link:
            continue
        news_articles.append((name,text,link))
    success.append(name)
 #print(news_articles)
except Exception as e:
    failure.append((name,e))
    pass

#TNPSC
try:

    source=requests.get('https://www.tnpsc.gov.in/English/press_releases.aspx',verify=False).text
    name = "TNPSC Prepp official"
    url='https://www.tnpsc.gov.in/'
    soup=BeautifulSoup(source,'html.parser')
    table=soup.find('tbody')
    for tr in table.find_all('tr'):
        td=tr.find_all('td')
        text=td[2].text
        link=td[3].a['href']
        text=text.lstrip()
        text=text.rstrip()
        link=link.lstrip()
        link=link.rstrip()
        link=link.lstrip('. ./')
        text= " ".join(text.split())
        if 'http' not in link:
            link=url+link
         #print(text,end=" ")
         #print(link) 
        news_articles.append((name,text,link))
    success.append(name)
 #print(news_articles) 
except Exception as e:
    failure.append((name,e))
    pass

#CIPET
try:
    url = 'https://www.cipet.gov.in/whatisnew.php'
    name = "CIPET Prepp official"
    res = requests.get(url,verify=False)
    soup=BeautifulSoup(res.text,'html.parser')

    head = soup.find('ul',class_='maincontentsubpagecontentp').find_all('a',target='_blank')
    for l in head:
        headline = l.get_text().strip()[:999]
        headline=headline.replace('\xa0','')
        l1 = l.get('href')
        news_articles.append((name,headline,l1))
    #print(news_articles)
    success.append((name))
except Exception as e:
    failure.append((name,e))
    pass



# Indian post
try:
    url= 'https://www.indiapost.gov.in'
    name = "Indian post Prepp official"
    source=requests.get('https://www.indiapost.gov.in/VAS/Pages/Content/Recruitments.aspx?Category=Recruitment',verify=False).text
    soup=BeautifulSoup(source,'html.parser')
    div=soup.find_all('div',class_="col-xs-12 col-md-12")
    for a in div[2].find_all('a'):
        text=a.text
        link=a['href']
        text=text.lstrip()
        text=text.rstrip()
        link=link.lstrip()
        link=link.rstrip()
        if 'http' not in link:
            link=url+link
            news_articles.append((name,text,link))
    success.append(name)
 #print(news_articles) 
except Exception as e:
    failure.append((name,e))
    pass

#CTET

try:
    url = 'https://ctet.nic.in/'
    name = "CTET Prepp official"
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    try:
        results = soup.find_all('div', class_='vc_tta-panels')
        for res in results:
            res2 = res.find_all('li')
            for r in res2:
                headline = r.find('a').text.strip()
                link = r.find('a', href=True).get('href').strip()
                news_articles.append((name, headline, link))
    except Exception as e:
        pass

    success.append(name)
    # print(news_articles)
except Exception as e:
    failure.append((name, e))
    pass

#RSMSSB(Latest News)

try:
    base_url = 'https://rsmssb.rajasthan.gov.in/'
    url = 'https://rsmssb.rajasthan.gov.in/page?menuName=ApBuI6wdvnNKC6MoOgFsfXwFRsE7cKLr'
    name = "RSMSSB-Latest News Prepp official"
    req = requests.get(url)
    # print(req.status_code == 200)
    soup = BeautifulSoup(req.text, 'html.parser')
    results = soup.find('div', class_='content_').find_all('li')
    for res in results:
        headline = res.find('a').text
        link = base_url + res.find('p').find('a').get('href').strip()
        news_articles.append((name, headline, link))
    success.append(name)
except Exception as e:
    failure.append((name, e))
    pass

#RSMSSB(Results)

try:
    base_url = 'https://rsmssb.rajasthan.gov.in/'
    url = 'https://rsmssb.rajasthan.gov.in/page?menuName=XThs/FdacUY='
    name = "RSMSSB-Results Prepp official"
    req = requests.get(url)
    # print(req.status_code == 200)
    soup = BeautifulSoup(req.text, 'html.parser')
    results = soup.find('tbody').find_all('tr')
    for res in results[:10]:
        try:
            headline = res.find('a').text.strip()
            link = base_url + res.find_all('td')[1].find('a').get('href')
            news_articles.append((name, headline, link))

        except Exception as e:
            pass
    success.append(name)
except Exception as e:
    failure.append((name, e))
    pass

# RSMSSB(Recruitment Advertisement)
# try:
#     base_url = 'https://rsmssb.rajasthan.gov.in/'
#     url = 'https://rsmssb.rajasthan.gov.in/page?menuName=EJwE/Y7GD1hMok0YfKTFOtUJMJFGLBa;455611;jbRgWtRe9q4='
#     req = requests.get(url)
#     # print(req.status_code == 200)
#     soup = BeautifulSoup(req.text, 'html.parser')
#     results = soup.find('tbody').find_all('tr')
#     for res in results[:10]:
#         try:
#             headline = res.find('a').text.strip()
#             link = base_url + res.find_all('td')[1].find('a').get('href')
#             news_articles.append(('RSMSSB-Recruitment Ad', headline, link))
#         except Exception as e:
#             pass
#     success.append('RSMSSB-Recruitment Ad')
# except Exception as e:
#     failure.append(('RSMSSB-Recruitment Ad', e))
#     pass

#DSSSB

try:
    url = 'https://dsssb.delhi.gov.in'
    base_url = 'https://dsssb.delhi.gov.in'
    name = "DSSSB Prepp official"
#     headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    content = requests.get(url, verify = False)
#     print(content.status_code)
    soup = BeautifulSoup(content.text, "html.parser")
    results = soup.find_all('li', class_ = 'menu-217')
    for result in results:
        headline=  result.text.replace("\n","")
        link = result.find('a').get('href')
        if link.startswith('http'):
            link =  link
        else:
            link = base_url+link
        news_articles.append((name, headline, link))

    results2 = soup.find_all('span', class_ = 'field-content')
    for result in results2:
        headline=  result.text.replace("\n","")
        link = result.find('a').get('href')
        if link.startswith('http'):
            link =  link
        else:
            link = base_url+link
        news_articles.append((name, headline, link))
    success.append(name) 
    
except Exception as e:
    failure.append((name,e))
    pass

#RPSC

try:
    name = 'RPSC Prepp official'
    url = 'https://rpsc.rajasthan.gov.in'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    # driver = webdriver.Edge(executable_path = 'D:\\edgedriver\\msedgedriver.exe')
    # driver.maximize_window()
    req = driver.get(url)

    time.sleep(2)
    (driver.find_element(By.XPATH,"//*[@id='carouselModal']/div[2]/div/div[3]/button")).click()
    time.sleep(2)
    (driver.find_element(By.XPATH,"//*[@id='aspnetForm']/div[3]/div[1]/div[2]/div[3]/div/div[3]/a")).click()

    elems = driver.find_elements(By.CLASS_NAME, "NewsAnchor")
    j = 0
    for elem in elems:
        if j <= 15:
            text = elem.text[10:]
            link = elem.get_attribute("href")
            news_articles.append((name,text,link))
            # print(name,text,link)
            j+=1
    success.append(name)
    
except Exception as e:
    failure.append((name, e))
    pass

#PSPCL(Notification)
try:
    url = 'https://pspcl.in/'
    base_url = 'https://pspcl.in/'
    name = "PSPCL Prepp official"
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    results = soup.find_all("div", class_='ticker-2')
    for res in results:
        try:
            var1 = res.find_all('li')
            for var in var1:
                headline = var.find('a').text.strip()
                link_ = var.find('a', href=True).get('href').strip()
                if link_.startswith(' https') == True:
                    link = link_
                else:
                    link = base_url+link_
                news_articles.append((name, headline, link))
            
        except Exception as e:
            pass
    success.append(name)        
except Exception as e:
    failure.append((name, e))
    pass

#PSPCL(Press Release)

try:
    url = 'https://pspcl.in/'
    base_url = 'https://pspcl.in/'
    name = "PSPCL Prepp official"
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    results = soup.find_all("div", class_='ticker-2')
    for res in results:
        try:
            var1 = res.find_all('a')
            for var in var1:
                headline = var.text.strip()
                link_ = var.get('href').strip()
                if link_.startswith('https') == True:
                    link =link_
                else:
                    link= base_url+link_
                news_articles.append((name, headline, link))
        except Exception as e:
            pass
    success.append(name)
except Exception as e:
    failure.append((name, e))
    pass

#UPSSSC
try:
    url = 'http://upsssc.gov.in/Default.aspx'
    name = 'UPSSSC Prepp official'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    driver.get(url)
    time.sleep(2)
    driver.find_element(By.XPATH,'//*[@id="fontSize"]/div/div/div/div/div[2]/div/div/div/h3/a').click()
    time.sleep(2)
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    headlines = soup.find_all('li',attrs={'style':'color:#0000ee;'})
    for i in range(len(headlines)):
        headline = headlines[i].find('a')['title']
        xpath = '//*[@id="ContentPlaceHolder1_Alert_Silder"]/ul/li[{}]/a'.format(i+1)
        driver.find_element(By.XPATH,xpath).click()
        driver.switch_to.window(driver.window_handles[1])
        link = driver.current_url
        news_articles.append((name,headline,link))
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

#BPSC
# try:
#     url = 'https://www.bpsc.bih.nic.in/'
#     base_url = 'https://www.bpsc.bih.nic.in/'
#     name = "BPSC Prepp official"
# #     headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
#     content = requests.get(url) 
# #     print(content.status_code)
#     soup = BeautifulSoup(content.text, "html.parser")
#     results = soup.find_all('td',  class_ ='C3', valign = 'top')
    
#     for result in results[:25]:
#             try:
#                 headline = result.text
#                 if bool(datetime.strptime(headline, '%d-%m-%Y')):
#                     pass
#             except:
#                 headline = headline
                
#                 links = result.find_all('a')
#                 if len(links) >1:
#                     link = []
#                     for l in links:
#                         link_ = l.get('href')
#                         if link_.startswith('http'):
#                             lk = link_
#                         else:
#                             lk = base_url+link_
#                         link.append(lk)
                    
# #                 print(headline, link, sep='\n')
#                 news_articles.append((name, headline, str(link)))
            
#     success.append((name))
# except Exception as e:
#     failure.append((name,e))
#     pass

try:
    url = 'https://www.bpsc.bih.nic.in/'
    name = 'BPSC Prepp official'
    content = requests.get(url)
    soup = BeautifulSoup(content.text,'html.parser')
    headlines = soup.find('table',attrs={'id':'table1'}).find_all('tr')[1:21]
    for line in headlines:
        headline = line.find_all('td')[1].text.strip()
        link = line.find('a')['href']
        if not link.startswith('https'):
            link = url + link
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

#CGPSC

try:
    url = 'https://www.psc.cg.gov.in/'
    name = 'CG-PSC Prepp official'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    # driver = webdriver.Edge(executable_path = 'D:\\edgedriver\\msedgedriver.exe')
    # driver.maximize_window()
    req = driver.get(url)
    time.sleep(2)

    # Notification
    Xpath_link = '/html/body/table/tbody/tr/td/table/tbody/tr[4]/td/table/tbody/tr[1]/td[2]/table/tbody/tr[2]/td[1]/span/a'
    link_a = driver.find_elements(By.XPATH,Xpath_link)
    for i in range(20):
        # print(link_a[i].text)
        # print(link_a[i].get_attribute('href'))
        text = link_a[i].text
        link = link_a[i].get_attribute('href')
        news_articles.append((name,text,link))
        # print((name,text,link))
    success.append(name)
    
except Exception as e:
    failure.append((name, e))
    pass

#IBPS
try:
    url = 'https://ibps.in/'
    base_url = 'https://ibps.in/'
    name = "IBPS Prepp official"
#     headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    content = requests.get(url, verify = False)
#     print(content.status_code)
    soup = BeautifulSoup(content.text, "html.parser")
    mqs = soup.find_all('div', style = 'clear:both;padding:10px 5px;')
    for mq in mqs:
        try:
            headlines = mq.find_all('a')
            for line in headlines:
                headline = line.text
                link = line.get('href')
                if link.startswith('http'):
                    link = link
                else:
                    link = base_url+link
                    
                if link.endswith('.pdf'):
                    news_articles.append((name, headline, link))
                else:
                    response = requests.get(link, verify =False)
                    soup = BeautifulSoup(response.text, "html.parser")
                    links = soup.find_all('div', style = 'clear:both;padding:10px 5px 10px 45px;border-radius:5px;margin-bottom:5px;background:url(https://www.ibps.in/wp-content/themes/ibps/images/hand-right.png) no-repeat 10px 2px #F4F4F4;')
                    if len(links) ==0:
                        news_articles.append((name, headline, link))
                    else:
                        for link_ in links:
                            headline = link_.find('a').text
                            link = link_.find('a').get('href')
                            news_articles.append((name,headline, link))        
                
                
        except Exception as e:
            failure.append((name,e))
            pass
        
        news_articles = list(set(news_articles))
        try:
            url = 'https://ibps.in/'
            base_url = 'https://ibps.in/'
            name = "IBPS Prepp official"
#             headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
            content = requests.get(url, verify = False)
        #     print(content.status_code)
            soup = BeautifulSoup(content.text, "html.parser")
            mqs = soup.find_all('div', style = 'clear:both;padding:40px 5px;')
            for mq in mqs:
                try:
                    headlines = mq.find_all('a')
                    for line in headlines:
                        headline = line.text
                        link = line.get('href')
                        if link.startswith('http'):
                            link = link
                        else:
                            link = base_url+link
                        news_articles.append((name, headline, link))
                except Exception as e:
                    # print('exp', e)
                    pass
                news_articles.append((name, headline, link))
                
            news_articles = list(set(news_articles))
        except Exception as e:
            failure.append((name,e))
            pass
#     print(news_articles)
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass


#CDS

try:

    source=requests.get('https://www.upsc.gov.in/whats-new',verify=False).text
    url='https://www.upsc.gov.in'
    name = "CDS Prepp official"
    soup=BeautifulSoup(source,'html.parser')
    div=soup.find('div',class_="view-content")
    for a in div.find_all('a'):
        text=a.text
        link=a['href']
        text=text.lstrip()
        text=text.rstrip()
        link=link.lstrip()
        link=link.rstrip()
        link=link.lstrip('. .')
        #text= " ".join(text.split())
        if 'http' not in link:
            link=url+link
        news_articles.append((name,text,link))
    success.append(name)
 #print(news_articles) 
except Exception as e:
    failure.append((name,e))
    pass

#WBPSC
try:
    url = 'https://wbpolice.gov.in/WBP/common/WBP_RecruitmentNew.aspx'
    name = 'WBPSC Prepp official'
    
    driver.get(url)
    for i in range(5):
        driver.find_elements(By.LINK_TEXT,'Get Details')[i].click()
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source,'html.parser')
        headlines = soup.find('div',attrs={'id':'ctl00_ContentPlaceHolder1_updtR'}).find_all('td',attrs={'align':'left'})
        links = soup.find('div',attrs={'id':'ctl00_ContentPlaceHolder1_updtR'}).find_all('a')
        for i in range(len(headlines)):
            headline = headlines[i].text.strip()
            link = links[i]['href']
            if not link.startswith('https'):
                link = link.replace("../..",'https://wbpolice.gov.in')
            news_articles.append((name,headline,link))
        driver.back()
        time.sleep(2)

    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

#JPSC
try:
    source=requests.get('https://www.jpsc.gov.in/index.php').text
    url='https://www.jpsc.gov.in/'
    name = "JPSC Prepp official"
    soup=BeautifulSoup(source,'html.parser')
    ul=soup.find('ul',id="ulid")
    for a in ul.find_all('a'):
        text=a.text
        link=a['href']
        text=text.lstrip()
        text=text.rstrip()
        link=link.lstrip()
        link=link.rstrip()
        link=link.lstrip('. .')
        #text= " ".join(text.split())
        if 'http' not in link:
            link=url+link
       # print(text,end=" ")
       # print(link)   
        news_articles.append((name,text,link))
    success.append(name)
     #print(news_articles) 
except Exception as e:
    failure.append((name,e))
    pass

#TSPSC
# try:

#     source=requests.get('https://www.tspsc.gov.in/').text
#     url='https://www.tspsc.gov.in'
#     soup=BeautifulSoup(source,'html.parser')
#     div=soup.find_all('div',class_="col-sm-4")
#     text=div[1].a.text
#     link=div[1].a['href']
#     text=text.lstrip()
#     text=text.rstrip()
#     link=link.lstrip()
#     link=link.rstrip()
#     link=link.lstrip('. .')
#     #text= " ".join(text.split())
#     if 'http' not in link:
#         link=url+link
#         news_articles.append(('TSPSC',text,link))
#     success.append('TSPSC')
#  #print(news_articles) 
# except Exception as e:
#     failure.append(('TSPSC',e))
#     pass

#UPTET


try:
    source=requests.get('https://updeled.gov.in/').text
    url='https://updeled.gov.in/'
    name = "UPTET Prepp official"
    soup=BeautifulSoup(source,'html.parser')
    section=soup.find('section',class_="news")
    for a in section.find_all('a'):
        text=a.text
        link=a['href']
        text=text.lstrip()
        text=text.rstrip()
        link=link.lstrip()
        link=link.rstrip()
        link=link.lstrip('. .')
        #text= " ".join(text.split())
        if 'http' not in link:
            link=url+link
     # print(text,end=" ")
     # print(link)
        news_articles.append((name,text,link))
    success.append(name)
 #print(news_articles) 
except Exception as e:
    failure.append((name,e))
    pass

#JKPSC

try:
    url = 'http://jkpsc.nic.in/'
    name = 'JKPSC Prepp official'
    content = requests.get(url)
    soup = BeautifulSoup(content.text,'html.parser')
    headlines = soup.find('ul',class_= 'notificationnews myBox').find_all('li')[:-1]
    for line in headlines:
        if line.find('a')['href'] != '':
            headline = line.find('a').text.strip().replace("\r\n"," ")
            link = line.find('a')['href']
            if not link.startswith('http'):
                link = url + link
            news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

#HPPSC

try:
    source=requests.get('http://www.hppsc.hp.gov.in/hppsc/').text
    url='http://www.hppsc.hp.gov.in'
    name = "HPPSC Prepp official"
    soup=BeautifulSoup(source,'html.parser')
    div=soup.find('div',class_="media")
    for a in div.find_all('a'):
        text=a.text    
        link=a['href']
        text=text.lstrip()
        text=text.rstrip()
        link=link.lstrip()
        link=link.rstrip()
        if 'http' not in link:
            link=url+link
        news_articles.append((name,text,link))
    success.append(name)
 #print(news_articles) 
except Exception as e:
    failure.append((name,e))
    pass

#RRB Kolkata

try:
    source=requests.get('https://www.rrbkolkata.gov.in/').text
    url='https://www.rrbkolkata.gov.in/'
    name = "RRB Kolkata Prepp official"
    soup=BeautifulSoup(source,'html.parser')

    a=soup.find('a',href="/lst5news.php")
    text=a.text    
    link=a['href']
    text=text.lstrip()
    text=text.rstrip()
    link=link.lstrip()
    link=link.rstrip()
    if 'http' not in link:
        link=url+link
        news_articles.append((name,text,link))
    success.append(name)
 #print(news_articles) 
except Exception as e:
    failure.append((name,e))
    pass

#Rajasthan high court

try:

    source=requests.get('https://hcraj.nic.in/hcraj/recruitment.php',verify = False).text
    url='https://hcraj.nic.in/hcraj/'
    name = "Rajasthan high court Prepp official"
    soup=BeautifulSoup(source,'html.parser')
    ul=soup.find('ul',class_="my-page-ul")
    for a in ul.find_all('a'):
        text=a.text    
        link=a['href']
        text=text.lstrip()
        text=text.rstrip()
        link=link.lstrip()
        link=link.rstrip()
        if 'http' not in link:
            link=url+link
      #print(text,end=" ")
      #print(link)
        news_articles.append((name,text,link))
    success.append(name)
 #print(news_articles) 
except Exception as e:
    failure.append((name,e))
    pass

#APSC

try:

    source=requests.get('http://www.apsc.nic.in/').text
    url='http://www.apsc.nic.in/'
    name = "APSC Prepp official"
    soup=BeautifulSoup(source,'html.parser')
    ul=soup.find_all('ul',class_="scroll-updates")
    for a in ul[1].find_all('a'):
        text=a.text    
        link=a['href']
        text=text.lstrip()
        text=text.rstrip()
        link=link.lstrip()
        link=link.rstrip()
        if 'http' not in link:
            link=url+link
            news_articles.append((name,text,link))
    success.append(name)
 #print(news_articles) 
except Exception as e:
    failure.append((name,e))
    pass

#JSSC

try:
    source=requests.get('http://www.jssc.nic.in/',verify=False).text
    url='http://www.jssc.nic.in/'
    name = "JSSC Prepp official"
    soup=BeautifulSoup(source,'html.parser')
    div=soup.find('div',class_="section")
    for a in div.find_all('a'):
        text=a.text    
        link=a['href']
        text=text.lstrip()
        text=text.rstrip()
        link=link.lstrip()
        link=link.rstrip()
        if 'http' not in link:
            link=url+link
        news_articles.append((name,text,link))
    success.append(name)
 #print(news_articles) 
except Exception as e:
    failure.append((name,e))
    pass

#ESIC Recruitment

try:

    source=requests.get('https://www.esic.nic.in/recruitments').text
    url='https://www.esic.nic.in/recruitments'
    name = "ESIC Recruitment Prepp official"
    soup=BeautifulSoup(source,'html.parser')
    p=soup.find('p',class_="marquee-grid")
    for a in p.find_all('a'):
        text=a.text    
        link=a['href']
        text=text.lstrip()
        text=text.rstrip()
        link=link.lstrip()
        link=link.rstrip()
        if 'http' not in link:
            link=url+link
        news_articles.append((name,text,link))
    success.append(name)
 #print(news_articles) 
except Exception as e:
    failure.append((name,e))
    pass


#Haryana Police
# try:

#     source=requests.get('https://haryanapolice.gov.in/login').text
#     url='https://haryanapolice.gov.in/'
#     soup=BeautifulSoup(source,'html.parser')
#     marquee=soup.find('marquee',direction="left")
#     a=marquee.find_all('a')
#     for i in range(0,2):
#         text=a[i].text    
#         link=a[i]['href']
#         text=text.lstrip()
#         text=text.rstrip()
#         link=link.lstrip()
#         link=link.rstrip()
#         if 'http' not in link:
#             link=url+link
#         news_articles.append(('Haryana Police',text,link))
#     success.append('Haryana Police')
#      #print(news_articles) 
# except Exception as e:
#     failure.append(('Haryana Police',e))
#     pass

#IPPB
try:
    source=requests.get('https://www.ippbonline.com/').text
    url='https://www.ippbonline.com/'
    name = "IPPB Prepp official"
    soup=BeautifulSoup(source,'html.parser')
    div=soup.find('div',class_="tab-pane fade",id="menu2")
    for a in div.find_all('a'):
        text=a.text
        link=a['href']
    #    if link==None:
    #        link=url
        text=text.lstrip()
        text=text.rstrip()
        link=link.lstrip()
        link=link.rstrip()
        #text= " ".join(text.split())
        if 'http' not in link:
            link=url+link
        news_articles.append((name,text,link))
    success.append(name)
 #print(news_articles) 
except Exception as e:
    failure.append((name,e))
    pass

#Bihar Police

try:

    source=requests.get('https://www.csbc.bih.nic.in/Default.htm').text
    url='https://www.csbc.bih.nic.in/'
    name = "Bihar Police Prepp official"
    soup=BeautifulSoup(source,'html.parser')
    table=soup.find_all('table',class_="normal")
    text=table[3].a.text
    link=table[3].a['href']
    #    if link==None:
    #        link=url
    text=text.lstrip()
    text=text.rstrip()
    link=link.lstrip()
    link=link.rstrip()
    #text= " ".join(text.split())
    if 'http' not in link:
        link=url+link
    news_articles.append((name,text,link))
    success.append(name)
 #print(news_articles) 
except Exception as e:
    failure.append((name,e))
    pass

#Assam Police

# try:

#     source=requests.get('https://police.assam.gov.in/portlets/career-and-recruitment').text
#     url='https://police.assam.gov.in/portlets/career-and-recruitment'
#     soup=BeautifulSoup(source,'html.parser')
#     table=soup.find_all('table')
#     td=table[0].find_all('td')
#     #print(td[1].text)
#     text=td[1].text
#     link=td[2].a['href']
#     #    if link==None:
#     #        link=url
#     text=text.lstrip()
#     text=text.rstrip()
#     link=link.lstrip()
#     link=link.rstrip()
#     #text= " ".join(text.split())
#     if 'http' not in link:
#         link=url+link
#     news_articles.append(('Assam Police',text,link))
#     success.append('Assam Police')
#  #print(news_articles) 
# except Exception as e:
#     failure.append(('Assam Police',e))
#     pass

#RBI Assistant

try:

    source=requests.get('https://opportunities.rbi.org.in/Scripts/Vacancies.aspx').text
    url='https://opportunities.rbi.org.in/Scripts/'
    name = "RBI Assistant Prepp official"
    soup=BeautifulSoup(source,'html.parser')
    div=soup.find('div',class_="grid_8 alpha content_area omega")
    for a in div.find_all('a'):
        text=a.text
        link=a['href']
        #    if link==None:
        #        link=url
        text=text.lstrip()
        text=text.rstrip()
        link=link.lstrip()
        link=link.rstrip()
        #text= " ".join(text.split())
        if 'http' not in link:
            link=url+link
        news_articles.append((name,text,link))
    success.append(name)
     #print(news_articles) 
except Exception as e:
    failure.append((name,e))
    pass

#CWC

try:
    source=requests.get('https://www.cewacor.nic.in/').text
    url='https://www.cewacor.nic.in/'
    name = "CWC Prepp official"
    soup=BeautifulSoup(source,'html.parser')
    div=soup.find('div',class_="microsoft mark")
    for a in div.find_all('a'):
        text=a.text
        link=a['href']
        #    if link==None:
        #        link=url
        text=text.lstrip()
        text=text.rstrip()
        link=link.lstrip()
        link=link.rstrip()
        #text= " ".join(text.split())
        if 'http' not in link:
            link=url+link
        news_articles.append((name,text,link))
    success.append(name)
 #print(news_articles) 
except Exception as e:
    failure.append((name,e))
    pass

#IES

try:
    source=requests.get('https://www.upsc.gov.in/',verify=False).text
    url='https://www.upsc.gov.in/'
    name = "IES Prepp official"
    soup=BeautifulSoup(source,'html.parser')
    div=soup.find('div',class_="whats-new-marq")
    for a in div.find_all('a'):
        text=a.text
        link=a['href']
        #    if link==None:
        #        link=url
        text=text.lstrip()
        text=text.rstrip()
        link=link.lstrip()
        link=link.rstrip()
        #text= " ".join(text.split())
        if 'http' not in link:
            link=url+link
        news_articles.append((name,text,link))
    success.append(name)
 #print(news_articles) 
except Exception as e:
    failure.append((name,e))
    pass

#TPSC
try:
    source=requests.get('https://tpsc.tripura.gov.in/',verify=False).text
    url='https://tpsc.tripura.gov.in/'
    name = "TPSC Prepp official"
    soup=BeautifulSoup(source,'html.parser')
    ul=soup.find('ul',id="whats-new")
    for a in ul.find_all('a'):
        text=a.text
        link=a['href']
        #    if link==None:
        #        link=url
        text=text.lstrip()
        text=text.rstrip()
        link=link.lstrip()
        link=link.rstrip()
        #text= " ".join(text.split())
        if 'http' not in link:
            link=url+link
        news_articles.append((name,text,link))
    success.append(name)
 #print(news_articles) 
except Exception as e:
    failure.append((name,e))
    pass


#UKPSC
try:
    source=requests.get('https://ukpsc.gov.in/latestupdate').text
    url='https://ukpsc.gov.in/'
    name = "UKPSC Prepp official"
    soup=BeautifulSoup(source,'html.parser')
    ul=soup.find('ul',class_="genList")
    for a in ul.find_all('a'):
        text=a.text
        link=a['href']
        text=text.lstrip()
        text=text.rstrip()
        link=link.lstrip()
        link=link.rstrip()
        text= " ".join(text.split())
        if 'http' not in link:
            link=url+link
        news_articles.append((name,text,link))
    success.append(name)
 #print(news_articles)
except Exception as e:
    failure.append((name,e))
    pass

#UPPSC Prepp Official

try:
    url = 'https://uppsc.up.nic.in/'
    name = 'UPPSC Prepp Official'
    driver.get(url)
    driver.switch_to.frame(driver.find_element(By.TAG_NAME,'iframe'))
    soup = BeautifulSoup(driver.page_source,'html.parser')
    headlines = soup.find_all('li')
    for line in headlines:
        headline = line.find('a').text
        driver.find_element(By.LINK_TEXT,headline).click()
        driver.switch_to.window(driver.window_handles[-1])
        link = driver.current_url
        news_articles.append(("UPPSC Prepp Official",headline,link))
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        driver.switch_to.frame(driver.find_element(By.TAG_NAME,'iframe'))
    success.append("UPPSC Prepp Official")
except Exception as e:
    failure.append(("UPPSC Prepp Official",e))
    pass

#UPPSC More Prepp Official
try:

    url = 'https://uppsc.up.nic.in/'
    name = 'UPPSC More Prepp Official'
    
    driver.get(url)
    driver.find_element(By.ID,'more').find_element(By.TAG_NAME,'a').click()
    driver.switch_to.window(driver.window_handles[1])
    soup = BeautifulSoup(driver.page_source,'html.parser')
    headlines = soup.find_all('td')
    for line in headlines:
        headline = line['title']
        link = line.find('a')['href']
        if link.startswith('https'):
            link = link
        else:
            link = url + link
        news_articles.append(("UPPSC More Prepp Official",headline,link))
    success.append("UPPSC More Prepp Official")
except Exception as e:
    failure.append(("UPPSC More Prepp Official",e))
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
    data = pd.read_csv('/root/New_Scrapers/Cd_scrapers/cd_main.csv')
    
except:
    pass
data = pd.concat([ data,df])
print("data concatenated")
data.drop_duplicates(subset = ['title'], inplace = True)
data.to_csv('/root/New_Scrapers/Cd_scrapers/cd_main.csv', index = False)
