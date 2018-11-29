########### This program to indicate whether a point is within a city's borders on a 2-dimensional grid (X and Y axes) or not ##############

import csv
from collections import  defaultdict
import numpy as np
import os.path



def ReadaingCitiesCoordinatesFromCSV():

    columns = defaultdict(list)
    # get the list of cities from the csv file
    with open('cities.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)  # read rows into a dictionary format
        for row in reader:  # read a row as {column1: value1, column2: value2,...}
            for (k, v) in row.items():  # go over each column name and value
                columns[k].append(v)  # append the value into the appropriate list

    column_name = columns['Name']
    column_TopLeft_X = list(map(int,columns['TopLeft_X']))
    column_TopLeft_Y = list(map(int,columns['TopLeft_Y']))
    column_BottomRight_X= list(map(int,columns['BottomRight_X']))
    column_BottomRight_Y = list(map(int,columns['BottomRight_Y']))

    return column_name, column_TopLeft_X ,column_TopLeft_Y,column_BottomRight_X, column_BottomRight_Y

def ReadaingPointsCoordinatesFromCSV():

    columns = defaultdict(list)
    # get the list of points from the csv file
    with open('points.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)  # read rows into a dictionary format
        for row in reader:  # read a row as {column1: value1, column2: value2,...}
            for (k, v) in row.items():  # go over each column name and value
                columns[k].append(v)  # append the value into the appropriate list

    column_ID = columns['ID']
    column_X = list(map(int,columns['X']))
    column_Y = list(map(int,columns['Y']))

    return column_ID,column_X,column_Y

#### concatenate the x coordinates list and y coordinates list in single list
def Concatenate_X_Y_Coordinates(X,Y):
    #X = X coordinate  , Y = Y coordinate
    concatenateList = (np.column_stack((X,Y))).tolist()

    return concatenateList

#### sort the cities based on the closest one to the origin point
def SortCities(FirstPointList,SecondPointList,NameList):
    # NameList : cities Names , FirstPointList : TopLeft Coordinates , SecondPointList : BottomRight Coordinates
    FirstPointList, SecondPointList , NameList = zip(*sorted(zip(FirstPointList,SecondPointList,NameList)))

    return FirstPointList,SecondPointList,NameList

#### Check whether a given point inside a rectangle or not
def CheckPointInsideRectangleOrNot(X_Point,Y_Point,X_TOPLEFT,X_BOTTOMRIGHT,Y_TOPLEFT,Y_BOTTOMRIGHT):
    #X_Point , Y_Point : coordinates of point
    #X_TOPLEFT,Y_TOPLEFT,X_BOTTOMRIGHT,Y_BOTTOMRIGHT : coordinates of city (Boundary of rectangle )

    if ((X_TOPLEFT <= X_Point <= X_BOTTOMRIGHT) and (Y_TOPLEFT <= Y_Point <= Y_BOTTOMRIGHT )):
        Flag = True
    else:
        Flag = False

    return Flag

def WritingOutputToCSV(id,x,y,city):
    file_exists = os.path.isfile("output_points.csv")
    with open("output_points.csv", "a", newline='', encoding='utf-8') as resultFile:  # open input file for reading

        # writer = csv.writer(resultFile)
        writer = csv.DictWriter(resultFile,
                                fieldnames=["ID","X","Y","CityName"])
        if not file_exists:
            writer.writeheader()  # file doesn't exist yet, write a header

        spamwriter = csv.writer(resultFile)

        spamwriter.writerow([id,x,y,city])

    resultFile.close()



##### Reading Cities Coordinates from csv
CityNameLists,TopLeft_XList,TopLeft_YList,BottomRight_XList,BottomRight_YList = ReadaingCitiesCoordinatesFromCSV()

#### Reading Points Coordinates from csv
PointID,Point_XList,Point_YList = ReadaingPointsCoordinatesFromCSV()

#### creating TopLeft list consists of all points of cities on the TopLeft corner
TopLeftLists = Concatenate_X_Y_Coordinates(TopLeft_XList,TopLeft_YList)

#### creating Bottom Right list consists of all points of cities on the BottomRight corner
BottomRightLists = Concatenate_X_Y_Coordinates(BottomRight_XList,BottomRight_YList)

#### sorting the TopLeftList, BottomRightList and CityNameList
TopLeftLists,BottomRightLists,CityNameLists = SortCities(TopLeftLists,BottomRightLists,CityNameLists)

PointsLists = Concatenate_X_Y_Coordinates(Point_XList,Point_YList)





#### iterate on all given points
for point_list,ID in zip(PointsLists,PointID):
    #this list that will contain all cities that belongs to point
    ListOfCitiesContainingPoint = []
    ### Read the coordinates (x,y) of given  point
    Point_X = point_list[0]
    Point_Y = point_list[1]
    #### read the coordinates (x,y) of city
    for TopLeft_List,BottomRight_List,CityName in zip(TopLeftLists,BottomRightLists,CityNameLists):
        #Flag to check if the list that contains cities that belongs to point is empty or not
        FlagListOfCities = False


        X_Top = TopLeft_List[0]
        Y_Top = TopLeft_List[1]

        Y_Bottom = BottomRight_List[1]
        X_Bottom = BottomRight_List[0]

        #check if the city is within this rectangle or not
        CheckFlag = CheckPointInsideRectangleOrNot(Point_X,Point_Y,X_Top,X_Bottom,Y_Top,Y_Bottom)
        #check if the point in the current city
        if CheckFlag == True:
            #if the city contains the point append the city to the list
            ListOfCitiesContainingPoint.append(CityName)
            FlagListOfCities = True
            continue

        #check if the point in the next city or not
        if (CheckFlag == False) and (FlagListOfCities == True):
            break

    #check if the point don't belong to any city so append a "None " to the list
    if not(ListOfCitiesContainingPoint):
        ListOfCitiesContainingPoint.append("None")

    if len(ListOfCitiesContainingPoint) == 1:
        ListOfCitiesContainingPoint = ListOfCitiesContainingPoint[0]

    WritingOutputToCSV(ID,Point_X,Point_Y,ListOfCitiesContainingPoint)









