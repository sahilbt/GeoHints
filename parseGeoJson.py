import json
import geopandas as gpd
import pandas as pd
from pandas import DataFrame as df
import numpy as np
import glob
from decimal import *


def main():

    allFiles = glob.glob("geoJSONData\*")
    for file in allFiles:
        #coordinate extraction
        geo = gpd.read_file(file)
        frame = pd.DataFrame(geo)
        coordinatesLineString = frame["geometry"]
        toString = str(coordinatesLineString[0])
        toString = toString.replace("LINESTRING (", "")
        toString = toString.replace(")", "")
        coordinatesAsString = toString.split(", ")
        for i in range(0, len(coordinatesAsString)):
            coordinatesAsString[i] = coordinatesAsString[i].split(" ")
            coordinatesAsString[i].reverse()
            #At this point, coordiantesAsString should be a 2D array with each entry containg a set 
            #of ordered lat/long pairs

        #timestamp extraction
        segments = frame['segments']
        asString = str(segments[0])
        asString = asString.split(', "steps"')
        asString = asString[1].replace(": [ ", "", 1)
        asString = asString.split("{")
        asString.pop(0)
        asString.pop(-1)

        waypoints = []

        for i in range(len(asString)):
            curr = asString[i].split('"')
            temp = []
            temp.append(curr[4])
            temp.append(curr[-1])
            temp[0] = temp[0].replace(": ", "")
            temp[0] = temp[0].replace(", ", "")
            temp[0] = Decimal(temp[0])
            temp[1] = temp[1].replace(": ", "")
            temp[1] = temp[1].replace(" }, ", "")
            temp[1] = json.loads(temp[1])
            waypoints.append(temp)

        times = [0]
        t = 0
        for j in range(len(waypoints)):
            duration = waypoints[j][0]
            points = waypoints[j][1]
            num = points[1] - points[0]
            interval = duration / num
            t = times[-1]

            for k in range(num):
                t = t + interval
                times.append(t)






        nparray = np.array(coordinatesAsString)
        times = np.array(times)
        newFrame = df(nparray, columns = ["lat", "long"])
        newFrame["timeStamp"] = times
    
        name = file.replace("geoJSONData", "")
        name = name.replace(".geojson", "")
        path = "geoJSONCSV" + name + ".csv"

        newFrame.to_csv(path, index = False)


if __name__ == "__main__":
    main()