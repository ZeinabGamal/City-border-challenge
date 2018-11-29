# City-border-challenge
This program to Check whether a given point inside a rectangle or not

## The steps of the algorithm :
1- Reading cities and points details from csv.
2-Sorting the cities based on the closest one to the origin point.
3-then check if th point inside the rectangle or not using this relation :
 #### For example : 
 Given a rectangle with points (x1,y1) and (x2,y2), a point (x,y) is within that rectangle if x1 < x < x2 and y1 < y < y

4- if the point insides the rectangle so check the next city so it maybe have the same x coordinates and intersect with the previous city 5- if not so the point is within one city .

6- Finally , writing all the cities that contain point.
