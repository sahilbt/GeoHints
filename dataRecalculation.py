import pandas as pd
from pandas import DataFrame as df
import glob
import numpy as np
from haversine import haversine, Direction


def newTimeStamp(df):
    """
    Recalculates the time stamps for a particular ride to be relative to the ride
    i.e Converts from Unix Epoch to a relative time
    """
    times = df['timeStamp']
    times = times.to_numpy()
    #Set the first time stamp as the reference
    ref = times[0]

    #Subtract the reference from each timestamp to get a relative time to the ride
    for i in range(len(times)):
        times[i] = (times[i] - ref) / 1000

    return times


def calculateDistances(frame):
    """
    Calculates the distance between every point in a given ride and assigns a 'distance stamp' 
    to each coordinate
    """
    array = frame.to_numpy()
    total = 0
    distances = [0]

    for i in range(len(array) - 1):
        #Assign current and next point
        currPoint = (array[i][0], array[i][1])
        nextPoint = (array[i+1][0], array[i+1][1])

        #Calculate distance between current and next point
        currentDistance = haversine(currPoint, nextPoint)

        #Add to total and assign distance to the current point
        total = total + currentDistance
        distances.append(total)

    return distances


def main():
    #Get all files and iterate over all files
    allFiles = glob.glob("FilteredData\*")

    for file in allFiles:
        #Read file
        df = pd.read_csv(file)

        #Recalculated data
        times = newTimeStamp(df)
        distances = calculateDistances(df)

        #Assigning newly calculated data back to the dataframe and exporting as a csv
        df = df.assign(timeStamp = times)
        df['Distance'] = distances
        path = file.replace("FilteredData", "FilteredDataNewTime")
        df.to_csv(path, index=False)


if __name__ == "__main__":
    main()