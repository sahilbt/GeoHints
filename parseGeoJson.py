import json
import geopandas as gpd
import pandas as pd
from pandas import DataFrame as df
import numpy as np
import glob
from decimal import *


def getCoordinates(frame):
    """
    Extracts coordinates from a given geoJSON file and returns it as an array of coordinates
    """
    coordinatesLineString = frame["geometry"]

    #String replacing to remove all unnecessary data
    toString = str(coordinatesLineString[0])
    toString = toString.replace("LINESTRING (", "")
    toString = toString.replace(")", "")
    coordinatesAsString = toString.split(", ")

    #Reading and adding coordinates to array
    for i in range(0, len(coordinatesAsString)):
        coordinatesAsString[i] = coordinatesAsString[i].split(" ")
        coordinatesAsString[i].reverse()
    
    return coordinatesAsString



def getTimeStampsAndDistance(frame):
    """
    Extracts timestamp and distance information from a given GeoJSON file and returns both 
    as individual arrays
    """
    #Initial Setup for extraction, removing unnecessary data
    segments = frame['segments']
    asString = str(segments[0])
    asString = asString.split(', "steps"')
    asString = asString[1].replace(": [ ", "", 1)
    asString = asString.split("{")
    asString.pop(0)
    asString.pop(-1)

    #Get waypoint data
    waypoints = getWayPoints(asString)

    #Calculate timestamps and distances using waypoints
    times, distances = calculateTimeDistance(waypoints)
    return times, distances


def getWayPoints(asString):
    """
    Extracts waypoint information from a given GeoJSON file
    Information includes distance, timestamp, and coordinates
    """
    waypoints = []
    for i in range(len(asString)):
        curr = asString[i].split('"')
        temp = []
        temp.append(curr[4])
        temp.append(curr[2])
        temp.append(curr[-1])
        temp[0] = temp[0].replace(": ", "")
        temp[0] = temp[0].replace(", ", "")
        temp[0] = Decimal(temp[0])
        temp[1] = temp[1].replace(": ", "")
        temp[1] = temp[1].replace(", ", "")
        temp[1] = Decimal(temp[1])
        temp[2] = temp[2].replace(": ", "")
        temp[2] = temp[2].replace(" }, ", "")
        temp[2] = json.loads(temp[2])
        waypoints.append(temp)
    return waypoints



def calculateTimeDistance(waypoints):
    """
    Primary function that handles calulation of timestamps and distances based on the 
    extracted waypoint information
    """
    times, distances = [0], [0]
    t, d = 0, 0

    for j in range(len(waypoints)):
        #Current duration from current waypoint
        duration = waypoints[j][0]

        #Current distance from current waypoint
        currDistance = waypoints[j][1] / 1000

        #Current set of coordinates for current waypoint
        points = waypoints[j][2]
        num = points[1] - points[0]

        #Time (interval) and distance (interval2) intervals for current waypoint
        interval = duration / num
        interval2 = currDistance / num
        t = times[-1]
        d = distances[-1]

        #Assigning each interval to a coordinate
        for k in range(num):
            t = t + interval
            d = d + interval2
            times.append(t)
            distances.append(d)
    return times, distances


def main():
    #Get all files and iterate over all files
    allFiles = glob.glob("geoJSONData\*")
    for file in allFiles:
        #Read current GeoJSON file using geopandas
        print(file)
        geo = gpd.read_file(file)

        #Convert to data frame
        frame = pd.DataFrame(geo)

        #Coordinate extraction
        coordinates = getCoordinates(frame)

        #Timestamp and Distance extraction
        times, distances = getTimeStampsAndDistance(frame)

        #Assign extracted data to a new data frame
        nparray = np.array(coordinates)
        times = np.array(times)
        newFrame = df(nparray, columns = ["lat", "long"])
        newFrame["timeStamp"] = times
        newFrame["Distance"] = distances
    
        #Create path for data to be stored and export dataframe as csv
        name = file.replace("geoJSONData", "")
        name = name.replace(".geojson", "")
        path = "geoJSONCSV" + name + ".csv"
        newFrame.to_csv(path, index = False)


if __name__ == "__main__":
    main()