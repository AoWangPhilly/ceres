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
results = api.GetSearch(raw_query='q=%23bushfires%20-filter:retweets&result_type=recent&since=2014-07-19&count=10')
wholeHtml = ''

# Writes the header of the page and everything before the tweeted content
with open("website/python/header.txt") as header:
    wholeHtml += header.read()

# Writes the tweeted content in cards, each tweet has its own card
# Generates one card per tweet
for result in results:
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
    wholeHtml+=twitterCard

# Adds the footer and rest of the page
with open("website/python/footer.txt") as footer:
    wholeHtml += footer.read()

# Writes the html file into twitterFeed.html
with open("twitterFeed.html", "w") as html:
    html.write(wholeHtml)

