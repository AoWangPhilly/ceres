"""
Latest update: Refactor the code and encapsulate header and footer to separate text files
Version: 2.9
lab section: 071
date: 06/04/2020
names: EJ Roberts, Ao Wang
description: Retrieves tweets and displays them on webpage
"""

from twitter import *
from requests_oauthlib import OAuth1Session

# README
# Must have python-twitter and OAuth1Session installed
# Must have an already present twitterFeed.html file in the same directory as the script


# Change these keys to be your own through Twitter's developer website
api = api.Api(consumer_key='PK1sz4xtGw7NI1czSurpxqjwg',
              consumer_secret='7yB9oscUnnVuvWJXdNVAfb9Fkt1S4ndOb01JVcyUKFZlq6Cvbp',
              access_token_key='1067122097674170368-B2NXOdXqyFIY1qEskfsBHkOMvSjYJr',
              access_token_secret='WQdb3bL4FTg1K93AGZmb4aIqm7dWo5pBQMoy0QDI4kwmb')
# Edit the query below for your refined search
# Check twitter developer site for query terms
# Change count=X term for number of tweets and %23X for the search term (%23 = #)
results = api.GetSearch(
    raw_query='q=%23bushfires%20&result_type=recent&since=2014-07-19&count=25')
# Original Results
print('FIRST RESULTS: {}'.format(results))
# This checks for tweets with duplicate text and effectively removes retweets
# Uses toBeRemoved list to determine what to remove and how many times to remove that occurence
toBeRemoved = []
for result in results:
    firstOccurence = True
    for result2 in results:
        if result.text == result2.text:
            if firstOccurence:
                firstOccurence = False
            else:
                print('{} was removed'.format(result2.id))
                toBeRemoved.append(result2.id)
if len(toBeRemoved) != 0:
    for resultID in toBeRemoved:
        for result2 in results:
            if resultID == result2.id:
                results.remove(result2)
# Prints results after removing retweets
print('SECOND RESULTS: {}'.format(results))
wholeHtml = ''
# Writes the header of the page and everything before the tweeted content
with open("website/python/header.txt") as header:
    wholeHtml += header.read()

# Writes the tweeted content in cards, each tweet has its own card
# Generates one card per tweet
f = open("twitterFeed.html", "a")
for result in results:
    print(api.GetStatusOembed(result.id))
    preEmbed = '{}'.format(
        api.GetStatusOembed(result.id)['html'].encode('ascii', 'replace'))
    resulting = preEmbed[2:]
    resulting = resulting[:-3]
    resulting = resulting.replace('</blockquote>\\n', '</blockquote>')
    twitterCard = '''<div class="column is-one-third">
                            <figure class="image is-fit">
                                <div class="content">
                                        <div class="content-overlay"></div>
                                        <div class="content-details fadeIn-top">
                                            <h3>{}</h3>
                                        </div>
                                </div>
                            </figure>
                        </div>'''.format(resulting)
    wholeHtml += twitterCard
# Writes the footer and rest of the page
with open("website/python/footer.txt") as footer:
    wholeHtml += footer.read()

# Writes the html file into twitterFeed.html
with open("twitterFeed.html", "w") as html:
    html.write(wholeHtml)
