from turtle import numinput
import pandas as pd
from pandas import DataFrame as df
import numpy as np
from haversine import haversine, Direction, inverse_haversine
from math import acos, pi

#START OF DEF
def average(speeds):
    average = 0
    for i in range(len(speeds)):
        average = average + speeds[i][1]

    average = average / len(speeds)
    return average
#END OF DEF

#START OF DEF
def getRideFilePath(name):
    name = "FilteredDataNewTime\\" + name + "-filtered.csv"
    return name
#END OF DEF

#START OF DEF
def findAngle(r, d):
    arg = 1 - ((d**2) / (2*(r**2)))
    angle = acos(arg)
    return angle
#END OF DEF

#START OF DEF
def getTimes(speed, distance, numPoints):
    totalTime = distance / speed
    intervals = totalTime / (numPoints - 1)
    times = [0]
    curr = intervals

    for i in range(numPoints - 1):
        times.append(curr)
        curr = curr + intervals
    return times
#END OF DEF

#START OF DEF
def getDistances(numPoints, totalDistance):
    intervals = totalDistance / (numPoints - 1)
    distances = [0]
    curr = intervals

    for i in range (numPoints - 1):
        distances.append(curr)
        curr = curr + intervals
    return distances
#END OF DEF

#START OF DEF
def getCoords(start, angle, numPoints, totalDistance):
    intervals = totalDistance / (numPoints - 1)
    coords = [start]
    curr = start
    for i in range(numPoints - 1):
        curr = inverse_haversine(curr, intervals, angle)
        coords.append(curr)
    return coords
#END OF DEF

#START OF DEF
def formatData(times, distances, coords):
    data = []
    for i in range(len(times)):
        curr = []
        curr.append(coords[i][0])
        curr.append(coords[i][1])
        curr.append(times[i])
        curr.append(distances[i])
        data.append(curr)
    return data
#END OF DEF

def main():
    speeds = pd.read_csv("speeds.csv")
    speeds = speeds.to_numpy()
    averageSpeed = average(speeds)

    for i in range(len(speeds)):
        name = getRideFilePath(speeds[i][0])
        ride = pd.read_csv(name)
        ride = ride.to_numpy()

        startCoordinate = (ride[0][0], ride[0][1])
        endCoordinate = (ride[-1][0], ride[-1][1])
        totalFlyDistance = haversine(startCoordinate, endCoordinate)
        northCoordinate = inverse_haversine(startCoordinate, totalFlyDistance, Direction.NORTH)
        distanceNorthEnd = haversine(northCoordinate, endCoordinate)
        angle = findAngle(totalFlyDistance, distanceNorthEnd)
        if(endCoordinate[1] < startCoordinate[1]):
            angle = (2*pi) - angle

        times = getTimes(averageSpeed, totalFlyDistance, len(ride))
        distances = getDistances(len(ride), totalFlyDistance)
        coords = getCoords(startCoordinate, angle, len(ride), totalFlyDistance)
        formatted = formatData(times, distances, coords)
        
        data = np.array(formatted)
        frame = df(data, columns = ['lat', 'long', 'timeStamp', 'distance'])
        path = "CrowData\\" + speeds[i][0] + "-crow.csv"
        frame.to_csv(path, index = False)


if __name__ == "__main__":
    main()