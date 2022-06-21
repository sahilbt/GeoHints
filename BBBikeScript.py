import requests
import pandas as pd
from pandas import DataFrame as df
import glob


def main():
    allFiles = glob.glob("FilteredData\*")
    for file in allFiles:
        df = pd.read_csv(file)
        startLat = df.iloc[0, 0]
        startLong = df.iloc[0,1]
        endLat = df.iloc[-1, 0]
        endLong = df.iloc[-1, 1]
        
        url = f"https://api.bbbike.org/api/0.2/bbbike/?appid=simra;startc_wgs84={startLong}%2C{startLat};startname=Brandenburger%20Tor;zielc_wgs84={endLong}%2C{endLat};zielname=Zionskirche;pref_seen=1;pref_speed=20;pref_cat=;pref_quality=;pref_specialvehicle=;scope=;output_as=gpx-track"
        r = requests.get(url)

        csvName = file.replace("FilteredData","")
        csvName = csvName.replace("-filtered.csv","")
        path = "GPXData" + csvName + "-efficientpath.gpx"
        
        with open(path, "wb") as f:
            f.write(r.content)


if __name__ == "__main__":
    main()