# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 12:07:52 2017

@author: Riggs
"""

import numpy as np
import os


def Reclaim_land():
    print('Bring nature back to the world')
    return()
    
def Attack_city():
    action = 10000
    while action !=0:
        View_cities()
        action = int(input("Which city would you like to liberate?"' 0 to exit\n'))
        #action input then loads population breakdown into a new army matrix and file
        if action == 0:
            break
        confirm = str.lower(input('Are you sure? y/n \n'))
        if confirm == 'y':
            print('Let the siege begin!')
            #Print armies
            #run simulation
            #print aftermath of battle
            #Interrogations
            break
        elif confirm == 'n':
            print('Look again at the cities')
        else:
            print()

    #Print out city list    
    return()
    
def Scout():
    print('Scouting')
    return()
    
def Gain_support():
    print('Going to find sympathizers')

    return()
    
def View_army():
    print("Here's the troop breakdown")

    return()

def View_cities():
    print("Here's what you know about the cities")
    return()
    
def Import_armyfile(armyfile):
    
    return()

#Reference materials
    #Import city list
    #Import initial army
    #Import Unit List
    #Import City unit list


action = 0
while action != 5:
    action = int(input('What would you like to do?\n'
                   '1. Scout a city\n'
                   '2. Gain suuport in a city\n'
                   '3. Attack a city\n'
                   '4. View army\n'
                   '5. View cities\n'
                   '6. End session\n'))

    if action ==1:
        Scout()
    elif action ==2:
        Gain_support()
    elif action ==3:
        Attack_city()
    elif action ==4:
        View_army()
    elif action ==5:
        View_cities()
    elif action ==6:
        print('Until next time')
        break
    else:
        print('You need to pick an action')
    