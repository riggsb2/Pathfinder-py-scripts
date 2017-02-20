# -*- coding: utf-8 -*-
"""
Created on Fri Nov 11 12:20:19 2016

@author: Riggs
"""

import numpy as np
import math as m

def Find_adjacent(location):
    #location is reported y,x. Vertical then horizantal
    adjacent = np.array([[location[0]-1,location[1]-1],
                        [location[0]-1,location[1]+0],
                        [location[0]+0,location[1]-1],
                        [location[0]+0,location[1]+1],
                        [location[0]+1,location[1]-1],
                        [location[0]+1,location[1]+0]])
    return(adjacent)                   

def Travel_route(startpoint, endpoint):
    global Map
    global Army_location
    
    #Map[endpoint[0],endpoint[1]] = '*'
    #show_map()
    Travel_location = startpoint
    time = 0
    while ((Travel_location[0] != endpoint[0]) or (Travel_location[1] != endpoint[1])):
        Next_hex = Find_adjacent(Travel_location)
        shortest = 100
        for i in range(len(Next_hex)):
            Y2 = abs(Next_hex[i][0]-endpoint[0])
            X2 = abs(Next_hex[i][1]-endpoint[1])
            D2 = m.sqrt(Y2**2+X2**2)
            if D2<shortest: 
                shortest = D2
                tile = i
        Travel_location = Next_hex[tile]
        time +=1
    return(time)

def move():
    global Army_location
    
    Destination = [int(x) for x in input('Where would you like to move?').split()]
    print(Destination)
    print('Trip will take',Travel_route(Destination),'days')
    confirm = str.lower(input('Would you like to move there?'))
    
    if confirm == 'y':
        Map[Army_location[0],Army_location[1]] = ''
        Army_location = Destination
        Map[Army_location[0],Army_location[1]] = 'Z'
    show_map()
    return()    
    
def show_map():
    #edit to center around the army
    for i in range(len(Map)):
        if i%2==0:
            for j in range(len(Map[i])):
                print('|','{:1}'.format(Map[i][j]),end='')
        else:
            print(' ',end='')
            for j in range(len(Map[i])):
                print('|','{:1}'.format(Map[i][j]),end='')
        print()
    print()  
  
#Sets up map  
Map= np.empty([80,80],dtype = str)
#Army_location = [5,4]
#Map[Army_location[0],Army_location[1]] = 'Z'
#show_map()
#move()