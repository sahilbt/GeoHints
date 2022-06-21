import pandas as pd
from pandas import DataFrame as df
import gpxpy
import numpy as np
import glob


def main():
    allFiles = glob.glob("GPXData\*")

    for file in allFiles:
        x = []
        y = []
        gpf = open(file, "r")

        gpx = gpxpy.parse(gpf)

        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    x.append(point.longitude)
                    y.append(point.latitude)


        data = []
        for i in range(0, len(x)):
            temp = []
            temp.append(y[i])
            temp.append(x[i])
            data.append(temp)

        if(len(x) == 0 or len(y) == 0):
            print(file)
            continue
        num = np.array(data)
        frame = df(num, columns = ["lat", "long"])
        name = file.replace("GPXData", "")
        name = name.replace(".gpx", "")
        path = "GPXCSV" + name + ".csv"

        frame.to_csv(path, index = False)


if __name__ == "__main__":
    main()  