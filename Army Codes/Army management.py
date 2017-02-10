# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 12:07:52 2017

@author: Riggs
"""

import numpy as np
import os
import random as r

def Reclaim_land():
    print('Bring nature back to the world')
    return()
    
def Attack_city():
    selection = 10000
    while action !=0:
        View_cities()
        selection = int(input("Which city would you like to liberate? 0 to exit\n"))
        #action input then loads population breakdown into a new army matrix and file
        if selection == 0:
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
    print('****************Scouting*******************')
    selection = 1000    
    city =[]   
    while selection != 0:
        View_cities()
        selection = int(input('Which city would you like to scout? 0 to exit.'))    
        if selection == 0:
            break
        for i in range(1,len(Known_cities)):
            try:            
                if selection == int(Known_cities[i][0]):
                    print(Known_cities[i]) 
                if selection == int(Cities[i][0]):
                    city = Cities[i]
            except:
                print()
        if city.size:
            scouts = int(input('How many scouts will you send? '))
            size = int(city[4])
            time= size/(scouts*100000)
            randmin= .5+((scouts/10)-(time/100))
            randmax= 1.5-((scouts/10)-(time/100))
            accuracy =int((1-randmin)*100)
            print('Scouting will take',time,'days with +/- ',accuracy,'% accuracy.')
            confirm = str.lower(input('Are you sure? (y/n) '))
            if confirm == 'y':
                print('The scouts are off!')
                gained_intel =[city[0],city[1],city[2],city[3],city[4],
                               int(r.uniform(randmin,randmax)*int(city[5])),
                               int(r.uniform(randmin,randmax)*int(city[6])),
                               int(r.uniform(randmin,randmax)*int(city[7])),
                               int(r.uniform(randmin,randmax)*int(city[8])),
                               int(r.uniform(randmin,randmax)*int(city[9])),
                               int(r.uniform(randmin,randmax)*int(city[10]))]
                print('Your scouts returned. Here is what they found')
                print(gained_intel)
                for i in range(1,len(Known_cities)):
                    if int(gained_intel[0])==int(Known_cities[i][0]):
                        Known_cities[i] = gained_intel
                        np.savetxt('Known Cities.csv', Known_cities,fmt='%.20s', delimiter=",")
                break
            elif confirm == 'n':
                print('Look again at the cities')
            else:
                print()
    return()
    
def Gain_support():
    print('****************Gain some supporters*******************')
    selection = 1000    
    city =[] 
    druids =1000
    soldiers = 1000
    while selection != 0:
        View_cities()
        selection = int(input('Which city would you like to gain support for? 0 to exit.'))    
        if selection == 0:
            break
        for i in range(1,len(Known_cities)):
            try:            
                if selection == int(Known_cities[i][0]):
                    print(Known_cities[i]) 
                if selection == int(Cities[i][0]):
                    city = Cities[i]
            except:
                print()
        if city.size:
            while druids > druids_available:
                druids = int(input('How many druids will you send to spread your word?'))
                if druids > druids_available:
                    print('You only have ', druids_available, 'available. Try again.')
            while soldiers > soldiers_available:
                soldiers = int(input('How many soldiers will you send to protect your druids? '))
                if soldiers > soldiers_available:
                    print('You only have ', soldiers_available, 'available. Try again.')
            time = int(input('How long should they stay in the city? '))
            print(druids,' driuds and ', soldiers, ' soldiers are off for ',time, 'days to add to your flock.')

            Guards = int(city[5])
            Scholars = int(city[7])
            Encounter = 
    return()
    
def View_army():
    print("Here's the troop breakdown")
    print(Army)
    return()

def View_cities():
    global Known_cities
    print("Here's what you know about the cities")
    Known_cities = np.genfromtxt('Known Cities.csv', dtype = str, delimiter = ',')
    print(Known_cities) 
    return()
    
def Import_armyfile(armyfile):
    global soldiers_available 
    global druids_available    

    soldiers_available  = 0
    druids_available =0
    
    Army = np.genfromtxt('Enemy army.csv', dtype = str, delimiter = ',')
    for i in range(len(Army)):
        if Army[i][1]=='ELevel1':
            soldiers_available = int(Army[i][0])
        if Army[i][1]=='Druid1':
            druids_available = int(Army[i][0])
    print(soldiers_available,druids_available)        
    return()

#Reference materials
global Army
global Cities
city_units = np.genfromtxt('City unit stats.csv', dtype = str, delimiter = ',')
Army_units = np.genfromtxt('Army unit stats.csv', dtype = str, delimiter = ',')
Cities = np.genfromtxt('City list.csv', dtype = str, delimiter = ',')
Import_armyfile('Enemy army.csv')                           

action = 0
while action != 6:
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
    