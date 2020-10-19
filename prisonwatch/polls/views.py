from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
import requests
from bs4 import BeautifulSoup
import json
from .models import prison, news
import os
from django.shortcuts import get_object_or_404


def index(request):
    return ("index")
def start_crawler(request):
    input_file = open (os.path.dirname(os.path.realpath(__file__)) +'\\'+'prison.json', "r", encoding="big5")
    json_array = json.load(input_file)
    prison_count = 0
    bbs_count = 0
    get_prison = None
    print("cral start\n")
    for item in json_array:
        #print("prison_name:" + item['prison_name'])
        url_domain = item['prison_domain_name']
        try: 
        	get_prison = prison.objects.get(prison_name = item['prison_name'])
        	print(get_prison)
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

        html = requests.get(item['prison_BBS'])
        soup_html = BeautifulSoup(html.text,"html5lib")
        post_title = soup_html.findAll("div",{"class":"list"})

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
            	print("a_tag"+str(a_tag))
            	print("span_tag "+str(span_tag))
            	print("time :"+str(datatimes_tag))
            	print("get_title "+str(get_title))
            	final_title_soup = BeautifulSoup(str(get_title),"html5lib")
            	final_title = final_title_soup.find_all('a')[0].text
            	print("final_title :"+str(final_title))

            	#continue
            	try:
            		news.objects.get( topic = str(final_title), prison_related = get_prison)
            	except news.DoesNotExist:
	                get_news = news(
	                    topic=str(final_title),
	                    post_date=str(datatimes_tag),
	                    news_url="",
	                    attach_filename="",
	                    news_detail_text="",
	                    prison_related=get_prison
	                )
	                bbs_count = bbs_count + 1
	                get_news.save()

    retstr = "200 OK __Get %d prisons and %d bbs" %(prison_count, bbs_count)
    return HttpResponse(retstr)

def remove_all_bbsnews(request):
    input_file = open (os.path.dirname(os.path.realpath(__file__)) +'\\'+'prison.json', "r", encoding="big5")
    json_array = json.load(input_file)

    for item in json_array:

    	prison_name_v = item['prison_name']
    	probj = prison.objects.filter(prison_name = prison_name_v)[:1]
    	print("\n\n\n\n ooooo \n\n\n")
    	print(news.objects.filter(prison_related = probj).delete())
    	#print(news.objects.filter(prison_name = "").delete())
    	#print(news.objects.filter(prison_name=item['prison_name']))
    	#print(news.objects.filter(prison_name=item['prison_name']).delete())
    news.objects.all().delete()	
    return HttpResponse("remove all prison news")