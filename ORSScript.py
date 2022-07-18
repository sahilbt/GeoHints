import requests
import pandas as pd
from pandas import DataFrame as df
import glob
import time
from key import osr_api_key


def main():
    # Get all files in directory and iterate over all files
    allFiles = glob.glob("FilteredData\*")
    for file in allFiles:
        #Read current file
        df = pd.read_csv(file)

        #Get start and end coorindates of current ride
        startLat = df.iloc[0, 0]
        startLong = df.iloc[0,1]
        endLat = df.iloc[-1, 0]
        endLong = df.iloc[-1, 1]

        #Generate request with OSR API
        #The user must have their own API KEY obtained from creating an OSR account
        #Please input this API KEY in the key.py file
        print(file)
        url = f"https://api.openrouteservice.org/v2/directions/cycling-regular?api_key={osr_api_key}&start={startLong},{startLat}&end={endLong},{endLat}"
        r = requests.get(url)

        #Path creation. This OSR request generates a response in the format of a GeoJSON file
        csvName = file.replace("FilteredData","")
        csvName = csvName.replace("-filtered.csv","")
        path = "geoJSONData" + csvName + "-efficientpath.geojson"

        #Write contents of the request to the path
        with open(path, "wb") as f:
            f.write(r.content)

        #Delay used so OSR limit is not exceeded
        time.sleep(2)


if (__name__ == "__main__"):
    main()