import folium
from folium.plugins import HeatMapWithTime
import pandas as pd
import requests
from bs4 import BeautifulSoup
import schedule
import time
import datetime
import subprocess

def retrieve_data(country, sensor, time):
    """Webscrapes the NASA website for the wildfire data
    
    Args:
        country (str): The name of the country in title case
        sensor (str): The name of the sensor, like MODIS or VIIRS
        time (str): The timeframe of the data (24h, 48h, 7d)
        
    Returns:
        str: The link of the CSV file
    """
    index = 0
    url = "https://firms.modaps.eosdis.nasa.gov/active_fire/#firms-txt"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    a_tag = soup.findAll("a")
    a_tag_string = [str(i) for i in a_tag]
    for idx in range(len(a_tag_string)):
        if country in a_tag_string[idx] and\
           time in a_tag_string[idx] and\
           "csv" in a_tag_string[idx] and\
           sensor in a_tag_string[idx]:
            index = idx
            break
    link = a_tag[index]["href"]
    download_url = "https://firms.modaps.eosdis.nasa.gov" + link
    return download_url

def high_confidence(m, v, n):
    """Drops all the coordinates that are less than 80% confidence and low confidence
    """
    m = m[m.confidence > 80].drop_duplicates()
    v = v[(v.confidence == "nominal") | (v.confidence == "high")].drop_duplicates()
    n = n[(n.confidence == "high") | (n.confidence == "high")].drop_duplicates()
    return m, v, n

def combine_data_sets(df):
    """Combinates the three data frames."""
    all_df = []
    for i in range(3):
        all_df.append(df[i][["latitude", "longitude", "acq_date"]])
    return pd.concat(all_df)

def get_week_time_coordinates(df):
    week = []
    times = [str(i) for i in df["acq_date"].drop_duplicates()]
    start = 0
    for i in range(len(times)):
        end = df.index[df.acq_date == times[i]][len(df.index[df.acq_date == times[i]])-1] + 1
        df1 = df.iloc[start:end][["latitude", "longitude"]]
        day1 = [[df1.iloc[j][0],df1.iloc[j][1]] for j in range(len(df1))]
        week.append(day1)
        start = end
    return week, times


# Creates the map focusing on Australia
m = folium.Map(location=[-28.2744, 135.7751], zoom_start=4.5, tiles="CartoDB dark_matter")

def plot_to_map(wild_fire_df):
    """Plots all the points to the map
    
    Args:
        wild_fire_df (pandas.core.frame.DataFrame): The wildfire dataset 
    Returns:
        None
    """
    b = wild_fire_df[[
        col for col in wild_fire_df.columns if "bright" in col][0]]
    for lat, lon, inten in zip(
            wild_fire_df.latitude, wild_fire_df.longitude, wild_fire_df.frp):
        folium.Circle(
            location=[lat, lon],
            radius=inten,
            color="crimson",
            fill=True
        ).add_to(m)


def add_nav_bar(references, title):
    """Adds the navigation bar"""
    with open("/Users/aowang/ceres/australia_map.html") as mapping:
        txt = mapping.read()
        soup = BeautifulSoup(txt, features="lxml")

    new_link = soup.new_tag("link", rel="stylesheet", href="main.css")
    add_body, unlisted = soup.new_tag("body"), soup.new_tag("ul")
    taggings, listings = [], []

    for hyper in references:
        taggings.append(soup.new_tag("a", href=hyper))
    lists = [soup.new_tag("li") for i in range(len(references))]
    
    for i, string in enumerate(title):
        taggings[i].string = string
        
    for i, tags in enumerate(taggings):
        lists[i].append(tags)
        
    for l in lists:
        unlisted.append(l)

    add_body.append(unlisted)
    soup.head.append(new_link)
    soup.head.append(add_body)
    with open("/Users/aowang/ceres/australia_map.html", "w") as outf:
        outf.write(str(soup))


def remove_zoom():
    """Removes the zoom buttons on webpage"""
    with open("/Users/aowang/ceres/australia_map.html") as mapping:
        txt = mapping.read()
        txt = txt.replace("zoomControl: true", "zoomControl: false")
    with open("/Users/aowang/ceres/australia_map.html", "w") as outf:
        outf.write(txt)

# The git command for Python were from:
# https://www.ivankrizsan.se/2017/03/19/interacting-with-github-using-python/


def execute_shell_command(cmd, work_dir):
    """Executes a shell command in a subprocess, waiting until it has completed.

    :param cmd: Command to execute.
    :param work_dir: Working directory path.
    """
    pipe = subprocess.Popen(
        cmd,
        shell=True,
        cwd=work_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    (out, error) = pipe.communicate()
    print(out, error)
    pipe.wait()


def git_commit(commit_message, repo_dir):
    """Commits the Git repository located in supplied repository directory with the supplied commit message.

    :param commit_message: Commit message.
    :param repo_dir: Directory containing Git repository to commit.
    """
    cmd = 'git commit -am "%s"' % commit_message
    execute_shell_command(cmd, repo_dir)


def git_push(repo_dir):
    """Pushes any changes in the Git repository located in supplied repository directory to remote git repository.

    :param repo_dir: Directory containing git repository to push.
    """
    cmd = 'git push '
    execute_shell_command(cmd, repo_dir)

# add try and except for the HTTPS error
# and keep on trying till it web scrapes the data
def main():
    """Updates the map daily at 10 AM. Different colors represent the different satellite.
    """
    print("Folium version:", folium.__version__)  # 0.10.1
    references = ["map.html", "News", "Page.html", "Donation", "homepage.html"]
    tabs = ["Map", "News", "Charities", "Donations", "About"]
    
    wild_fire_noaa_df = pd.read_csv(retrieve_data("Australia", "noaa", "7d"))
    wild_fire_viirs_df = pd.read_csv(retrieve_data("Australia", "viirs", "7d"))
    wild_fire_modis_df = pd.read_csv(retrieve_data("Australia", "MODIS", "7d"))
    
    high_c = high_confidence(wild_fire_modis_df, wild_fire_viirs_df, wild_fire_noaa_df)
    main_df = combine_data_sets(high_c)
    main_df.to_csv("main_df.csv")
    formatted = get_week_time_coordinates(main_df)
    HeatMapWithTime(formatted[0], formatted[1]).add_to(m)
    m.save("/Users/aowang/ceres/australia_map.html")
    #add_nav_bar(references, tabs)
    #remove_zoom()
    git_commit("Update map", "/Users/aowang/ceres/")
    git_push("/Users/aowang/ceres/")
    print("Done!", datetime.datetime.now())
    

print("Running...")
schedule.every(2).hours.do(main) # currently every two hours
while True:
    schedule.run_pending()
    time.sleep(1)