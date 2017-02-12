# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 12:07:52 2017

@author: Riggs
"""

import numpy as np
import os
import random as r
import math as m
import Battlecode as b

def Reclaim_land():
    print('Bring nature back to the world')
    return()
    
def Attack_city():
    print('**************** Preparing for Battle **********************')    
    selection = 10000
    while action !=0:
        View_cities()
        selection = int(input("Which city would you like to liberate? 0 to exit\n"))
        #action input then loads population breakdown into a new army matrix and file
        if selection == 0:
            break
        Lookup_city(selection)
        Army_stat = np.array(['Number',"Type",
                                  'HP','AC','Hit Bonus','Dmg Bonus',
                                  'Dmg rng','Crit','Exp','Pos'])
        for i in range(1,len(Army)):
            if Army[i][1] == 'Sold1' or Army[i][1] =='Sold2' or Army[i][1] =='Sold3' or Army[i][1] =='Sold4':
                Army_stat = np.vstack((Army_stat,Army[i]))
        print('Here are your attacking units\n',Army_stat)
        np.savetxt('Enemy.csv',Army_stat,fmt='%.20s',delimiter = ",")
        
        confirm = str.lower(input('Are you sure? y/n '))
        
        if confirm == 'y':
            print('Let the siege begin!')
            
            #Creates the city army based on the City list data            
            guard_cnt = int(city[5])
            conscripts_cnt = int(city[6])
            Warrior_cnt = int(city[9])
            Encounter_stat = np.array(['Number',"Type",
                                       'HP','AC','Hit Bonus','Dmg Bonus',
                                       'Dmg rng','Crit','Exp','Pos'])
            unit_stat = Lookup_unit('Guards','City',guard_cnt)
            Encounter_stat = np.vstack((Encounter_stat,unit_stat))
            unit_stat = Lookup_unit('Conscripts','City',conscripts_cnt)
            Encounter_stat = np.vstack((Encounter_stat,unit_stat))
            unit_stat = Lookup_unit('Warriors','City',Warrior_cnt)
            Encounter_stat = np.vstack((Encounter_stat,unit_stat))
            np.savetxt('Ally.csv', Encounter_stat,fmt='%.20s', delimiter=",")  
            
            result = b.battle('Ally.csv','Enemy.csv',1)
            
            City_Army = np.genfromtxt('Ally.csv', dtype = str, delimiter = ",")
            Army_stat = np.genfromtxt('Enemy.csv', dtype = str, delimiter = ",")
            for i in range(1,len(Army)):
                try:                
                    if Army_stat[i][1]==Army[i][1]:
                        Army[i] = Army_stat[i]
                except:
                    break
            
            city[5] = City_Army[1][0] #updates number of guards in city
            city[6] = City_Army[2][0] #updates number of conscripts in city
            city[9] = City_Army[3][0] #updates number of warriors in city
            known_city[5] = City_Army[1][0] #updates number of known guards in city
            known_city[6] = City_Army[2][0] #updates number of known conscripts in city
            known_city[9] = City_Army[3][0] #updates number of known warriors in city
            total_exp = 0
            
            for i in range(1,len(Encounter_stat)):
                total_exp += int(Encounter_stat[i][8])
           
            if result[0]==1:
                print('Your army has been DEFEATED. You have fallen back to the last city')
                Import_armyfile('Enemy army.csv')
                View_army()
                gain_xp(total_exp,'s')
                
            elif result[0]==0:
                print('Your army has been Victorious. You have taken ', city[1])
                Import_armyfile(os.path.join(gamestate,'Enemy army.csv'))
                View_army()
                gain_xp(total_exp,'s')
                #Conversion of the populace
                
                print('\n Let the conversion of ',city[1],' begin\n')
                symp_conv = int(city[8])
                print(symp_conv,' sympathizers have joined your army as level 1 soliders.')                
                for i in range(3):
                    print('You have ' , druids_available,',druids available')
                    print('There are:\n')
                    print(city[10],' commoners')
                    print(city[7],' scholars')
                    print(city[5],' guards')
                    print(city[6],' conscripts')
                    print(city[9],' warriors')
                    time = m.ceil((int(city[10])+int(city[7])+int(city[5])+int(city[6])+int(city[9]))/16)
                    print('\n that are in need of conversion. It will take ',time,' days')
                    confirm = 'x'                    
                    while confirm != 'y' and confirm != 'n':
                        confirm = str.lower(input('Would you like to attempt to convert? Otherwise we will just kill them? y/n '))
                        if confirm == 'y':
                            commoner_conv = m.floor(int(city[10])*(r.randint(1,20)+18-12)/100)
                            scholar_conv = m.floor(int(city[7])*(r.randint(1,20)+18-16)/100)
                            guard_conv = m.floor(int(city[5])*(r.randint(1,20)+18-15)/100)
                            conscript_conv = m.floor(int(city[6])*(r.randint(1,20)+18-14)/100)
                            warrior_conv = m.floor(int(city[6])*(r.randint(1,20)+18-18)/100)
                            print('You have converterted:\n')
                            print(commoner_conv,' commoners to level 1 soliders')
                            print(scholar_conv,' scholars to level 1 druids')
                            print(guard_conv,' guards to level 2 soldiers')
                            print(conscript_conv,' conscripts to level 1 soliders')
                            print(warrior_conv,' warriors to level 3 soldiers')
                            print('\n You have ', (2-i), ' days left to convert the rest of the population')
                        elif confirm == 'n':
                            break
                        else:
                            print('That is not an acceptable answer')
                    #updates army numbers
                    for j in range(1,len(Army)):
                        if Army[j][1] == 'Sold1':
                            Army[j][0] = int(Army[j][0])+symp_conv+commoner_conv+conscript_conv
                            symp_conv = 0
                        elif Army[j][1] == 'Sold2':
                            Army[j][0] = int(Army[j][0])+guard_conv
                        elif Army[j][1] == 'Sold3':
                            Army[j][0] = int(Army[j][0])+warrior_conv
                        elif Army[j][1] == 'Druid1':
                            Army[j][0] = int(Army[j][0])+scholar_conv
                            
                    #update city numbers
                    city[10] = int(city[10])-commoner_conv
                    city[7] = int(city[7]) - scholar_conv
                    city[5] = int(city[5]) - guard_conv
                    city[6] = int(city[6])- conscript_conv
                    city[9] = int(city[9]) - warrior_conv
                    city[8] = 0
                
                #Sets pop to zero. Killed the rest
                print('You killed the remaining population')                
                city[10] = 0
                city[7] = 0
                city[5] = 0
                city[6] = 0
                city[8] = 0
                city[9] = 0
                known_city[10] = 0
                known_city[7] = 0
                known_city[5] = 0
                known_city[6] = 0
                known_city[8] = 0
                known_city[9] = 0
                                                           
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
    while selection != 0:
        View_cities()
        selection = int(input('Which city would you like to scout? 0 to exit.'))    
        if selection == 0:
            break
        Lookup_city(selection)
        if city.size:
            scouts = int(input('How many scouts will you send? '))
            size = int(city[4])
            time= size/(scouts*100000)
            randmin= .5+((scouts/10)-(time/100))
            randmax= 1.5-((scouts/10)-(time/100))
            accuracy =int((1-randmin)*100)
            print('Scouting will take',int(time),'days with +/- ',accuracy,'% accuracy.')
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
                break
            elif confirm == 'n':
                print('Look again at the cities')
            else:
                print()
    print()
    return()
    
def Gain_support():
    print('****************Gain some supporters*******************')
    selection = 1000    
    druids =1000
    soldiers = 1000
    while selection != 0:
        View_cities()
        selection = int(input('Which city would you like to gain support for? 0 to exit.'))    
        if selection == 0:
            break
        Lookup_city(selection)
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
            confirm = str.lower(input('Are you sure? (y/n) '))
            if confirm == 'y':
                print('\n Your mission is off!')
                area = int(city[4])/43560 #land area in acres
                Guards = int(city[5])
                Scholars = int(city[7])
                Symp = int(city[8])
                Commoner = int(city[10])
                Encounter = ((druids+soldiers)/area)*(Scholars/area)
                days = 0
                total_added = 0
                Guards_killed = 0
                soldiers_killed = 0
                for i in range(time):
                    if r.uniform(0,1) < Encounter and Guards>0:
                        #Sets up guard encounter
                        attackers = m.ceil(Guards/area)
                        Encounter_stat = np.array(['Number',"Type",
                                       'HP','AC','Hit Bonus','Dmg Bonus',
                                       'Dmg rng','Crit','Exp','Pos'])
                        unit_stat = Lookup_unit('Guards','City',attackers)
                        Encounter_stat = np.vstack((Encounter_stat,unit_stat)) 
                        np.savetxt('Ally.csv', Encounter_stat,fmt='%.20s', delimiter=",")
                        
                        #Sets up soldier and druid stat blocks
                        Encounter_stat = np.array(['Number',"Type",
                                       'HP','AC','Hit Bonus','Dmg Bonus',
                                       'Dmg rng','Crit','Exp','Pos'])
                        unit_stat = Lookup_unit('ELevel1','Enemy',soldiers)
                        Encounter_stat = np.vstack((Encounter_stat,unit_stat))
                        unit_stat = Lookup_unit('Druid1','Enemy',druids)
                        Encounter_stat = np.vstack((Encounter_stat,unit_stat))
                        np.savetxt('Enemy.csv', Encounter_stat,fmt='%.20s', delimiter=",")                       
                        
                        #Uses battlecode to determine outcome
                        result = b.battle('Ally.csv','Enemy.csv',1)
                        print('Day ',(days+1),':Your troops got attacked', result[2],' survived')
                        g_kill = attackers - result[1]
                        s_kill = (druids + soldiers - result[2])
                        Guards -= g_kill
                        soldiers -= s_kill
                        Guards_killed += g_kill
                        soldiers_killed += s_kill
                    else:
                        print('Day ',(days+1),': Preaching in the city')
                        convert_chk = 0
                        for i in range(druids):                  
                            convert_chk = r.randint(1,5)/100
                            convert_chk +=convert_chk
                        added_symp = m.ceil(convert_chk*Commoner)
                        Symp += added_symp
                        Commoner -= added_symp
                        total_added += added_symp
                    #update city
                   
                    if soldiers <=0:
                        print('All your soldiers were killed. The druids returned early')
                        break
                    days +=1
                
                city[5] = Guards
                city[8] = Symp
                city[10] = Commoner
                try: #in case the place they know nothing
                    known_city[5] = int(known_city[5])-Guards_killed
                    known_city[8] = int(known_city[8])+total_added
                    known_city[10] = int(known_city[10])-total_added
                except:
                    print()
                    
                Army[1][0] = int(Army[1][0])-soldiers_killed               
                print('Your druids have retuned after ', days,' days.')
                print('You have gained ', total_added,' sympathizers in ', city[1])
                print()
                break
            elif confirm == 'n':
                print('Look again at the cities')
            else:
                print()     
                  
    return()
    
def View_army():
    print("Here's the troop breakdown\n")
    print(Army,'\n')
    return()

def View_cities():
    global Known_cities
    print("Here's what you know about the cities\n")
    print(Known_cities,'\n') 
    return()
    
def Import_armyfile(armyfile):
    global soldiers_available 
    global druids_available    
    global Army
    
    soldiers_available  = 0
    druids_available =0
    druid_power = 0
    Army = np.genfromtxt(armyfile, dtype = str, delimiter = ',')
    for i in range(len(Army)):
        if Army[i][1] == 'Sold1' or Army[i][1] == 'Sold2' or Army[i][1] == 'Sold3' or Army[i][1] == 'Sold4':
            soldiers_available = int(Army[i][0])
        if Army[i][1] == 'Druid1' or Army[i][1] == 'Druid2' or Army[i][1] == 'Druid3' or Army[i][1] == 'Druid4':
            druids_available = int(Army[i][0])
            for j in range(len(Army_units)):
                if Army_units[j][0]=='Druid1':
                    druid_power += (int(Army[i][0])*int(Army_units[j][1]))
                if Army_units[j][0]=='Druid2':
                    druid_power += (int(Army[i][0])*int(Army_units[j][1]))
                if Army_units[j][0]=='Druid3':
                    druid_power += (int(Army[i][0])*int(Army_units[j][1]))
                if Army_units[j][0]=='Druid4':
                    druid_power += (int(Army[i][0])*int(Army_units[j][1]))
    return()
    
def Lookup_unit(unit, side, count):
    if side == 'Enemy':
        Table = Army_units
    if side == 'City':
        Table = city_units
    found = 0    
    for j in range(len(Table)):    
        if Table[j][0] == unit:
            found = 1
            unit_lvl = int(Table[j,1])
            unit_exp = int(290.95*m.e**(0.3466*(unit_lvl)))
            HP = int(Table[j][2])
            AC = int(Table[j][3])
            HitBonus = int(Table[j][4])
            DmgBonus = int(Table[j][5])
            DmgRng = int(Table[j][6])
            Crit = int(Table[j][7])
                    
            Exp = int(count*unit_exp)

            unit_stat = np.array([count,unit,
                            HP,AC,HitBonus,DmgBonus,DmgRng,
                            Crit,Exp,0])
    if found == 1:
        return(unit_stat)  
    else:
        print('Cannot find a unit by that name')
        return()

def Lookup_city(selection):
    global known_city
    global city
    for i in range(1,len(Known_cities)):
        if selection == int(Known_cities[i][0]):
            known_city = Known_cities[i]
            print(known_city)
        if selection == int(Cities[i][0]):
            city = Cities[i]
    
def gain_xp(exp,unit):
    unit_cnt = 0
    if unit == 's':
        for i in range(1,len(Army)):
            if Army[i][1] == 'Sold1' or Army[i][1] == 'Sold2' or Army[i][1] == 'Sold3' or Army[i][1] == 'Sold4':
                unit_cnt += int(Army[i][0])
        unit_exp = exp/unit_cnt
        for i in range(1,len(Army)):
            if Army[i][1] == 'Sold1' or Army[i][1] == 'Sold2' or Army[i][1] == 'Sold3' or Army[i][1] == 'Sold4':
                Army[i][8] = int(Army[i][8])+unit_exp
    elif unit == 'd':
        for i in range(1,len(Army)):
            if Army[i][1] == 'Druid1' or Army[i][1] == 'Druid2' or Army[i][1] == 'Druid3' or Army[i][1] == 'Druid4':
                unit_cnt += int(Army[i][0])
        unit_exp = exp/unit_cnt
        for i in range(1,len(Army)):
            if Army[i][1] == 'Druid1' or Army[i][1] == 'Druid2' or Army[i][1] == 'Druid3' or Army[i][1] == 'Druid4':
                Army[i][8] = int(Army[i][8])+unit_exp
    else:
        print('No units of that type')
    
    return()
    
def Save_game():
    global gamestate

    gamestate = str.lower(input('Save game as:'))
    if not os.path.isdir(gamestate):    
        os.makedirs(gamestate)
    np.savetxt(os.path.join(gamestate,'City list.csv'), Cities, fmt='%.20s', delimiter = ',')
    np.savetxt(os.path.join(gamestate,'Enemy Army.csv'), Army, fmt='%.20s', delimiter = ',')
    np.savetxt(os.path.join(gamestate,'Known Cities.csv'),Known_cities,  fmt='%.20s',  delimiter = ',')
    
def load_game():
    global Army
    global Cities
    global city_units
    global Army_units
    global Known_cities
    global gamestate
    
    game = 0
    city_units = np.genfromtxt('City unit stats.csv', dtype = str, delimiter = ',')
    Army_units = np.genfromtxt('Army unit stats.csv', dtype = str, delimiter = ',')
    
    
    while game ==0:    
        gamestate = str.lower(input('Load game as (0 for new game):'))
        if gamestate == '0':
            Cities = np.genfromtxt(os.path.join('newgame','City list.csv'), dtype = str, delimiter = ',')
            Import_armyfile(os.path.join('newgame','Enemy army.csv'))                          
            Known_cities = np.genfromtxt(os.path.join('newgame','Known Cities.csv'), dtype = str, delimiter = ',')  
            Save_game()
            game = 1
        else:
            try:
                Cities = np.genfromtxt(os.path.join(gamestate,'City list.csv'), dtype = str, delimiter = ',')
                Import_armyfile(os.path.join(gamestate,'Enemy army.csv'))                         
                Known_cities = np.genfromtxt(os.path.join(gamestate,'Known Cities.csv'), dtype = str, delimiter = ',')  
                game = 1
            except:
                print('Cannot find file')
                
    return()       
#Reference materials


load_game()

action = 0
while action != 6:
    action = int(input('What would you like to do?\n'
                   '1. Scout a city\n'
                   '2. Gain support in a city\n'
                   '3. Attack a city\n'
                   '4. View army\n'
                   '5. View cities\n'
                   '6. End session and save\n'))

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
        Save_game()
        print('Until next time')
        break
    else:
        print('You need to pick an action')
    