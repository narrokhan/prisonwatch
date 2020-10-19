import requests
from bs4 import BeautifulSoup
import json
from models import prison, news

input_file = open ('prison.json', "r", encoding="big5")
json_array = json.load(input_file)
#print(json_array)
for item in json_array:
    print("prison_name:" + item['prison_name'])

    url_domain = item['prison_domain_name']
    #====new prison object
    new_prison = prison(prison_name = item['prison_name'],
    prison_domain_name = item['prison_domain_name'],
    prison_BBS = item['prison_BBS'],
    prison_area = item['prison_area'])

    #====
    html = requests.get(item['prison_BBS'])
    soup = BeautifulSoup(html.text,"html5lib")
    post_title = soup.findAll("div",{"class":"list"})
    for post in post_title:
        print( post)
    #	print(post.text,url_domain+post.find("a").get("href"))