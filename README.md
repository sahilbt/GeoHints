# **GeoHints**
In Fog and Edge computing, resources such as data replicas must be available close to the consumer. For mobile consumers, this means that data replicas are move around depending on the client location. This project aims to evalute whether location prediction for placing edge nodes can be improved with GeoHints, hints from the client about its future location. 

## **Methodology**
The main premise of this project is to compare computed routes through a city with actual routes taken by users. These details are described below. By 

### **Actual Routes**
Data to simulate user taken routes is used from the SimRa dataset of recorded bicycle rides within the city of Berlin. [SimRa](https://www.digital-future.berlin/en/research/projects/simra/) is an application intended to improve bicycle safety by utilizing crowdsourced bicycle ride data. The dataset used can be found [here](https://github.com/simra-project).

### **Computed Routes**
Computed routes are obtained by using a Routing Service which takes in a start and end coordinates to produce a route between the two locations. The start and end coordinates are obtained from each user ride. The Routing Service used in this project is [openrouteservice](https://openrouteservice.org/) (OSR).


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
