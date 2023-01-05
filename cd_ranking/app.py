import requests
import json

data=requests.get("http://178.18.255.188/cd_ranking/category_tag/daily")
print(json.loads(data.text))
