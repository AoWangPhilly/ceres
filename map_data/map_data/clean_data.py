from bs4 import BeautifulSoup
import pandas as pd
import requests


class CleanData:
    def __init__(self, country="Australia", sensor="noaa", time="7d"):
        self.country = country
        self.sensor = sensor
        self.time = time

    def __str__(self):
        return "CERES: WILDFIRE DATA\nCountry: {}\nSensor: {}\nTime frame: {}".format(self.country,
                                                                                      self.sensor,
                                                                                      self.time)

    def retrieve_data(self):
        url = "https://firms.modaps.eosdis.nasa.gov/active_fire/#firms-txt"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        for a_tag in soup.find_all("a", href=True):
            a_tag_string = str(a_tag)
            if all(req in a_tag_string for req in [self.country, self.time, "csv", self.sensor]):
                download_url = "https://firms.modaps.eosdis.nasa.gov" + \
                    a_tag["href"]
                return pd.read_csv(download_url)
        return

    def get_high_confidence(self):
        df = self.retrieve_data()
        if df.dtypes.confidence == "object":
            # (df.confidence == "nominal")|(df.confidence == "high")
            return df[df.confidence == "high"]
        elif df.dtypes.confidence == "int64":
            return df[df.confidence >= 90]

    def combine_data_sets(self, *dfs):
        master_df = [self.get_high_confidence(
        )[["latitude", "longitude", "acq_date"]]]
        for df in dfs:
            master_df.append(df.get_high_confidence()[
                             ["latitude", "longitude", "acq_date", "frp"]])
        return pd.concat(master_df)

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


if __name__ == "__main__":
    def get_week_time_coordinates(df):
        json = {}
        for arr in collected.itertuples():
            if arr.acq_date not in json:
                json[arr.acq_date] = []
            else:
                json[arr.acq_date].append([arr.latitude, arr.longitude])
        return json

    modis, viirs, noaa = CleanData(sensor="MODIS"), CleanData(
        sensor="viirs"), CleanData(sensor="noaa")
    collected = modis.combine_data_sets(viirs, noaa)

    frp_series = collected.frp[collected.frp.notna()]
    frp_series.to_csv("/Users/aowang/715/website/frp.csv", index=False)

    plot_data = get_week_time_coordinates(collected)
    with open("/Users/aowang/715/website/week_data.json", "w") as data:
        data.write(str(plot_data).replace("'", '"'))
