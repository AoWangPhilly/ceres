from newsapi import NewsApiClient
import datetime as dt
import json
import requests

newsapi = NewsApiClient(api_key='0f23c49de41b405b863c7f6653a2cf73')

url = ('http://newsapi.org/v2/everything?'
       'q=australia bushfire&'
       'sources=bbc-news&'
       'from=2020-01-24&'
       'sortBy=popularity&'
       'apiKey=0f23c49de41b405b863c7f6653a2cf73')
response = requests.get(url)
the_news = response.json()

with open('bbcnewsjan24.json', 'w') as json_file:
    json.dump(the_news, json_file)