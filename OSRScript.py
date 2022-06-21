import requests
import pandas as pd
from pandas import DataFrame as df
import glob
import time
from key import osr_api_key


def main():
    allFiles = glob.glob("FilteredData\*")
    for file in allFiles:
        df = pd.read_csv(file)
        startLat = df.iloc[0, 0]
        startLong = df.iloc[0,1]
        endLat = df.iloc[-1, 0]
        endLong = df.iloc[-1, 1]

        url = f"https://api.openrouteservice.org/v2/directions/cycling-regular?api_key={osr_api_key}&start={startLong},{startLat}&end={endLong},{endLat}"
        r = requests.get(url)

        csvName = file.replace("FilteredData","")
        csvName = csvName.replace("-filtered.csv","")
        path = "geoJSONData" + csvName + "-efficientpath.geojson"

        with open(path, "wb") as f:
            f.write(r.content)

        time.sleep(2)


if (__name__ == "__main__"):
    main()