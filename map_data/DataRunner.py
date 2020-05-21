"""
course: CI103
lab section: 071
date: 05/21/2020
id: aw3338
name: Ao Wang
description: The script is the runner, used to collect, clean, and plot the map and statistics, then push to the Github repo.
"""

from CleanData import CleanData, get_week_time_coordinates
from GitCommand import AutomateCommit
import pandas as pd
import schedule
import time


def collectAndClean():
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


def runGit():
    # Initialize the object to run git commands
    command = AutomateCommit(commit_message="Update wildfire data",
                             repo_dir="/home/aow252/ceres-bucket-1/ceres/")
    command.git_commit()
    command.git_push()


def main():
    collectAndClean()
    runGit()


# Runs the script every 12 hours
schedule.every(12).hours.do(main)
while True:
    schedule.run_pending()
    time.sleep(1)
