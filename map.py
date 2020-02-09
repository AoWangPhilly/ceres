import folium
import pandas as pd
import requests
from bs4 import BeautifulSoup
import schedule
import time
import datetime
import subprocess


def retrieve_data(country, satellite):
    """Webscrapes from the nasa website for the 24 csv files
    """
    index = 0
    url = "https://firms.modaps.eosdis.nasa.gov/active_fire/#firms-txt"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    a_tag = soup.findAll("a")
    a_tag_string = [str(i) for i in a_tag]
    for idx in range(len(a_tag_string)):
        if country in a_tag_string[idx] and\
           "24h" in a_tag_string[idx] and\
            "csv" in a_tag_string[idx] and\
                satellite in a_tag_string[idx]:
            index = idx
            break
    link = a_tag[index]["href"]
    download_url = "https://firms.modaps.eosdis.nasa.gov/" + link
    return download_url


# Creates the map focusing on Australia
m = folium.Map(location=[-28.2744, 135.7751], zoom_start=4.5)


def plot_to_map(wild_fire_df, fill_in_color, stamp):
    """Plots all the points to the map
    """
    b = wild_fire_df[[
        col for col in wild_fire_df.columns if "bright" in col][0]]
    for lat, lon, inten in zip(
            wild_fire_df.latitude, wild_fire_df.longitude, b):
        folium.Circle(
            location=[lat, lon],
            popup="{} - Brightness: {}".format(stamp, inten),
            radius=inten,
            color=fill_in_color,
            fill=True,
            fill_color=fill_in_color
        ).add_to(m)


def add_nav_bar():
    """Adds the navigation bar"""
    with open("/Users/aowang/ceres/australia_map.html") as mapping:
        txt = mapping.read()
        soup = BeautifulSoup(txt)

    new_link = soup.new_tag("link", rel="stylesheet", href="main.css")
    hrefs = ["map.html", "News", "Page.html", "Donation", "homepage.html"]
    strings = ["Map", "News", "Charities", "Donations", "About"]

    add_body = soup.new_tag("body")
    unlisted = soup.new_tag("ul")
    taggings, listings = [], []

    for hyper in hrefs:
        taggings.append(soup.new_tag("a", href=hyper))
    lists = [soup.new_tag("li") for i in range(len(hrefs))]
    for i, string in enumerate(strings):
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


def main():
    """Updates the map daily at 10 AM. Different colors represent the different satellite.
    """
    print("Folium version:", folium.__version__)  # 0.10.1
    wild_fire_noaa_df = pd.read_csv(retrieve_data("Australia", "noaa-20"))
    wild_fire_viirs_df = pd.read_csv(retrieve_data("Australia", "viirs"))
    wild_fire_modis_df = pd.read_csv(retrieve_data("Australia", "MODIS"))
    plot_to_map(wild_fire_noaa_df, "crimson", "NOAA")
    plot_to_map(wild_fire_viirs_df, "orange", "VIIRS")
    plot_to_map(wild_fire_modis_df, "yellow", "MODIS")
    m.save("/Users/aowang/ceres/australia_map.html")
    add_nav_bar()
    remove_zoom()
    git_commit("Update map", "/Users/aowang/ceres/")
    git_push("/Users/aowang/ceres/")
    print("Done!", datetime.datetime.now(), "\n")


print("Running...")
schedule.every(2).hours.do(main) # currently every two hours
while True:
    schedule.run_pending()
    time.sleep(1)
