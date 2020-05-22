"""
course: CI103
lab section: 071
date: 05/21/2020
id: aw3338
name: Ao Wang
description: The module holds the class CleanData to web scrape, clean, and present wildfire data from NASA's satellites
"""

from bs4 import BeautifulSoup
import pandas as pd
import requests
from collections import OrderedDict


class CleanData:
    """
    The CleanData object web scraps datasets from NASA's Active Fire FIRM website. Additionally, 
    cleans the data for high confidence values to prevent false positives. And is able to combine
    multiple, similar datasets from NASA's different sensors.

    :param country: The parameter specifies which country you wish to webscrap from, default: Australia
    :type country: str
    :param sensor: The parameter specifies which sensor to use, three choices: noaa, MODIS, viirs
    :type senor: str
    :param time: The parameter specifies which time to grab from, choices 24h, 48h, 7 days
    :type time: str
    """

    def __init__(self, country="Australia", sensor="noaa", time="7d"):
        self.country = country
        self.sensor = sensor
        self.time = time

    def __str__(self):
        """Overloading method to print out CleanData attributes."""
        return "CERES: WILDFIRE DATA\nCountry: {}\nSensor: {}\nTime frame: {}".format(self.country, self.sensor, self.time)

    def retrieve_data(self):
        """Web scrapes wild fire data from NASA.

        :returns: A Pandas Dataframe of wild fire
        :rtype: pandas.core.frame.DataFrame
        """
        url = "https://firms.modaps.eosdis.nasa.gov/active_fire/#firms-txt"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        # Loops through all the HTML a-tags and open the CSV file that matches the country
        # time, and sensor, and turns it into a Pandas DataFrame.
        for a_tag in soup.find_all("a", href=True):
            a_tag_string = str(a_tag)
            if all(req in a_tag_string for req in [self.country, self.time, "csv", self.sensor]):
                download_url = "https://firms.modaps.eosdis.nasa.gov" + \
                    a_tag["href"]
                return pd.read_csv(download_url)
        return

    def get_high_confidence(self):
        """Returns wild fire data frame with only high confidence values of either
           high or >= 90, determined by the sensors.

        :returns: Higher confidence wild fire data.
        :rtype: pandas.core.frame.DataFrame
        """
        df = self.retrieve_data()

        # For MODIS sensor, measures confidence through low, nominal, and high confidence
        if df.dtypes.confidence == "object":
            # (df.confidence == "nominal")|(df.confidence == "high")
            return df[df.confidence == "high"]

        # For viirs and noaa sensors, measures confidence through 0-100
        elif df.dtypes.confidence == "int64":
            return df[df.confidence >= 90]

    def combine_data_sets(self, *dfs):
        """Combines any number of similarly formatted wild fire dataframes.
           Initally, it's to combine MODIS, noaa, and viirs, but given in the
           future there are more, the method will be able to.

        :param `*dfs`: The variable argument is used for a list of wildfire datasets.
        :ivar arg: pandas.core.frame.DataFrame
        :returns: A combined wildfire datasets.
        :rtype: pandas.core.frame.DataFrame
        """
        master_df = [self.get_high_confidence(
        )[["latitude", "longitude", "acq_date"]]]
        for df in dfs:
            master_df.append(df.get_high_confidence()[
                             ["latitude", "longitude", "acq_date", "frp"]])
        return pd.concat(master_df, sort=True)

    def set_country(self, country):
        self.country = country

    def get_country(self):
        return self.country

    def set_sensor(self, sensor):
        self.sensor = sensor

    def get_sensor(self):
        return self.sensor

    def set_time(self, time):
        self.time = time

    def get_time(self):
        return self.time


def get_week_time_coordinates(df):
    """Creates a dictionary of lists with the week of day being the keys and values as lists of 
       coordinates.

    :param df: The wildfire dataframe.
    :type df: pandas.core.frame.DataFrame
    :returns: The coordinates matched with the day of the week.
    :rtype: dict
    """
    json = {}
    for row in df.itertuples():
        if row.acq_date not in json:
            json[row.acq_date] = []
        else:
            json[row.acq_date].append([row.latitude, row.longitude])
    json = OrderedDict(sorted(json.items()))
    return json


if __name__ == "__main__":
    # Initalize three CleanData objects for MODIS, viirs, and noaa
    modis, viirs, noaa = CleanData(sensor="MODIS"), CleanData(
        sensor="viirs"), CleanData(sensor="noaa")

    # Combines the three dataframes
    collected = modis.combine_data_sets(viirs, noaa)

    # Gets the fire radiative power from the combined dataframe and
    # saves it as a CSV file
    frp_series = pd.DataFrame(collected.frp[collected.frp.notna()])
    frp_series.columns = ["FRP"]
    frp_series.to_csv(
        "/home/aow252/ceres-bucket-1/ceres/website/frp.csv", index=False)

    # Gets the mapping of coordinates of wildfires per day and saves it
    # as a JSON file
    plot_data = get_week_time_coordinates(collected)
    with open("/home/aow252/ceres-bucket-1/ceres/website/week_data.json", "w") as data:
        data.write(str(plot_data).replace("'", '"'))

