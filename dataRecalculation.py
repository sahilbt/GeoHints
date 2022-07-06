import pandas as pd
from pandas import DataFrame as df
import glob
import numpy as np
from haversine import haversine, Direction


#START OF DEF
def newTimeStamp(df):
    times = df['timeStamp']
    times = times.to_numpy()
    ref = times[0]

    for i in range(len(times)):
        times[i] = (times[i] - ref) / 1000

    return times
#END OF DEF


#START OF DEF
def calculateDistances(frame):
    array = frame.to_numpy()
    total = 0
    distances = [0]

    for i in range(len(array) - 1):
        currPoint = (array[i][0], array[i][1])
        nextPoint = (array[i+1][0], array[i+1][1])
        currentDistance = haversine(currPoint, nextPoint)
        total = total + currentDistance
        distances.append(total)

    return distances
#END OF DEF


def main():

    allFiles = glob.glob("FilteredData\*")

    for file in allFiles:
        df = pd.read_csv(file)
        times = newTimeStamp(df)
        distances = calculateDistances(df)

        df = df.assign(timeStamp = times)
        df['Distance'] = distances
        path = file.replace("FilteredData", "FilteredDataNewTime")
        df.to_csv(path, index=False)






if __name__ == "__main__":
    main()