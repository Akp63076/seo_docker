import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
from datetime import datetime
import csv
from zoneinfo import ZoneInfo
import requests
import os
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

os.chdir("/root/New_Scrapers")
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
# Aglasem-1
try:
    base_url = 'https://news.aglasem.com/'
    agent = {"User-Agent":"Mozilla/5.0"}
    res = requests.get(base_url, headers=agent)
    soup = BeautifulSoup(res.text, 'html.parser')
    newss = soup.find(class_='jeg_posts jeg_load_more_flag').find_all('h3')
    for news in newss:
        headline = news.get_text().strip()
        link = news.find('a').get('href')
        news_articles.append(('Aglasem', headline[:999], link))
    success.append('Aglasem-1')
except Exception as e:
    failure.append(('Aglasem-1', e))
    pass

# Aglasem-2
try:
    base_url = 'https://news.aglasem.com/'
    agent = {"User-Agent":"Mozilla/5.0"}
    res = requests.get(base_url, headers=agent)
    soup = BeautifulSoup(res.text, 'html.parser')
    results = soup.find(class_='jeg_postblock_21').find(class_='jeg_block_container').find_all(class_='jeg_post')
    for result in results:
        headline = result.find('h3').find('a').get_text().strip()[:999]
        link = result.find('h3').find('a').get('href')
        news_articles.append(('Aglasem', headline, link))
    success.append('Aglasem-2')
except Exception as e:
    failure.append(('Aglasem-2', e))
    pass

#Aglasem-3
try:
    base_url = 'https://admission.aglasem.com/'
    agent = {"User-Agent":"Mozilla/5.0"}
    res = requests.get(base_url, headers=agent)
    soup = BeautifulSoup(res.text, 'html.parser')
    newss = soup.find(class_ = 'jeg_posts jeg_load_more_flag').find_all(class_ = 'jeg_postblock_content')
    for news in newss:
        headline = news.find('h3').find('a').get_text()
        link = news.find('h3').find('a').get('href')
        news_articles.append(('Aglasem', headline, link))
    success.append('Aglasem-3')
except Exception as e:
    failure.append(('Aglasem-3', e))
    pass

# Aglasem-4
try:
    base_url = 'https://institutes.aglasem.com/'
    agent = {"User-Agent":"Mozilla/5.0"}
    res = requests.get(base_url, headers = agent)
    soup = BeautifulSoup(res.text, 'html.parser')
    newss = soup.find(class_='jeg_main_content col-sm-8').find_all(class_='jeg_postblock_content')
    for news in newss:
        headline = news.find('a').get_text()
        link = news.find('a').get('href')
        news_articles.append(('Aglasem', headline, link))
    success.append('Aglasem-4')
except Exception as e:
    failure.append(('Aglasem-4',e))
    pass

# BusinessLine On Campus
try:
    base_url = 'https://bloncampus.thehindubusinessline.com/b-school-corner/'
    res = requests.get(base_url)
    soup = BeautifulSoup(res.text, 'html.parser')
    newss = soup.find('div',class_ = 'col-md-5')
    news = newss.find_all('div',class_ = 'nudt2a')
    for i in news:
        box = i.find('h3')
        link = box.find('a').get('href')
        headline = box.text        
    news_articles.append(('BusinessLine On Campus', headline, link))
    success.append('BusinessLine On Campus')
except Exception as e:
    failure.append(('BusinessLine On Campus', e))
    pass


# News.carrers-360
try:
    base_url = 'https://news.careers360.com'
    url = 'https://news.careers360.com/latest?page=1'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    newss = soup.find(class_="artiLis-MainBlock").find_all(class_='heading4')
    for news in newss:
        headline = news.find('a').get_text()
        link = news.find('a').get('href')
        link = base_url+link
        if headline == '':
            continue
        else:
            news_articles.append(('Careers-360', headline[:999], link))
    success.append('Careers-360')
except Exception as e:
    failure.append(('Careers-360', e))
    pass

# College Admission
try:
    base_url = 'https://www.collegeadmission.in/index.shtml'
    res = requests.get(base_url)
    soup = BeautifulSoup(res.text, 'html.parser')
    newss = soup.find('div', {'class':'link_list'}).find_all('li')
    for news in newss:
        headline1 = news.find('span', {'class':'name_list_search'}).find('a').find('br').get_text().strip()[:999]
        try:
            headline2 = news.find('span', {'class':'name_list_search'}).find('a').find('br').next_sibling.strip()
        except:
            pass
        college_name = news.find('span', {'class':'name_list_search'}).find('a').find('span', {'style':'text-decoration:underline; color:#000000; font-style:normal'}).get_text().strip()[:999].encode('ascii', 'ignore').decode("utf-8")
        link = news.find('span', {'class':'name_list_search'}).find('a').get('href')
        if headline1 !='':
            news_articles.append(('College-Admission',headline1+':'+' '+college_name,link))
        else:
            news_articles.append(('College-Admission',headline2+':'+' '+college_name,link))
    success.append('College-Admission')
except Exception as e:
    failure.append(('College-Admission',e))
    pass

# Collegedekho - 1
try:
    base_url = 'https://www.collegedekho.com/news/'
    res = requests.get(base_url)
    soup = BeautifulSoup(res.text, 'html.parser')
    results = soup.find(class_='newslistCol').find_all(class_='box')
    for result in results:
        headline = result.find(class_='image').find('img').get('alt').strip()[:999]
        link = result.find(class_='image').find('a').get('href')
        if headline == '':
            continue
        else:
            news_articles.append(('Collegedekho', headline[:999], link))
    success.append('Collegedekho-1')
except Exception as e:
    failure.append(('Collegedekho-1', e))
    pass
# Collegedekho - 2
try:
    base_url = 'https://www.collegedekho.com/news/'
    res = requests.get(base_url)
    soup = BeautifulSoup(res.text, 'html.parser')
    results = soup.find(class_='news-group-bg').find_all(class_='news-title-new')
    for result in results:
        headline = result.find('a').get_text().strip()[:999]
        link = result.find('a').get('href')
        link = 'https://www.collegedekho.com' + link
        if headline == '':
            continue
        else:
            news_articles.append(('Collegedekho', headline[:999], link))
    success.append('Collegedekho-2')
except Exception as e:
    failure.append(('Collegedekho-2', e))
    pass
# Collegedekho - 3
try:
    base_url = 'https://www.collegedekho.com/news/'
    res = requests.get(base_url)
    soup = BeautifulSoup(res.text, 'html.parser')
    results = soup.find(class_='rightCol').find_all(class_='box')
    for result in results:
        headline = result.find('a').find('img').get('alt').strip()[:999]
        link = result.find('a').get('href')
        if headline == '':
            continue
        else:
            news_articles.append(('Collegedekho', headline[:999], link))
    success.append('Collegedekho-3')
except Exception as e:
    failure.append(('Collegedekho-3', e))
    pass
# Collegedekho - 4
try:
    base_url = 'https://www.collegedekho.com/articles/'
    res = requests.get(base_url)
    soup = BeautifulSoup(res.text, 'html.parser')
    results = soup.find(class_='newslistCol').find_all(class_='box')
    for result in results:
        headline = result.find(class_='image').find('img').get('alt').strip()[:999]
        link = result.find(class_='image').find('a').get('href')
        if headline == '':
            continue
        else:
            news_articles.append(('Collegedekho', headline[:999], link))
    success.append('Collegedekho-4')
except Exception as e:
    failure.append(('Collegedekho-4', e))
    pass
# Collegedekho - 5
try:
    base_url = 'https://www.collegedekho.com/articles/'
    res = requests.get(base_url)
    soup = BeautifulSoup(res.text, 'html.parser')
    results = soup.find(class_='news-group-bg').find_all(class_='news-title-new')
    for result in results:
        headline = result.find('a').get_text().strip()[:999]
        link = result.find('a').get('href')
        link = 'https://www.collegedekho.com' + link
        if headline == '':
            continue
        else:
            news_articles.append(('Collegedekho', headline[:999], link))
    success.append('Collegedekho-5')
except Exception as e:
    failure.append(('Collegedekho-5', e))
    pass
# Collegedekho - 6
try:
    base_url = 'https://www.collegedekho.com/articles/'
    res = requests.get(base_url)
    soup = BeautifulSoup(res.text, 'html.parser')
    results = soup.find(class_='rightCol').find_all(class_='box')
    for result in results:
        headline = result.find('a').find('img').get('alt').strip()[:999]
        link = result.find('a').get('href')
        if headline == '':
            continue
        else:
            news_articles.append(('Collegedekho', headline[:999], link))
    success.append('Collegedekho-6')
except Exception as e:
    failure.append(('Collegedekho-6', e))
    pass

# Hindustan Times
try:
    base_url = 'https://hindustantimes.com/education'
    url = 'https://www.hindustantimes.com/'
    agent = {"User-Agent":"Mozilla/5.0"}
    res = requests.get(base_url, headers = agent)
    soup = BeautifulSoup(res.text, 'html.parser')
    newss = soup.find(id='dataHolder').find_all('h2')
    for news in newss:
        headline = news.find('a').get_text()
        link = url+news.find('a').get('href')
        news_articles.append(('HT', headline, link))
    success.append('HT')
except Exception as e:
    failure.append(('HT', e))
    pass

# Indian-Express-2
try:                                            
    base_url = 'https://indianexpress.com/section/education/'
    res = requests.get(base_url)
    soup = BeautifulSoup(res.text, 'html.parser')
    newss = soup.find(class_='nation').find_all(class_='articles')
    for news in newss:
        headline = news.find(class_='title').find('a').get_text()
        link = news.find(class_='title').find('a').get('href')
        news_articles.append(('Indian-Express', headline[:999], link))
    success.append('Indian-Express-2')
except Exception as e:
    failure.append(('Indian-Express-2', e))
    pass

# JagranJosh
try:                                            
    base_url = 'http://www.jagranjosh.com'
    url = 'https://www.jagranjosh.com/news?source=hp_news'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    newss = soup.find_all(class_='listing')[0].find_all(class_='heading')
    for news in newss:
        link = news.find('a').get('href')
        link = base_url + link
        news_articles.append(('JagranJosh', news.get_text().strip()[:999], link))
    success.append('JagranJosh')
except Exception as e:
    failure.append(('JagranJosh', e))
    pass

#Jagranjosh
try:
    url = 'https://www.jagranjosh.com/news?source=hp_news'
    base_url = 'https://www.jagranjosh.com'
    name = "JAGRANJOSH"

    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    tags = soup.find('ul', class_ = 'listing').find_all('li')
    base_url = 'https://www.jagranjosh.com'
    for tg in tags:
        headline = tg.div.text.replace('\n', '')
        url = tg.div.a.get('href')
        if url.startswith('https'):
            url  = url
        else:
            url = base_url+url
        news_articles.append((name, headline, url))
    success.append(name)
except Exception as e:
    failure.append((name, e))

#Success CDS Admission
try:
    url = 'https://www.successcds.net/admission-notification/index.html'
    name = 'Success CDS Admission'
    content = requests.get(url)
    soup = BeautifulSoup(content.text,'html.parser')
    headlines = soup.find_all('tr',class_='wptb-row',attrs={'style':'background-color: rgb(255, 255, 255);'})[:10]
    for line in headlines:
        headline = line.find_all('td')[0].text + ' ' + line.find_all('td')[1].text
        link = line.find('a')['href']
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

#Success CDS Entrance Exam 
try:
    url = 'https://www.successcds.net/Entrance-Exam/latest-notifications.html'
    name = 'Success CDS Entrance Exam'
    content = requests.get(url)
    soup = BeautifulSoup(content.text,'html.parser')
    headlines = soup.find_all('tr',class_='wptb-row',attrs={'style':'background-color: rgb(255, 255, 255);'})[:10]
    for line in headlines:
        if len(line.find_all('td')[1].text) == 1:
            headline = line.find_all('td')[0].text.replace("\xa0","")
        else:
            headline = line.find_all('td')[0].text + ' ' + line.find_all('td')[1].text.replace("\xa0","")
        link = line.find('a')['href']
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

#Punekar News

try:
    url = 'https://www.punekarnews.in/category/education/'
    name= 'Punekar News'
    content = requests.get(url)
    soup = BeautifulSoup(content.text,'html.parser')
    headlines = soup.find_all('article')
    for line in headlines:
        headline = line.find('h3').find('a').text.strip()
        link = line.find('h3').find('a')['href']
        news_articles.append((name,headline,link))
    success.append(name)
except Exception as e:
    failure.append((name,e))
    pass

# Legally-India
try:   
    url = 'https://www.legallyindia.com'                                       
    base_url = 'https://www.legallyindia.com/lawschools/lawschools/blog'
    res = requests.get(base_url)
    soup = BeautifulSoup(res.text, 'html.parser')
    newss = soup.find(class_='items-leading itemwrap clearfix').find_all('h2')
    for news in newss:
        headline = news.find('a').get_text().strip()
        link = url + news.find('a').get('href')
        news_articles.append(('Legally-India', headline, link))
    success.append('Legally-India')

except Exception as e:
    failure.append(('Legally-India', e))
    pass

# MBA-Universe
try:
    base_url = 'https://www.mbauniverse.com'                                  
    url = 'https://www.mbauniverse.com/7-days-search.php'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    newss = soup.find(class_='view-content').find_all(class_='views-row')
    for news in newss:
        headline = news.find(class_='field-content').get_text()
        link = news.find('a').get('href')
        link = base_url + link
        news_articles.append(('MBA-Universe', headline[:999], link))
    success.append('MBA-Universe')
except Exception as e:
    failure.append(('MBA-Universe', e))
    pass

# Times Now
try:
    base_url = 'https://www.timesnownews.com/education'
    res = requests.get(base_url)
    soup = BeautifulSoup(res.text, 'html.parser')
    main_box = soup.find('div',class_ = 'ArticleList-tnn__grid-holder-21BHe')
    newss = main_box.find_all('a')
    for i in newss:
        headline = i.text
        link = i.get('href')
        if 'http' not in link:
            link = base_url+link
        news_articles.append(('Times Now', headline, link))
    success.append('Times Now')
except Exception as e:
    failure.append(('Times Now', e))
    pass

# Times of India
try:
    base_url = 'https://timesofindia.indiatimes.com'
    url = 'https://timesofindia.indiatimes.com/education'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    newss = soup.find(id='c_wdt_list_1').find('ul').find_all('li')
    for news in newss:
        try:
            headline = news.find('a').get('title')
            link = news.find('a').get('href')
            if headline or link is not None or '':
                link = base_url + link
                news_articles.append(('TOI', headline[:999], link))
        except:
            pass
    success.append('TOI')
except Exception as e:
    failure.append(('TOI', e))
    pass


#RESULT-91
try:
    base_url="http://www.result91.com/h/AllIndiaResults"
    res=requests.get(base_url)
    soup = BeautifulSoup(res.text, 'html.parser')
    university_names=soup.find_all("a",{"class":"list-group-item list-header padleft5"})
    results=soup.find_all("a",{"class":"list-group-item pl35"})
    for university in university_names:
        uni_name=university.find("b").get_text()
        while True:
            if university.find_next("a").get('class') == ['list-group-item', 'pl35']:
                result = university.find_next("a", class_='list-group-item pl35')
                result_name = result.get_text().strip()
                link = result.get('href')
                headline = uni_name +' - '+ result_name
                news_articles.append(('Result-91', headline[:999], link ))
                university = university.find_next("a", class_='list-group-item pl35')
            else:
                break
    success.append('Result-91')
except Exception as e:
    failure.append(('Result-91', e))
    pass

#RK-Alert
# try:
#     base_url="https://rkalert.in/category/admit-card/"
#     res=requests.get(base_url)
#     soup = BeautifulSoup(res.text, 'html.parser')
#     newss=soup.find(id="main").find_all('article')
#     for news in newss:
#         headline=news.find(class_='entry-title').find('a').get_text()
#         link=news.find(class_='entry-title').find('a').get("href")
#         news_articles.append(("RK-Alert", headline[:999], link))
#     success.append('RK-Alert')
# except Exception as e:
#     failure.append(('RK-Alert', e))
#     pass

#PagalGuy
try:
    base_url="https://www.pagalguy.com/articles"
    res=requests.get(base_url)
    soup = BeautifulSoup(res.text, 'html.parser')
    newss=soup.find("section", {"class": "latest-post-selection"}).find_all('article')
    for news in newss:
        headline = news.find('a', {'class':'main-link read-more-wrap'}).get('title').strip()
        link = news.find('a', {'class':'main-link read-more-wrap'}).get('href')
        news_articles.append(("PagalGuy", headline[:999], link))
    success.append('PagalGuy')
except Exception as e:
    failure.append(('PagalGuy', e))
    pass
# Shiksha (new)
# try:
#     url = 'https://www.shiksha.com/articles-all'
#     base_url = 'https://www.shiksha.com'
#     name = "Shiksha"
#     headers = { 'Accept-Language' : 'en-US,en;q=0.9','User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}
#     resp = requests.get(url)
#     soup = BeautifulSoup(resp.text, 'html.parser')
#     tags = soup.find_all('h3', class_ = 'articleTitle')
#     for tg in tags:
#         headline = tg.text.replace('\n', '')
#         url = tg.a.get('href')
#         if url.startswith('https'):
#             url  = url
#         else:
#             url = base_url+url
#         news_articles.append((name, headline, url))
#     success.append(name)
# except Exception as e:
#     failure.append((name, e))
#sarvgyan(1)

def next_page():
    url = 'https://news.sarvgyan.com/education/entrance-exams/'
    urls=[url]
    for i in range(2,6):
        next_url = url.split('page/')[0]+'page/'+str(i)
        urls.append(next_url)
    return urls

urls=next_page()

for url in urls:
    try:
        base_url = "https://news.sarvgyan.com"
        req = requests.get(url)
        # print(req.status_code == 200)
        soup = BeautifulSoup(req.text, "html.parser")
        results = soup.find("div", id="uid_c279").find_all('div', class_='p-content')
        for result in results:
            headline = result.find('a').text.strip()
            link= result.a.get("href").strip()
            news_articles.append(('sarvgyan(1)', headline, link))
        
    except Exception as e:
        failure.append(('sarvgyan(1)',e))
        pass
success.append('sarvgyan(1)')

#sarvgyan(2)

Input = 4            #int(input('Enter no of page to extract : '))
url = 'https://news.sarvgyan.com/education/board-exams/'

for i in range(1,Input+1):
    if i == 1:
        try:
            name = 'sarvgyan(2)'
            content = requests.get(url)
            document = BeautifulSoup(content.text, "html.parser")
            div1 = document.find_all('div',class_="block-inner")
            for div2 in div1:
                div3 = div2.find_all('h3', class_="entry-title")
                for div4 in div3:
                    headline = div4.text.split('–')[0]  # Heading
                    link = div4.find_all('a', href=True)[0]['href']
                    news_articles.append((name, headline, link))
                    # print(name, headline, link)
            success.append(name)
        except Exception as e:
            failure.append((name, e))
            pass
    else:
        try:
            content = requests.get('https://news.sarvgyan.com/education/board-exams/page/'+str(i)+'/')
            document = BeautifulSoup(content.text, "html.parser")
            div1 = document.find_all('div', class_="block-inner")
            for div2 in div1:
                div3 = div2.find_all('h3', class_="entry-title")
                for div4 in div3:
                    headline = div4.text.split('–')[0]  # Heading
                    link = div4.find_all('a', href=True)[0]['href']
                    news_articles.append((name, headline, link))
                    # print(news_articles)
            
        except Exception as e:
            failure.append((name, e))
            pass
success.append(name)
#sarvgyan(3)

try:
    url='https://news.sarvgyan.com/education/universities-colleges/'
    req= requests.get(url)
    # print(req.status_code==200)
    soup = BeautifulSoup(req.text, 'html.parser')
    results=soup.find('div', id='uid_c334')
    for res in results:
        var = res.find_all('div', class_ = 'p-content')
        for v in var:
            headline=v.find('a').text
            link = v.find('a').get('href').strip()
            news_articles.append(('sarvgyan(3)', headline, link))
    success.append('sarvgyan(3)')
except Exception as e:
    failure.append(('sarvgyan(3)',e))
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
