import folium
import pandas as pd
import requests
from bs4 import BeautifulSoup
import schedule
import time
import datetime
import subprocess as cmd

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

wild_fire_noaa_df = pd.read_csv(retrieve_data("Australia", "noaa-20"))
wild_fire_viirs_df = pd.read_csv(retrieve_data("Australia", "viirs"))
wild_fire_modis_df = pd.read_csv(retrieve_data("Australia", "MODIS"))
m = folium.Map(location=[-28.2744, 135.7751], zoom_start = 4.5) # Creates the map focusing on Australia

def plot_to_map(wild_fire_df, fill_in_color, stamp):
    """Plots all the points to the map
    """
    b = wild_fire_df[[col for col in wild_fire_df.columns if "bright" in col][0]]
    for lat, lon, inten in zip(wild_fire_df.latitude, wild_fire_df.longitude, b):
        folium.Circle(
          location=[lat, lon],
          popup="{} - Brightness: {}".format(stamp, inten),
          radius=inten,
          color=fill_in_color,
          fill=True,
          fill_color=fill_in_color
       ).add_to(m)

        
def add_nav_bar():
    pass


def remove_zoom():
    pass


def main():
    """Updates the map daily at 12 PM. Different colors represent the different satellite. 
    """
    print("Folium version:", folium.__version__) # 0.10.1
    plot_to_map(wild_fire_noaa_df, "crimson", "NOAA")
    plot_to_map(wild_fire_viirs_df, "orange", "VIIRS")
    plot_to_map(wild_fire_modis_df, "yellow", "MODIS")
    m.save("/Users/aowang/715/australia_map.html")
    print("Done!", datetime.datetime.now())
    
schedule.every().day.at("12:00").do(main)
while True:
    schedule.run_pending()
    time.sleep(1)