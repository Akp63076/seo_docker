import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup

url = "https://collegedunia.com/exams/jee-main"
req = requests.get(url)
html_doc = req.text

soup = BeautifulSoup(html_doc, 'html.parser')