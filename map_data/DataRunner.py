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
import datetime
import time


def collectAndClean():
    # Initalize three CleanData objects for MODIS, viirs, and noaa
    print("Web scraping NASA satellite data...", end="")
    modis, viirs, noaa = CleanData(sensor="MODIS"), CleanData(
        sensor="viirs"), CleanData(sensor="noaa")
    print("DONE!! At {}".format(datetime.datetime.now()))

    # Combines the three dataframes
    print("Combining and cleaning...", end="")
    collected = modis.combine_data_sets(viirs, noaa)
    print("DONE!! At {}".format(datetime.datetime.now()))

    # Gets the fire radiative power from the combined dataframe and
    # saves it as a CSV file
    print("Gathering FRP data...", end="")
    frp_series = pd.DataFrame(collected.frp[collected.frp.notna()])
    frp_series.columns = ["FRP"]
    frp_series.to_csv(
        "/home/aow252/ceres-bucket-1/ceres/website/frp.csv", index=False)
    print("DONE!! At {}".format(datetime.datetime.now()))

    print("Mapping wildfire data...", end="")
    # Gets the mapping of coordinates of wildfires per day and saves it
    # as a JSON file
    plot_data = get_week_time_coordinates(collected)
    with open("/home/aow252/ceres-bucket-1/ceres/website/week_data.json", "w") as data:
        data.write(str(plot_data).replace("'", '"'))
    print("DONE!! At {}".format(datetime.datetime.now()))

def runGit():
    print("Committing and Pushing...", end="")
    # Initialize the object to run git commands
    command = AutomateCommit(commit_message="Update wildfire data",
                             repo_dir="/home/aow252/ceres-bucket-1/ceres/")
    command.git_commit()
    command.git_push()
    print("DONE!! At {}\n".format(datetime.datetime.now()))


def main():
    print("""             (         (                  (    (    (      (     (    (         
   (         )\ )      )\ )     (  (      )\ ) )\ ) )\ )   )\ )  )\ ) )\ )      
   )\   (   (()/( (   (()/(     )\))(   '(()/((()/((()/(  (()/( (()/((()/( (    
 (((_)  )\   /(_)))\   /(_))   ((_)()\ )  /(_))/(_))/(_))  /(_)) /(_))/(_)))\   
 )\___ ((_) (_)) ((_) (_))  _  _(())\_)()(_)) (_)) (_))_  (_))_|(_)) (_)) ((_)  
((/ __|| __|| _ \| __|/ __|(_) \ \((_)/ /|_ _|| |   |   \ | |_  |_ _|| _ \| __| 
 | (__ | _| |   /| _| \__ \ _   \ \/\/ /  | | | |__ | |) || __|  | | |   /| _|  
  \___||___||_|_\|___||___/(_)   \_/\_/  |___||____||___/ |_|   |___||_|_\|___| 
                                                                                """)
    collectAndClean()
    runGit()


# Runs the script every 12 hours
#schedule.every(12).hours.do(main)
#while True:
#    schedule.run_pending()
#    time.sleep(1)
main()
