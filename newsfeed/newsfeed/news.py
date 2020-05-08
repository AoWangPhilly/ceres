from newsapi import NewsApiClient  # imports the NewsApiClient from newsapi
import datetime as dt  # imports datetime to format date and time
import pandas as pd
import json
import requests
import schedule
import time
import os
from news_rewriter import *
newsapi = NewsApiClient(
    api_key='0f23c49de41b405b863c7f6653a2cf73')  # unique key


def clean_data(df_news):
    df_news.drop_duplicates(subset="title", keep=False,
                            inplace=True)  # removes repeat news
    cleaned_news = df_news[['title', 'url', 'urlToImage']]
    cleaned_news.to_csv("/Users/aowang/715/newsfeed/NewsData/cleaned_news.csv")


def retrieve():
    print("Collecting data...")
    url = ('http://newsapi.org/v2/everything?'  # top headlines are retrieved
           'q=australia bushfire&'  # must be relevant to australia bushfires
           'sortBy=popularity&'  # sorted by popularity
           'apiKey=0f23c49de41b405b863c7f6653a2cf73')  # uses the unique key
    response = requests.get(url)  # URLs are retrieved
    the_news = response.json()

    # JSON file is created with all the URLs and information
    with open('/Users/aowang/715/newsfeed/NewsData/wildfirenews.json', 'w') as json_file:
        json.dump(the_news, json_file)

    # Retrieves JSON can turns into Pandas DataFrame
    with open('/Users/aowang/715/newsfeed/NewsData/wildfirenews.json', 'r') as json_file:
        df_news = pd.DataFrame(json.load(json_file)["articles"])

    print("Cleaning data...")
    # Cleans data for repeats and grabbing only title, url, and image url
    clean_data(df_news)

#     with open('archive.csv', 'a') as f: # adding to an archive csv file, does not account for duplicates
#         df.to_csv(f, header=False)

    print("Almost there...")
    # Takes the data and substiutes the links and titles from previous
    rewrite_html()

    print("Done! At {}".format(dt.datetime.now()))
    print("Number of articles: {}".format(len(df_news)))


print("""                                                                                              
,--.  ,--.    ,------.     ,------. ,------.  ,-----.  ,----.   ,------.   ,---.  ,--.   ,--. 
|  ,'.|  |    |  .---'     |  .--. '|  .--. ''  .-.  ''  .-./   |  .--. ' /  O  \ |   `.'   | 
|  |' '  |    |  `--,      |  '--' ||  '--'.'|  | |  ||  | .---.|  '--'.'|  .-.  ||  |'.'|  | 
|  | `   |.--.|  |`.--.    |  | --' |  |\  \ '  '-'  ''  '--'  ||  |\  \ |  | |  ||  |   |  | 
`--'  `--''--'`--' '--'    `--'     `--' '--' `-----'  `------' `--' '--'`--' `--'`--'   `--' 
                                                                                              """)

schedule.every(3).weeks.do(retrieve)  # scheduled for every 3 weeks
while True:
    schedule.run_pending()
    time.sleep(1)
