<div align="center">
    <image src="website/icons/android-chrome-192x192.png">
</div>

# Ceres 

![AppVeyor](https://img.shields.io/appveyor/build/gruntjs/grunt)![Ceres](svg_badge/ceres-v2.7-blue.svg) [![Licence](svg_badge/licence-MIT-blue.svg)](https://choosealicense.com/licenses/mit/) ![python](svg_badge/python-v3.7.3-blue.svg)

 

Ceres is a web application dedicated to promoting and bringing awareness to the Austrailian bushfires. The web application includes daily map visualization and statistics of the bushfires, monthly news letters, and live twitter feed.

It started out as a freshman design project by Hung Do, Joey Huang, EJ Roberts, and Ao Wang and has been in development since early January 2020. 

## Table of Content
+ [Technologies Used](#tech-used)
+ [Installation](#install)
+ [How Does it Work?](#how)
+ [User Manual](#user-man)
+ [System Manual](#sys-man)
+ [Contributing ](#contrib)
+ [License](#license)


## Features

To get a complete list of supported features, please visit our [website](https://tinyurl.com/rucere-ious).

<div id="tech-used"></div>

## Technologies Used

### Front-end 

* HTML
* CSS
* JavaScript
* [Bulma](https://bulma.io/) - CSS Framework

### Back-end

* Python
* Pandas

### Automation

* Google Cloud Platform: 
    - [Compute Engine](https://cloud.google.com/compute)
    - [Storage Buckets](https://cloud.google.com/compute/docs/disks/gcs-buckets)

### Data Collection
* [News API](https://newsapi.org/) - A JSON API for live news and blog articles
* [Twitter API](https://python-twitter.readthedocs.io/en/latest/) 
* [NASA's Satellite Data](https://firms.modaps.eosdis.nasa.gov/active_fire/#firms-txt)

<div id="install"></div>

## Installation

Cloning the repo:

``` bash
git clone git@github.com:ow-wow-wang/ceres.git
```

Use the package manager [pip](https://pip.pypa.io/en/stable/) to download Python libraries:

``` bash
pip install -r requirements.txt
```

<div id="how"></div>

## How does it work?
Ceres web scraps bushfire data from NASA's sensors, cleans the false positives' data and plots them onto the map. There's also a statistics portion where Ceres counts the fires for each of Australia's regions and measures the distribution of Fire Radiative Power (FRP). This process occurs twice a day.

Additionally, Ceres has a charity page to many, reputable charities trying to fight the fire and support Australia's people and wildlife. 

But one of Ceres' goals is also to maintain the awareness of the bushfires, which is why we added a News Feed and Twitter Feed, gathering links using Python's News and Twitter API. The new news articles are shown every month and continually updating Twitter Feed. 

<div id="user-man"></div>

## User Manual

* [User Manual](https://gitlab.cci.drexel.edu/fds20/715/-/wikis/User-Manual)

<div id="sys-man"></div>

## Systems Manual

* [Systems Manual](https://gitlab.cci.drexel.edu/fds20/715/-/wikis/System-Manual)

<div id="contrib"></div>

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please take a look at our [contributing](CONTRIBUTING.md) guidelines if you're interested in helping!

## Contributers

  + Hung Do ([hd386@drexel.edu](hd386@drexel.edu))
  + Joey Huang ([jh3759@drexel.edu](jh3759@drexel.edu))
  + EJ Roberts ([ejr89@drexel.edu](ejr89@drexel.edu))
  + Ao Wang ([aw3338@drexel.edu](aw3338@drexel.edu))

<div id="license"></div>

## License

  + [MIT](https://choosealicense.com/licenses/mit/)

## Acknowledgements

  + Our TA's for their endless support
  + Dr. Pirmann and the other Freshmen Design Sequence professors for their guidance
