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
import Map

def Reclaim_land():
    print('\n******* Bring nature back to the world **************\n')
    area_left = int(city[4])
    dev= int(city[2])
    time = m.ceil((area_left*dev)/(druid_power*2400))
    print('Reclaimation should take ',time, 'days')
    for i in range(time):
        area_reclaimed = (druid_power*2400)/dev
        XP = area_reclaimed/100
        gain_xp(XP,'d')
        area_left -= area_reclaimed
        time = m.ceil((area_left*dev)/(druid_power*2400))
        total_time = i+1
    print(city[1],' has been reclaimed. It took ',total_time,' days')
    print()
    return()
    
def Attack_city():
    global roster
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
   
        for i in range(1,len(army)):
            if army[i][1] == 'Sold1' or army[i][1] =='Sold2' or army[i][1] =='Sold3' or army[i][1] =='Sold4':
                Army_stat = np.vstack((Army_stat,army[i]))
                
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
                        
            #counts type of units killed from the city army
            unique, counts = np.unique(result[3], return_counts = True)            
            city_killed = np.array([(key,val) for (key,val) in dict(zip(unique,counts)).items()],dtype=str)
            
            for i in range(len(city_killed)):
                if city_killed[i][0] == 'Guards':
                    city[5] = int(city[5])-1
                    known_city[5] = city[6] #updates number of known guards in city
                if city_killed[i][0] == 'Conscripts':
                    city[6] = int(city[6])-1
                    known_city[6] = city[6]
                if city_killed[i][0] == 'Warriors':
                    city[9] = int(city[9])-1
                    known_city[9] = city[9]            
                    
            update_army(result[4])
            View_army()
            
            total_exp = 0
            for i in range(1,len(Encounter_stat)):
                total_exp += int(Encounter_stat[i][8])
            
            gain_xp(total_exp,'s')

            if result[0]==1:
                print('Your army has been DEFEATED. You have fallen back to the last city')
               
            elif result[0]==0:
                print('Your army has been Victorious. You have taken ', city[1])
                
                #Conversion of the populace                
                print('\n Let the conversion of ',city[1],' begin\n')
                symp_conv = int(city[8])
                print(symp_conv,' sympathizers have joined your army as level 1 soliders.')                
                for i in range(3):
                    print('You have ' , druids_available,' druids available')
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

                    sold_conv = symp_conv + conscript_conv + commoner_conv
                    for j in range(sold_conv):
                        roster = np.vstack((roster,['Sold1',0,1300,1]))
                    for j in range(guard_conv):
                        roster = np.vstack((roster,['Sold2',0,3300,2]))                        
                    for j in range(warrior_conv):
                        roster = np.vstack((roster,['Sold3',0,6000,3]))
                    for j in range(scholar_conv):
                        roster = np.vstack((roster,['Druid1',0,1300,1]))
                    symp_conv = 0
                    update_army([])
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
                known_city[2] = city[2]
                known_city[3] = city[3]
                known_city[4] = city[4]
                Reclaim_land()
            break
        elif confirm == 'n':
            print('Look again at the cities')
        else:
            print()

    #Print out city list    
    return()

def Scout():
    global Known_cities
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
                               int(r.uniform(randmin,randmax)*int(city[10])),
                                0]
                print('Your scouts returned. Here is what they found')
                print(gained_intel)
                print()
                for i in range(1,len(Known_cities)):
                    if int(gained_intel[0])==int(Known_cities[i][0]):
                        Known_cities[i] = gained_intel
                
                for i in range(1,3):   
                    if Cities[selection+i][0] not in Known_cities[:,0]:
                        print('You have learned of a new city!',Cities[selection+i][1],'\n')
                        start = [city_loc[selection][1],city_loc[selection][2]] #update
                        end = [city_loc[selection+1][1],city_loc[selection+1][2]]
                        distance = Map.Travel_route(start, end)
                        new_city = [Cities[selection+i][0],Cities[selection+i][1],
                                     '','','','','','','','','',distance]
                        Known_cities = np.vstack((Known_cities,new_city))
                        
                View_cities()
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
    time = 0
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
            while time <=0:
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
                                       'Dmg rng','Crit','Exp','Level'])
                        unit_stat = Lookup_unit('Guards','City',attackers)
                        Encounter_stat = np.vstack((Encounter_stat,unit_stat)) 
                        np.savetxt('Ally.csv', Encounter_stat,fmt='%.20s', delimiter=",")
                        
                        #Sets up soldier and druid stat blocks
                        Encounter_stat = np.array(['Number',"Type",
                                       'HP','AC','Hit Bonus','Dmg Bonus',
                                       'Dmg rng','Crit','Exp','Level'])
                        unit_stat = Lookup_unit('Sold1','Enemy',soldiers)
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
                        update_army(result[4])

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
                
    
                print('Your druids have retuned after ', days,' days.')
                print('You have gained ', total_added,' sympathizers in ', city[1])
                print()
                break
            elif confirm == 'n':
                print('Look again at the cities')
            else:
                print()     
                  
    return()
    
def update_army(deadlist):
    global roster
    global druid_power
    global druids_available
    global soldiers_available
    global army
    
    for i in range(len(deadlist)):
       for j in range(1,len(roster)):
           if deadlist[i]==roster[j][0]:
               roster = np.delete(roster,j,axis=0)
               break
           
    #Counts instances of each type of unit in the roster, reports as array
    unique, counts = np.unique(roster[1:,0], return_counts = True)
    result = dict(zip(unique,counts))
    summary = np.array([(key,val) for (key,val) in result.items()],dtype=str)    

    #forms the summary array for viewing
    army = np.array(['Number','Type','HP','AC','Hit B.', 'Dmg.B', 'Dmg.Rng.','Crit','Exp','lvl'])

    for i in range(1,len(Army_units)):
        for j in range(len(summary)):               
            if summary[j][0] == Army_units[i][0]:
                temp = [summary[j][1]]
                temp = np.hstack((temp,Army_units[i]))
                army = np.vstack((army,temp))
    
    #counts soldiers and druids available
    soldiers_available  = 0
    druids_available = 0
    druid_power = 0
    
    for i in range(len(army)):
        if army[i][1]== 'Sold1' or army[i][1] == 'Sold2' or army[i][1] == 'Sold3' or army[i][1] == 'Sold4':
            soldiers_available += int(army[i][0])
        if army[i][1] == 'Druid1' or army[i][1] == 'Druid2' or army[i][1] == 'Druid3' or army[i][1] == 'Druid4':
            druids_available += int(army[i][0])
            druid_power += int(army[i][9])*int(army[i][0])
            
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
            unit_lvl = int(Table[j,8])
            unit_exp = int(290.95*m.e**(0.3466*(unit_lvl)))
            HP = int(Table[j][1])
            AC = int(Table[j][2])
            HitBonus = int(Table[j][3])
            DmgBonus = int(Table[j][4])
            DmgRng = int(Table[j][5])
            Crit = int(Table[j][6])
                    
            Exp = int(count*unit_exp)

            unit_stat = np.array([count,unit,
                            HP,AC,HitBonus,DmgBonus,DmgRng,
                            Crit,Exp,unit_lvl])
    if found == 1:
        return(unit_stat)  
    else:
        print('Cannot find a unit by that name')
        return()
    
def gain_xp(exp,unit):
    if unit == 's':
        unit_exp = int(exp/soldiers_available)
        for i in range(1,len(roster)):
            if roster[i][0] == 'Sold1' or roster[i][0] == 'Sold2' or roster[i][0] == 'Sold3' or roster[i][0] == 'Sold4':
                roster[i][1]=int(roster[i][1])+unit_exp #add experience to each unit
                if int(roster[i][1])>=int(roster[i][2]): #level up
                    lvl = int(roster[i][3])+1                    
                    roster[i][3] = lvl
                    roster[i][2] = 350*(lvl+1)**2 + 250*(lvl+1) - 600
                    roster[i][0] = "Sold"+str(lvl)
    elif unit == 'd':
        unit_exp = int(exp/druids_available)
        for i in range(1,len(roster)):
            if roster[i][0] == 'Druid1' or roster[i][0] == 'Druid2' or roster[i][0] == 'Druid3' or roster[i][0] == 'Druid4':
                roster[i][1]=int(roster[i][1])+unit_exp #add experience to each unit
                if int(roster[i][1])>=int(roster[i][2]): #level up
                    lvl = int(roster[i][3])+1                    
                    roster[i][3] = lvl
                    roster[i][2] = 350*(lvl+1)**2 + 250*(lvl+1) - 600
                    roster[i][0] = "Sold"+str(lvl)
    else:
        print('No units of that type')
    
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
    return()
    
def View_army():
    print("Here's the troop breakdown\n")
    print(army,'\n')
    return()

def View_cities():
    global Known_cities
    print("Here's what you know about the cities\n")
    print(Known_cities,'\n') 
    return()
    
def Save_game():
    global gamestate

    gamestate = str.lower(input('Save game as:'))
    if not os.path.isdir(gamestate):    
        os.makedirs(gamestate)
    np.savetxt(os.path.join(gamestate,'City list.csv'), Cities, fmt='%.20s', delimiter = ',')
    np.savetxt(os.path.join(gamestate,'Full Roster.csv'), roster, fmt='%.20s', delimiter = ',')
    np.savetxt(os.path.join(gamestate,'Known Cities.csv'),Known_cities,  fmt='%.20s',  delimiter = ',')
    
def load_game():
    global Army
    global Cities
    global city_units
    global Army_units
    global Known_cities
    global gamestate
    global exp_list
    global roster
    global city_loc
    global current_loc
    
    game = 0
    city_units = np.genfromtxt('City unit stats.csv', dtype = str, delimiter = ',')
    Army_units = np.genfromtxt('Army unit stats.csv', dtype = str, delimiter = ',')
    city_loc = np.genfromtxt('City locations.csv',dtype = int, delimiter = ",")
    while game ==0:    
        gamestate = str.lower(input('Load game as (0 for new game):'))
        if gamestate == '0':
            Cities = np.genfromtxt(os.path.join('newgame','City list.csv'), dtype = str, delimiter = ',')
            roster = np.genfromtxt(os.path.join('newgame','Full roster.csv'),dtype = str, delimiter = ",")
            update_army([])
            Known_cities = np.genfromtxt(os.path.join('newgame','Known Cities.csv'), dtype = str, delimiter = ',')  
            Save_game()
            game = 1
        else:
            try:
                Cities = np.genfromtxt(os.path.join(gamestate,'City list.csv'), dtype = str, delimiter = ',')
                roster = np.genfromtxt(os.path.join(gamestate,'Full roster.csv'),dtype = str, delimiter = ",")
                update_army([])
                Known_cities = np.genfromtxt(os.path.join(gamestate,'Known Cities.csv'), dtype = str, delimiter = ',')  
                game = 1
            except:
                print('Cannot find file')
    exp_list = [0,1300,3300,6000,10000,23000]    
    current_loc = np.argwhere(Known_cities == 'X')[0][0]
  
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
    