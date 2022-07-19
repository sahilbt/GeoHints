# **GeoHints**
In Fog and Edge computing, resources such as data replicas must be available close to the consumer. For mobile consumers, this means that data replicas are move around depending on the client location. This project aims to evalute whether location prediction for placing edge nodes can be improved with GeoHints, hints from the client about its future location. 

## **Methodology**
The main premise of this project is to compare computed routes through a city with actual routes taken by users. These details are described below. By 

### **Actual Routes**
Data to simulate user taken routes is used from the SimRa dataset of recorded bicycle rides within the city of Berlin. [SimRa](https://www.digital-future.berlin/en/research/projects/simra/) is an application intended to improve bicycle safety by utilizing crowdsourced bicycle ride data. The dataset used can be found [here](https://github.com/simra-project).

### **Computed Routes**
Computed routes are obtained by using a Routing Service which takes in a start and end coordinates to produce a route between the two locations. The start and end coordinates are obtained from each user ride. The Routing Service used in this project is [openrouteservice](https://openrouteservice.org/) (ORS).


## **Getting Started**

### **Requirements**
To ensure each of the files run correctly, be sure to have all the required dependecies installed. 

They can be installed with the following commands:
```
pip install pandas
pip install geopandas
pip install numpy
pip install matplotlib
pip install Shapely
pip install haversine
```

### **Running the Project**
This project has a few scripts that are all used to get to the final result. To get started, begin by cloning the repository to your local files.

#### **Short Run Through**
This repository contains all of the files needed to simply get the final results immediately. If you would like to just get the results, run the ```metrics.py``` script. If you would like to obtain results using a different grid size, simple edit the script using an IDE of your choice and change the ```edgeLength``` paramater to the desired size in kilometers. This script takes care of all the calculations in calculating the various metrics for this project and it will produce a csv file containing various metrics.


#### **Long Run Through**
If you wish to incorporate all the scripts and produce results from scratch, follow these steps:

1. Begin by deleting the contents of ```FilteredDataNewTime```, ```geoJSONCSV```, and ```geoJSONData``` while keeping the folder itself.
2. Run the ```dataRecalculation.py``` script. This script will handle some refactoring of the originally extracted data.
3. Run the ```ORSScript.py``` script. This script will handle the API requests to ORS in order to get a computed route for each ride. Note that a maximum of 2000 rides can be processed every 24 hours due to ORS restrictions.
4. Run the ```parseGeoJson.py``` script. This script will handle interpreting the GeoJSON files.
5. After all the previous steps have been fulfilled, the data required to run the final metrics should all be available. Run ```metrics.py```. Once the script is finished running, it will produce a csv file containing various metrics.


## **The Files**
#### **FilteredData**
Contains data extracted from the original SimRa dataset in the form of csv files. Each file corresponds to a particular ride and contains longitiude, latitude and timestamp information.

#### **FilteredDataNewTime**
Contains the same data from ```FilteredData``` in addition to some extra information. This information includes the relative distance at each given point, as well as a new timestamp metric that is relative to each ride.

#### **geoJSONCSV**
Contains data extracted from GeoJSON files that are produced by ORS when requesting a route between two points for each given ride

#### **geoJSONData**
Contains  GeoJSON data recieved from ORS when requesting a route for each ride. Data is extracted from each file and stored in ```geoJSONCSV```
#### **Detailnetz-Strassenabschnitte.geojson**
GeoJSON file containing a detailed mesh of road segements within Berlin. This is primarlily used for the ride visualizer so that rides can be overlayed on top of visible street segments. Obtained from [here](https://daten.odis-berlin.de/de/dataset/detailnetz_strassenabschnitte/).

#### **ORSScript.py**
A simple script that uses the starting ending points from each user ride and requests a computed route through ORS. Data is recieved in a GeoJSON format and stored accordingly in ```geoJSONData```

#### **dataRecalculation.py**
A script that handles calculations on the originally filtered data contained within ```FilteredData```. The script calculates relative distances between each point as well as calculates a new relative timestamp to differeniate from the original unix timestamp.

#### **key.py**
Simple used to store a users API Key that is needed for the ORS Script to function. An API Key can be obtained by creating an account with ORS.

#### **metrics.py**
The main script that handles calculating the various metrics that are used for this project. By editing the script, the user can choose the edge length for which they wish to caluculate the metrics with. Please note that grid edge lengths smaller than 1km take extremely long to run and is not reccomended.

#### **parseGeoJson.py**
A script that handles extracting relevant data from the GeoJSON files produced by ORS. Relevant data includes waypoints (longitude and latitude information), timestamps and distances.

#### **rideVisualizer.ipynb**
A Jupyter Notebook that allows the user to visualize any given ride that is contained within ```FilteredData``` and ```geoJSONCSV```. The notebook utilzes ```Detailnetz-Strassenabschnitte.geojson``` to display a mesh map of Berlin containing street segments. The user taken ride, and its computed counterpart are then overlayed on top of the map to show where the ride was taken by the user and what ORS reccomends as a path to take. 