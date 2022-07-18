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

They can be installed with the following commands
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
This repository contains all of the files needed to simply get the final results immediately. If you would like to just get the results without any hassle, run the ```metrics.py``` script. This script takes care of all the calculations in calculating the various metrics for this project and will produce an output file contaning the results named ```results.csv```.


#### **Long Run Through**
If you wish to incorporate all the scripts and produce results from scratch, follow these steps:

1. Begin by deleting the contents of ```FilteredDataNewTime```, ```geoJSONCSV```, and ```geoJSONData``` while keeping the folder itself.
2. Run the ```dataRecalculation.py``` script. This script will handle some refactoring of the originally extracted data.
3. Run the ```ORSScript.py``` script. This script will handle the API requests to ORS in order to get a computed route for each ride. Note that a maximum of 2000 rides can be processed every 24 hours do to ORS restrictions.
4. Run the ```parseGeoJson.py``` script. This script will handle interpreting the GeoJSON files.
5. After all the previous steps have been fulfilled, the data required to run the final metrics should all be available. Run ```metrics.py```. Once the script is finished running, results will be available under ```results.csv```.