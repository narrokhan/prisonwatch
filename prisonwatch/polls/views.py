from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
import requests
from bs4 import BeautifulSoup
import json
from .models import prison, news
import os
from django.shortcuts import get_object_or_404
import threading
import time

CRAWLER_INIT = 0
CRAWLER_WORKING = 1
crawler_state = CRAWLER_INIT
crawlering_prison_name = ""
crawlering_total_number = 0
crawlering_count_now = 0
COUNT_PER_PAGE = 30 

def index(request):
    global crawler_state
    t = threading.Thread(target = start_crawler)
    t.start()
    return HttpResponse("index")
def return_pollstate(request):
    return HttpResponse("{\"crawlering_prison_name\":\""+str(crawlering_prison_name)+
        "\",\"crawlering_count_now\":"+str(crawlering_count_now)+
        ",\"crawlering_total_number\":"+str(crawlering_total_number)+
        ",\"news_count\":"+str(news.objects.all().count())+"}")

def start_crawler():
    crawler_state = CRAWLER_WORKING
    global crawlering_total_number, crawlering_prison_name ,crawlering_count_now
    input_file = open (os.path.dirname(os.path.realpath(__file__)) +'\\'+'prison.json', "r", encoding="big5")
    json_array = json.load(input_file)
    prison_count = 0
    bbs_count = 0
    get_prison = None
    print("cral start\n")
    for item in json_array:
        #print("prison_name:" + item['prison_name'])
        crawlering_prison_name = item['prison_name']
        url_domain = item['prison_domain_name']
        try: 
        	get_prison = prison.objects.get(prison_name = item['prison_name'])
        	#print(get_prison)
        except prison.DoesNotExist:
    #====new prison object

	        new_prison = prison(
	        prison_name = item['prison_name'],
	        prison_domain_name = item['prison_domain_name'],
	        prison_BBS = item['prison_BBS'],
	        prison_area = item['prison_area']
	        )
	        print("\n new pr\n")

	        
	        new_prison.save()
	        get_prison = new_prison
        except:
        	print("\nsomething happen \n")

        if get_prison == None: #get no prison
        	print("\n\n\n get no prison\n\n\n")
        	continue
        else:
        	prison_count = prison_count + 1
        crawlering_total_number = total_posts = int(get_total_topic(item['prison_BBS'],requests))
        page_count = 0
        crawlering_count_now = 0
        while int(crawlering_count_now) < int(total_posts):
            the_url_of_bbs = item['prison_BBS'] + ("?Page=%d&PageSize=%d&type=" %(page_count+1,COUNT_PER_PAGE))
            #print(the_url_of_bbs)
            page_count = page_count +1
            html = requests.get(the_url_of_bbs) 
            soup_html = BeautifulSoup(html.text,"html5lib")
            post_title = soup_html.findAll("div",{"class":"list"})
            total_posts = get_total_topic(item['prison_BBS'],requests)

            for post in post_title:
                soup_post =  BeautifulSoup(str(post),"html5lib")
                li_tags = soup_post.find_all('li')

                for li_tag in li_tags:
                    soup_li =  BeautifulSoup(str(li_tag),"html5lib")
                    datatimes_tag = soup_li.find_all('time')[0]['datetime']

                    span_tag = soup_li.find_all('span')[0]
                    a_tag = soup_li.find_all('a')[0]
                    a_tag_str = str(a_tag)
                    get_title = a_tag_str.replace(str(span_tag),"")
                    print("time :"+str(datatimes_tag))
                    final_title_soup = BeautifulSoup(str(get_title),"html5lib")
                    final_title = final_title_soup.find_all('a')[0].text
                    print("final_title :"+str(final_title))
                    final_href = item['prison_BBS'] +final_title_soup.find_all('a')[0].get("href")
                    print("final_href="+final_href)
                    news_obj_m = None
                    try:
                        news_obj_m = news.objects.get( topic = str(final_title), prison_related = get_prison ,news_url = final_href)
                    except news.DoesNotExist:
                        get_news = news(
                        topic = str(final_title),
                        post_date = str(datatimes_tag),
                        news_url = final_href,
                        attach_filename = "",
                        news_detail_text = "",
                        prison_related = get_prison
                        )
                        bbs_count = bbs_count + 1
                        get_news.save()
                    else:
                        news_obj_m.topic = str(final_title)
                        news_obj_m.post_date = str(datatimes_tag)
                        news_obj_m.news_url = final_href
                        news_obj_m.prison_related = get_prison
                        news_obj_m.save()



            crawlering_count_now = crawlering_count_now + COUNT_PER_PAGE
    crawlering_count_now = 0
    retstr = "200 OK __Get %d prisons and %d bbs" %(prison_count, bbs_count)
    return HttpResponse(retstr)
def get_total_topic(prison_bbs_url,request):
    html = requests.get(prison_bbs_url)
    soup_html = BeautifulSoup(html.text,"html5lib")
    post_total = soup_html.findAll("div",{"class":"total"})
    total_soup = BeautifulSoup(str(post_total),"html5lib")
    total_tags = total_soup.find_all('span')
    return (str(total_tags[0].text))
def remove_all_bbsnews(request):
    input_file = open (os.path.dirname(os.path.realpath(__file__)) +'\\'+'prison.json', "r", encoding="big5")
    json_array = json.load(input_file)

    for item in json_array:

    	prison_name_v = item['prison_name']
    	probj = prison.objects.filter(prison_name = prison_name_v)[:1]
    	print(news.objects.filter(prison_related = probj).delete())
    	#print(news.objects.filter(prison_name = "").delete())
    	#print(news.objects.filter(prison_name=item['prison_name']))
    	#print(news.objects.filter(prison_name=item['prison_name']).delete())
    news.objects.all().delete()	
    return HttpResponse("remove all prison news")