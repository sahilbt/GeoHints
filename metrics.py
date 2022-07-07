import pandas as pd
from pandas import DataFrame as df
import matplotlib.pyplot as plt
import descartes
import geopandas as gpd
from shapely.geometry import Point, Polygon
import shapely
import glob
import numpy as np
from haversine import haversine, inverse_haversine, Direction
from math import sqrt, pi

# START OF DEF
def createGrid(edgeLength):
    # Creating grid cells given an edge length 
    gridcells = []
    columns = []

    # Bounding box of 'Detailnetz-Strassenabschnitte.geojson' file
    xmin =  13.090246535756732
    ymin =  52.340436617775886
    xmax =  13.756924989951091
    ymax =  52.659932312168635
    topLeft = (ymax, xmin)

    hyp = sqrt(edgeLength**2 + edgeLength**2)

    #Make first column
    while(topLeft[0] > ymin):
        newSquareBR = inverse_haversine(topLeft, hyp, 135*(pi/180))

        #Grid cell dimensions
        sqxmin = topLeft[1]
        sqxmax = newSquareBR[1]
        sqymin = newSquareBR[0]
        sqymax = topLeft[0]

        #Create polygon with dimensions
        square = shapely.geometry.box(sqxmin, sqymin, sqxmax, sqymax)
        gridcells.append(square)
        coords = list(square.exterior.coords)
        topLeft = (coords[3][1], coords[3][0])
        columns.append((coords[1][1], coords[1][0]))

    #Make rest of the rows
    for i in range(len(columns)):
        topLeft = columns[i]
        while (topLeft[1] < xmax):
            #Find BR corner of new grid cell
            newSquareBR = inverse_haversine(topLeft, hyp, 135*(pi/180))

            #Grid cells dimensions
            sqxmin = topLeft[1]
            sqxmax = newSquareBR[1]
            sqymin = newSquareBR[0]
            sqymax = topLeft[0]

            #Create polygon with dimensions
            square = shapely.geometry.box(sqxmin, sqymin, sqxmax, sqymax)
            gridcells.append(square)

            #Get cooridinates of ploygon and flip them for easier use
            coords = list(square.exterior.coords)
            temp = []
            for i in range(len(coords)):
                temp.append((coords[i][1], coords[i][0]))
            coords = temp 

            topLeft = coords[1]

    return gridcells
#END OF DEF


#START OF DEF
def findClosest(rec, timeStamp):
    absUser = np.abs(rec - timeStamp)
    index = absUser.argmin()
    return index, rec[index]
#END OF DEF


#START OF DEF
def findContainingGrid(point, gridcells):
    for i in range(len(gridcells)):
        cell = gridcells[i]
        if(cell.contains(point)):
            return cell
#END OF DEF

#START OF DEF
def userDirectory(path):
    path = path.replace("geoJSONCSV", "")
    path = path.replace("efficientpath.csv", "")
    name = path
    path = "FilteredDataNewTime" + path + "filtered.csv"
    return name, path
#END OF DEF


#START OF DEF
def getRecTimeStamps(rec):
    recTimeStamps = []
    for i in range(len(rec)):
        recTimeStamps.append(rec[i][2])
    recTimeStamps = np.array(recTimeStamps)
    return recTimeStamps
#END OF DEF    


#START OF DEF
def getOverlapForCurrentRide(rec, user, recTimeStamps, gridcells):
    userEndTimeStamp = user[-1][2]
    recEndTimeStamp = rec[-1][2]
    userGrid = []
    recGrid = []

    #Find gridcells that eachpoint is contained within
    for i in range(len(user)):
        userCurrentTimeStamp = user[i][2]
        userCurrentPoint = Point(user[i][1], user[i][0])
        recIndex, recClosestTime = findClosest(recTimeStamps, userCurrentTimeStamp)
        recCurrentPoint = Point(rec[recIndex][1], rec[recIndex][0])

        recGrid.append(findContainingGrid(recCurrentPoint, gridcells))
        userGrid.append(findContainingGrid(userCurrentPoint, gridcells))

    return userGrid, recGrid
#END OF DEF


#START OF DEF
def calculateScore(recGrid, userGrid):
    match = 0
    for j in range(len(recGrid)):
        if(recGrid[j] == userGrid[j]): 
            match = match + 1
    score  = (match / len(recGrid))
    return score
#END OF DEF


#START OF DEF
def calculateScore2(recGrid, user, edgeLength, gridcells):
    match = 0
    for i in range(len(user)):
        oneOverCells = []
        recCurrentGrid = recGrid[i]
        userCurrentPoint = (user[i][0], user[i][1])
        Npt = inverse_haversine(userCurrentPoint, edgeLength, Direction.NORTH)
        Ept = inverse_haversine(userCurrentPoint, edgeLength, Direction.EAST)
        Spt = inverse_haversine(userCurrentPoint, edgeLength, Direction.SOUTH)
        Wpt = inverse_haversine(userCurrentPoint, edgeLength, Direction.WEST)

        Npt = tuple(reversed(Npt))
        Ept = tuple(reversed(Ept))
        Spt = tuple(reversed(Spt))
        Wpt = tuple(reversed(Wpt))

        oneOverCells.append(findContainingGrid(Point(Npt), gridcells))
        oneOverCells.append(findContainingGrid(Point(Ept), gridcells))
        oneOverCells.append(findContainingGrid(Point(Spt), gridcells))
        oneOverCells.append(findContainingGrid(Point(Wpt), gridcells))

        for j in range(4):
            if(oneOverCells[j] == recCurrentGrid):
                match = match + 1

    return match / len(user)
#END OF DEF


def main():
    edgeLength = 4

    allScores = []

    allReccomendedRides = glob.glob('geoJSONCSV\*')
    for file in allReccomendedRides:
        name, userDirectoryPath = userDirectory(file)
        name = name.replace("\\", "")
        name = name[:-1]

        rec = pd.read_csv(file)
        user = pd.read_csv(userDirectoryPath)

        user = user.to_numpy()
        rec = rec.to_numpy()
        
        gridcells = createGrid(edgeLength)

        recTimeStamps = getRecTimeStamps(rec)

        userGrid, recGrid = getOverlapForCurrentRide(rec, user, recTimeStamps, gridcells)

        score = calculateScore(recGrid, userGrid)

        score2 = calculateScore2(recGrid, user, edgeLength, gridcells)

        allScores.append([name, score, score2,  user[-1][2], rec[-1][2], user[-1][3], rec[-1][3]])

    frame = df(allScores, columns = ['Ride','Percentage Overlap', 'Percentage Overlap - One Grid Over', 'User Ride Duration', 'Recommended Ride Duration', 'User Ride Distance', 'Recommended Ride Distance'])
    frame.to_csv("results.csv", index = False)

if __name__ == '__main__':
    main()