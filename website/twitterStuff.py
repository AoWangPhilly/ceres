from twitter import *
from requests_oauthlib import OAuth1Session

# Change these keys to be your own through Twitter's developer website
api = api.Api(consumer_key='PK1sz4xtGw7NI1czSurpxqjwg',
              consumer_secret='7yB9oscUnnVuvWJXdNVAfb9Fkt1S4ndOb01JVcyUKFZlq6Cvbp',
              access_token_key='1067122097674170368-B2NXOdXqyFIY1qEskfsBHkOMvSjYJr',
              access_token_secret='WQdb3bL4FTg1K93AGZmb4aIqm7dWo5pBQMoy0QDI4kwmb')
# Edit the query below for your refined search
# Check twitter developer site for query terms
results = api.GetSearch(raw_query='q=%23bushfires%20&result_type=recent&since=2014-07-19&count=10')
wholeHtml = ''
f = open("twitterFeed.html", "w")
f.write('''<html>

<head>
    <link rel="apple-touch-icon" sizes="180x180" href="icons/apple-touch-icon.png">
    <link rel="icon" type="image/png" sizes="32x32" href="icons/favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="16x16" href="icons/favicon-16x16.png">
    <link rel="manifest" href="/site.webmanifest">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta charset="utf-8">
    <link href="https://fonts.googleapis.com/css?family=Great+Vibes|Spartan&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css?family=Raleway&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.8.0/css/bulma.min.css">
    <link rel="stylesheet" href="css/newsfeed.css">
    <link rel="stylesheet" href="css/main.css">
    <link rel="stylesheet" href="css/scrollbar.css">
    <link href="https://fonts.googleapis.com/css?family=Manrope&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="css/footer.css">
    <script src="jquery-3.4.1.min.js"></script>
    <script defer src="https://use.fontawesome.com/releases/v5.3.1/js/all.js"></script>
    <script src="js/newsfeed.js"></script>
    <script src="js/dropdown.js"></script>
    <title>Twitter Feed</title>

</head>

<body>
    <section class="hero is-warning is-bold is-small">
        <div class="hero-head">
            <nav class="navbar">
                <div class="container">
                    <div class="navbar-brand">
                        <a href="home.html" class="navbar-item">
                            <p style="font-size: 2rem; font-family: Great Vibes">Ceres</p>
                            <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/Ceres_symbol.svg/1024px-Ceres_symbol.svg.png" class="image">
                        </a>
                        <a role="button" class="navbar-burger" data-target="navMenu" aria-label="menu" aria-expanded="true">
                            <span aria-hidden="true"></span>
                            <span aria-hidden="true"></span>
                            <span aria-hidden="true"></span>
                        </a>
                    </div>

                    <div class="navbar-menu navbar-end" id="navMenu">
                        <a href="home.html" class="navbar-item">
                            Home
                        </a>
                        <a href="charity.html" class="navbar-item">
                            Charities
                        </a>
                        <a href="map.html" class="navbar-item">
                            Map
                        </a>
                        <a href="mapinfo.html" class="navbar-item">
                            Map Information
                        </a>
                        <a href="newsFeed.html" class="navbar-item">
                            News Feed
                        </a>
						<a href="wildfirestats.html" class="navbar-item">
							Bushfire Statistics                            
						</a>
                        <a href="meetTheTeam.html" class="navbar-item">
                            Meet the Team
                        </a>
                        <a href="twitterFeed.html" class="navbar-item is-active">
                            <img src="https://i.ya-webdesign.com/images/twitter-png-black-8.png" class="image">
                        </a>
                        <a href="privacyPolicy.html" class="navbar-item">
                                Privacy
                        </a>
                        <span class="navbar-item">
                            <a href="https://github.com/ow-wow-wang/ceres" class="button is-inverted">
                                <span class="icon">
                                    <i class="fab fa-github"></i>
                                </span>
                                <span>Download</span>
                            </a>
                        </span>

                    </div>
                </div>
            </nav>
        </div>
        <div class="hero-body">
            <div class="container has-text-centered">
                <h1 style="font-size: 60px; font-family: 'Raleway', sans-serif;" class="title has-text-black-ter">
                    Twitter Feed
                </h1>
            </div>
        </div>
    </section>    <section class="section">
            <div class="container">
                <div class="columns is-multiline">"''')
f.close()
f = open("twitterFeed.html", "a")
for result in results:
    print(api.GetStatusOembed(result.id))
    resulting = '{}'.format(
        api.GetStatusOembed(result.id)['html'].encode('ascii', 'replace'))
    f.write('''\n<div class="column is-one-third">
                            <figure class="image is-fit">
                                <div class="content">
                                        <div class="content-overlay"></div>
                                        <div class="content-details fadeIn-top">
                                            <h3>{}</h3>
                                        </div>
                                </div>
                            </figure>
                        </div>'''.format(resulting))
    print('twitter.com/i/web/status/{}'.format(result.id))
f.write('''</div>
            </div>
        </section>   <footer class="footer">
        <div align="center">
            <div class="container is-widescreen">
                <div class="columns">
                    <div class="column">
                        <p id="icons"><a href="home.html"><img src="icons/home.png"></a></p>
                    </div>
                    <div class="column">
                        <p id="icons"><a href="map.html"><img src="icons/map.png"></a></p>
                    </div>
                    <div class="column">
                        <p id="icons"><a href="newsFeed.html"><img src="icons/news.png"></a></p>
                    </div>
                    <div class="column">
                        <p id="icons"><a href="twitterFeed.html"><img src="icons/twitter.png"></a></p>
                    </div>
                    <div class="column">
                        <p id="icons"><a href="meetTheTeam.html"><img src="icons/about.png"></a></p>
                    </div>
                </div>
            </div>
            <p>&nbsp;&nbsp;</p>
            <p id="footerInfo">The source code is licensed <a href="http://opensource.org/licenses/mit-license.php"
                id="links">MIT</a>. <br>
            Bulma by <a href="https://jgthms.com" id="links">Jeremy Thomas</a>.</p>
        </div>
    </footer>
</body>

</html>
''')
f.close()
