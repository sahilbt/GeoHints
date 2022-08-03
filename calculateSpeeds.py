import pandas as pd
from pandas import DataFrame as df
import numpy as np
import glob


def getName(file):
    file = file.replace("-efficientpath.csv", "-filtered.csv")
    file = file.replace("geoJSONCSV\\", "FilteredDataNewTime\\")
    return file


def main():
    allFiles = glob.glob("geoJSONCSV\*")
    speeds = []
    for file in allFiles:
        currFile = getName(file)
        print()
        frame = pd.read_csv(currFile)
        name = currFile.replace("FilteredDataNewTime\\", "")
        name = name.replace("-filtered.csv", "")
        frame = frame.to_numpy()
        time = frame[-1][2]
        distance = frame[-1][3]
        speed = distance / time
        speeds.append([name, speed])

    export = df(speeds, columns = ["Ride", "Speed (km/s)"])
    export.to_csv("speeds.csv", index = False)

if __name__ == "__main__":
    main()