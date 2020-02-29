import folium
import pandas as pd
import requests
import bs4
import schedule
import time
import datetime
import subprocess
from folium import plugins
from bs4 import BeautifulSoup
import plotly.offline 
import plotly.graph_objs as go

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
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    a_tag = soup.findAll("a")
    a_tag_string = [str(tag) for tag in a_tag]
    for idx in range(len(a_tag_string)):
        if all(req in a_tag_string[idx]
               for req in [country, time, "csv", sensor]):
            index = idx
            break
    link = a_tag[index]["href"]
    download_url = "https://firms.modaps.eosdis.nasa.gov" + link
    return download_url


def high_confidence(m, v, n):
    """Drops all the coordinates that are less than 80% confidence and low confidence

    Args:
        m (pandas.core.frame.DataFrame): The MODIS sensor
        v (pandas.core.frame.DataFrame): The viirs sensor
        n (pandas.core.frame.DataFrame): The noaa sensor

    Returns:
        tuple (pandas.core.frame.DataFrame): A tuple of the three dataframes
    """
    m = m[m.confidence >= 80].drop_duplicates()
    v = v[(v.confidence == "nominal") | (
        v.confidence == "high")].drop_duplicates()
    n = n[(n.confidence == "nominal") | (
        n.confidence == "high")].drop_duplicates()
    return m, v, n


def combine_data_sets(df):
    """Combinates the three data frames

    Args:
        df (tuple (pandas.core.frame.DataFrame)): The tuple of dataframes from MODIS, viirs, and noaa

    Returns:
        pandas.core.frame.DataFrame: The combined dataframes
    """
    all_df = []
    for i in range(3):
        all_df.append(df[i][["latitude", "longitude", "acq_date"]])
    return pd.concat(all_df)


def get_week_time_coordinates(df):
    """Groups up the coordinates with the same times

    Args:
        df: The combined dataframes

    Returns:
        tuple (list): Returns grouped up coordinates by the dates, as well as the week dates

    """
    week, start = [], 0
    times = [str(i) for i in df["acq_date"].drop_duplicates()]
    for i in range(len(times)):
        end = df.index[df.acq_date == times[i]][len(
            df.index[df.acq_date == times[i]]) - 1] + 1
        df1 = df.iloc[start:end][["latitude", "longitude"]]
        day1 = [[df1.iloc[j][0], df1.iloc[j][1]] for j in range(len(df1))]
        week.append(day1)
        start = end
    return week, times


def fix_slider():
    """Fixes the HeatMapWithTime slider issue"""
    script1 = r'<link rel="stylesheet" href="http://apps.socib.es/Leaflet.TimeDimension/dist/leaflet.timedimension.control.min.css"/>'
    script2 = r'<link rel="stylesheet" href="https://rawcdn.githack.com/socib/Leaflet.TimeDimension/master/dist/leaflet.timedimension.control.min.css"/>'
    with open("/home/aow252/ceres/website/REALMAP.html", "r") as mapping, open("/home/aow252/ceres/website/REALMAP.html", "r+") as new_mapping:
        html = mapping.read()
        html = html.replace(script1, script2)
        new_mapping.write(html)

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
    """Updates the map every four hours.
    """

    # Creates the map focusing on Australia
    m = folium.Map(location=[-28.2744,
                             135.7751],
                   zoom_start=3.5,
                   world_copy_jump=True,
                   control_scale=True)

    print("Web scraping...")
    wild_fire_noaa_df = pd.read_csv(retrieve_data("Australia", "noaa", "7d"))
    wild_fire_viirs_df = pd.read_csv(retrieve_data("Australia", "viirs", "7d"))
    wild_fire_modis_df = pd.read_csv(retrieve_data("Australia", "MODIS", "7d"))

    print("Gathering data...")
    high_c = high_confidence(
        wild_fire_modis_df,
        wild_fire_viirs_df,
        wild_fire_noaa_df)
    main_df = combine_data_sets(high_c)

    print("Cleaning data...")

    # main_df.to_csv("main_df.csv")
    formatted = get_week_time_coordinates(main_df)
    
    # Creates the line graph
    data = [go.Scatter(x=formatted[1], y=[len(coord) for coord in formatted[0]], mode="lines")]
    layout = go.Layout(title="Australian's Weekly Bushfire Progression")
    fig = go.Figure(data, layout)
    plotly.offline.plot(fig, filename ="/home/aow252/ceres/website/wildfirestats.html", auto_open=False)
    
    plugins.HeatMapWithTime(
        formatted[0],
        formatted[1],
        position="bottomleft").add_to(m)
    print("Plotting...")

    plugins.MousePosition().add_to(m)  # adds coordinates for where the cursor is
    minimap = plugins.MiniMap()  # Addings minimap for easier navigation
    m.add_child(minimap)

    # Adds different tile options for the map
    stylings = [
        'openstreetmap',
        'Stamen Terrain',
        'stamentoner',
        'cartodbpositron',
        'cartodbdark_matter']
    for style in stylings:
        folium.TileLayer(style).add_to(m)
    folium.LayerControl().add_to(m)

    m.save("/home/aow252/ceres/website/REALMAP.html")
    fix_slider()

    print("Commiting and pushing to Github webpage...")
    git_commit("Update map", "/home/aow252/ceres/")
    git_push("/home/aow252/ceres/")
    print("Done!", datetime.datetime.now(), "\n")
    print("Running...")


print("Running...")
print("Folium version:", folium.__version__)  # 0.10.1
print("Pandas version:", pd.__version__)  # 0.25.3
print("Requests version:", requests.__version__)  # 2.22.0
print("BS4 version:", bs4.__version__)  # 4.8.1

schedule.every(4).hours.do(main)  # currently every four hours
while True:
    schedule.run_pending()
    time.sleep(1)
