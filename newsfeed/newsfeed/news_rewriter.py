import pandas as pd


def rewrite_html():
    body, html = "", ""
    beginning_body = """    <section class="section">
            <div class="container">
                <div class="columns is-multiline">"""
    news_info = pd.read_csv(
        "/Users/aowang/715/newsfeed/NewsData/cleaned_news.csv")

    with open("/Users/aowang/715/newsfeed/header.txt", "r") as header, \
            open("/Users/aowang/715/newsfeed/footer.txt", "r") as footer:
        head = header.read()
        foot = footer.read()

    head += beginning_body

    with open("/Users/aowang/715/website/newsFeed.html", "w") as newsFeed:
        for news in news_info.iterrows():
            title, url_link, image_link = news[1][1], news[1][2], news[1][3]

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
