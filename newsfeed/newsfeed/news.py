# retrieves URLs and puts them into a JSON file to be used to display in a news feed

from newsapi import NewsApiClient # imports the NewsApiClient from newsapi
import datetime as dt # imports datetime to format date and time
import json
import requests

newsapi = NewsApiClient(api_key='0f23c49de41b405b863c7f6653a2cf73') # unique key

url = ('http://newsapi.org/v2/everything?' # different parameters for URLs retrieved 
       'q=australia bushfire&' # has to pertain to the australia bushfire
       'sources=bbc-news&' # has to be from BBC news
       'from=2020-01-24&' # has to be after January 24, 2020
       'sortBy=popularity&' # sorted by popularity
       'apiKey=0f23c49de41b405b863c7f6653a2cf73') # uses the unique key
response = requests.get(url) # URLs are retrieved
the_news = response.json()

with open('bbcnewsjan24.json', 'w') as json_file: # JSON file is created with all the URLs and information
    json.dump(the_news, json_file)