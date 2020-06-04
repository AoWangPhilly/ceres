"""
course: CI103
lab section: 071
date: 05/21/2020
name: Ao Wang, Joey Huang, Hung Do
description: The script is the runner, cleaning the news articles to duplicates and rewrites the news feed HTML page.
"""

from newsapi import NewsApiClient  # imports the NewsApiClient from newsapi
import datetime as dt  # imports datetime to format date and time
import time
import pandas as pd
import json
import requests
import schedule
from NewsRewriter import *
from GitCommand import AutomateCommit

newsapi = NewsApiClient(
    api_key='0f23c49de41b405b863c7f6653a2cf73')  # unique key


def clean_data(df_news):
    """The function removes duplicate article titles and saves it as a CSV file.

    :param df_news: the unclean news feed data frame
    :type df_news: pandas.DataFrame
    """
    df_news.drop_duplicates(subset="title", keep=False,
                            inplace=True)  # removes repeat news
    cleaned_news = df_news[['title', 'url', 'urlToImage']]
    cleaned_news.to_csv(
        "/home/aow252/ceres-bucket-1/ceres/newsfeed/NewsData/cleaned_news.csv")


def runGit():
    # Initialize the object to run git commands
    command = AutomateCommit(commit_message="Retrieve new articles",
                             repo_dir="/home/aow252/ceres-bucket-1/ceres/")
    command.git_commit()
    command.git_push()


def retrieve():
    """Collects the JSON file from the NewsAPI, cleans it, and rewrites the HTML"""

    print("Collecting data...")
    url = ('http://newsapi.org/v2/everything?'  # top headlines are retrieved
           'q=australia bushfire&'  # must be relevant to australia bushfires
           'sortBy=popularity&'  # sorted by popularity
           'apiKey=0f23c49de41b405b863c7f6653a2cf73')  # uses the unique key
    response = requests.get(url)  # URLs are retrieved
    the_news = response.json()

    # JSON file is created with all the URLs and information
    with open('/home/aow252/ceres-bucket-1/ceres/newsfeed/NewsData/wildfirenews.json', 'w') as json_file:
        json.dump(the_news, json_file)

    # Retrieves JSON can turns into Pandas DataFrame
    with open('/home/aow252/ceres-bucket-1/ceres/newsfeed/NewsData/wildfirenews.json', 'r') as json_file:
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

    runGit()  # Commits and pushes new articles


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
