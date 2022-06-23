import pandas as pd
import matplotlib.pyplot as plt
import descartes
import geopandas as gpd
from shapely.geometry import Point, Polygon
import shapely
import glob
import numpy as np
from haversine import haversine, inverse_haversine, Direction
from math import sqrt, pi

#START OF DEF
def createGrid(edgeLength):
    #Producing grid cells
    gridcells = []
    columns = []
    xmin =  13.090246535756732
    ymin =  52.340436617775886
    xmax =  13.756924989951091
    ymax =  52.659932312168635
    topLeft = (ymax, xmin)

    hyp = sqrt(edgeLength**2 + edgeLength**2)

    #Make first column
    while(topLeft[0] > ymin):
        newSquareBR = inverse_haversine(topLeft, hyp, 135*(pi/180))
        sqxmin = topLeft[1]
        sqxmax = newSquareBR[1]
        sqymin = newSquareBR[0]
        sqymax = topLeft[0]
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

            #create grid cell and add to gridcell array
            square = shapely.geometry.box(sqxmin, sqymin, sqxmax, sqymax)
            gridcells.append(square)

            #get coordinates and flip them
            coords = list(square.exterior.coords)
            temp = []
            for i in range(len(coords)):
                temp.append((coords[i][1], coords[i][0]))
            coords = temp 

            topLeft = coords[1]

    return gridcells
#END OF DEF


#START OF DEF
def findClosest(user, timeStamp):
    absUser = np.abs(user - timeStamp)
    index = absUser.argmin()
    return index, user[index]
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
    path = "FilteredDataNewTime" + path + "filtered.csv"
    return path
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
    score  = 100 * (match / len(recGrid))
    return score
#END OF DEF








def main():
    # #User and reccomeded path data converted to numpy arrays
    # user = pd.read_csv("FilteredDataNewTime\VM2_-76660491-filtered.csv")
    # recc = pd.read_csv("geoJSONCSV\VM2_-76660491-efficientpath.csv")

    # user = user.to_numpy()
    # recc = recc.to_numpy()

    # gridcells = createGrid()

    # #Putting User Time Stamps into a single array
    # reccTimeStamps = []
    # for i in range(len(recc)):
    #     reccTimeStamps.append(recc[i][2])
    # reccTimeStamps = np.array(reccTimeStamps)

   

    # #METRIC STUFF
    # userEndTimeStamp = user[-1][2]
    # reccEndTimeStamp = recc[-1][2]
    # userGrid = []
    # reccGrid = []


    # #Find gridcells that eachpoint is contained within
    # for i in range(len(user)):
    #     userCurrentTimeStamp = user[i][2]
    #     userCurrentPoint = Point(user[i][1], user[i][0])
    #     reccIndex, reccClosestTime = findClosest(reccTimeStamps, userCurrentTimeStamp)
    #     reccCurrentPoint = Point(recc[reccIndex][1], recc[reccIndex][0])

    #     reccGrid.append(findContainingGrid(reccCurrentPoint, gridcells))
    #     userGrid.append(findContainingGrid(userCurrentPoint, gridcells))

    #     if(reccClosestTime == userEndTimeStamp):
    #         break


    # #Metric
    # match = 0

    # for j in range(len(reccGrid)):
    #     if(reccGrid[j] == userGrid[j]): 
    #         match = match + 1

    # score  = 100 * (match / len(reccGrid))

    # print(score)

        

    
    #All files thing
    # DO THIS TMRW, MAKE METRICS FOR ALL FILES
    # HAVE A METRIC PER RIDE AND HAVE A METRIC DESCRIBINGF ALL RIDES

    allScores = []

    allReccomendedRides = glob.glob('geoJSONCSV\*')
    for file in allReccomendedRides:
        userDirectoryPath = userDirectory(file)

        rec = pd.read_csv(file)
        user = pd.read_csv(userDirectoryPath)

        user = user.to_numpy()
        rec = rec.to_numpy()
        
        gridcells = createGrid(4)

        recTimeStamps = getRecTimeStamps(rec)

        userGrid, recGrid = getOverlapForCurrentRide(rec, user, recTimeStamps, gridcells)

        score = calculateScore(recGrid, userGrid)

        allScores.append([file, score])

    for i in range(len(allScores)):
        print(allScores[i])

    print(len(allScores))

if __name__ == '__main__':
    main()