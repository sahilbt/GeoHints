import json
import geopandas as gpd
import pandas as pd
from pandas import DataFrame as df
import numpy as np
import glob


def main():

    allFiles = glob.glob("geoJSONData\*")
    for file in allFiles:
        #coordinate extraction
        print(file)
        geo = gpd.read_file(file)
        frame = pd.DataFrame(geo)
        coordinatesLineString = frame["geometry"]
        toString = str(coordinatesLineString[0])
        toString = toString.replace("LINESTRING (", "")
        toString = toString.replace(")", "")
        coordinatesAsString = toString.split(", ")
        for i in range(0, len(coordinatesAsString)):
            coordinatesAsString[i] = coordinatesAsString[i].split(" ")
            #At this point, coordiantesAsString should be a 2D array with each entry containg a set 
            #of ordered lat/long pairs

        #timestamp extraction
        segments = frame['segments']
        asString = str(segments[0])
        asString = asString.split(', "steps"')
        asString = asString[0].split(", ")
        asString = asString[1].replace('"duration": ', "")
        duration = float(asString)
        intervals = duration / (len(coordinatesAsString) - 1)

        t = 0
        times = []
        for i in range(len(coordinatesAsString)):
            times.append(t)
            t = t+intervals



        nparray = np.array(coordinatesAsString)
        times = np.array(times)
        newFrame = df(nparray, columns = ["long", "lat"])
        newFrame["timeStamp"] = times
    
        name = file.replace("geoJSONData", "")
        name = name.replace(".geojson", "")
        path = "geoJSONCSV" + name + ".csv"

        newFrame.to_csv(path, index = False)


if __name__ == "__main__":
    main()