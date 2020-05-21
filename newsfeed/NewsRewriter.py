"""
course: CI103
lab section: 071
date: 05/21/2020
contributors: Ao Wang, Joey Huang, Hung Do
description: The module holds methods that help rewrite the news feed page. 
"""


import pandas as pd


def rewrite_html():
    """The function rewrites the news feed page by pulling the new CSV file and replacing the old URL and image links with 
       more relevant news."""

    body, html = "", ""
    beginning_body = """    <section class="section">
            <div class="container">
                <div class="columns is-multiline">"""

    # Reads in the URL's as a Pandas DataFrame
    news_info = pd.read_csv(
        "/home/aow252/ceres-bucket-1/ceres/newsfeed/NewsData/cleaned_news.csv")

    # Reads in the HTML header and footer in a seperate textfile
    with open("/home/aow252/ceres-bucket-1/ceres/newsfeed/header.txt", "r") as header, \
            open("/home/aow252/ceres-bucket-1/ceres/newsfeed/footer.txt", "r") as footer:
        head = header.read()
        foot = footer.read()

    head += beginning_body

    # Rewriting the HTML file
    with open("/home/aow252/ceres-bucket-1/ceres/website/newsFeed.html", "w") as newsFeed:

        # Loops through news dataframe to retrieve the news aricle's title, URL, and image URL
        for news in news_info.iterrows():
            title, url_link, image_link = news[1][1], news[1][2], news[1][3]

            # HTML and Bulma CSS to create the grids/columns
            news_part = """                <div class="column is-one-third">
                            <figure class="image is-fit">
                                <div class="content">
                                    <a href="{}">
                                        <div class="content-overlay"></div>
                                        <img class="content-image" src="{}">
                                        <div class="content-details fadeIn-top">
                                            <h3>{}</h3>
                                        </div>
                                    </a>
                                </div>
                            </figure>
                        </div>\n""".format(url_link, image_link, title)

            body += news_part
        body += """            </div>
            </div>
        </section>"""
        html += head + body + foot
        newsFeed.write(html)
