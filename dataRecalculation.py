import pandas as pd
from pandas import DataFrame as df
import glob
import numpy as np


#START OF DEF
def newTimeStamp(df):
    times = df['timeStamp']
    times = times.to_numpy()
    ref = times[0]

    for i in range(len(times)):
        times[i] = (times[i] - ref) / 1000
#END OF DEF


#START OF DEF
def calculateDistances(df):
    x=2
#END OF DEF


def main():

    allFiles = glob.glob("FilteredData\*")

    for file in allFiles:
        df = pd.read_csv(file)
        times = newTimeStamp(df)
        distances = calculateDistances(df)

        df = df.assign(timeStamp = times)
        path = file.replace("FilteredData", "FilteredDataNewTime")
        df.to_csv(path, index=False)






if __name__ == "__main__":
    main()