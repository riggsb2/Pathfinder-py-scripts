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
    global Journal
    global calendar
    print('\n******* Bring nature back to the world **************\n')
    area_left = int(city[4])
    dev= int(city[2])
    time = m.ceil((area_left*dev)/(druid_power*2400))
    print('Reclaimation should take ',time, 'days')
    for i in range(time):
        area_reclaimed = (druid_power*2400)/dev
        XP = area_reclaimed/100
        area_left -= area_reclaimed
        time = m.ceil((area_left*dev)/(druid_power*2400))
        total_time = i+1
        gain_xp(XP,'d')
        gain_xp(soldiers_available*idle_exp,'s')
        gain_xp(XP,'c')
        raid()

    calendar += total_time
    temp = np.array([calendar, 'Your druids have converted the city back to nature'])
    Journal = np.vstack((Journal,temp))
    print(city[1],' has been reclaimed. It took ',total_time,' days')
    print()
    return()
    
def Attack_city():
    global roster
    global Journal
    global calendar
    global current_loc
    global Known_cities
    global Cities
    global attack_date
    
    
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
            print('Let the siege begin!\n')
            travel_time =  Map.Travel_route(current_loc,[city_loc[selection][1],city_loc[selection][2]])               

            temp = [calendar,'Army is moving to '+ city[1]]
            Journal = np.vstack((Journal,temp))
            calendar += travel_time
            attack_date = calendar

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
                    city[5] = int(city[5])-int(city_killed[i][1])
                    known_city[5] = city[6] #updates number of known guards in city
                if city_killed[i][0] == 'Conscripts':
                    city[6] = int(city[6])-int(city_killed[i][1])
                    known_city[6] = city[6]
                if city_killed[i][0] == 'Warriors':
                    city[9] = int(city[9])-int(city_killed[i][1])
                    known_city[9] = city[9]            
                    
            if update_army(result[4]) == 0:
                load_game()
                break
            View_army()
            
            total_exp = 0
            for i in range(1,len(Encounter_stat)):
                total_exp += int(Encounter_stat[i][8])
            
            gain_xp(total_exp,'s')
            gain_xp(total_exp/100,'c')
            temp = [calendar,'Attacking the city']
            Journal = np.vstack((Journal,temp))
            calendar += int(round(result[5]/(24*60),0))
            
            print('\n The battle waged on for ', int(round(result[5],0)), ' minutes\n')
            print('During the battle', len(result[4]),' fell in the service of Mal')
            if result[0]==1:
                print('Your army has been DEFEATED. You have fallen back to the last city')
                
                temp = np.array([calendar, 'The army travels back to camp'])
                Journal = np.vstack((Journal,temp))
                calendar += travel_time
                temp = np.array([calendar, 'Your have returned defeated'])
                Journal = np.vstack((Journal,temp))
                
            elif result[0]==0:
                print('Your army has been Victorious. You have taken ', city[1])
                current_loc = [city_loc[selection][1],city_loc[selection][2]]
                update_distance()
                temp = [calendar, 'Your army has settled into ' + city[1]]
                Journal = np.vstack((Journal,temp))                
                
                #Conversion of the populace                
                print('\n Let the conversion of ',city[1],' begin\n')
                symp_conv = int(city[8])
                print(symp_conv,' sympathizers have joined your army as level 1 soliders.\n')                
                total_time = 0
                for i in range(3):
                    print('You have ' , druids_available,' druids available')
                    print('There are:\n')
                    print(city[10],' commoners')
                    print(city[7],' scholars')
                    print(city[5],' guards')
                    print(city[6],' conscripts')
                    print(city[9],' warriors')
                    population = int(city[10])+int(city[7])+int(city[5])+int(city[6])+int(city[9])
                    time = m.ceil(population/(16*0.5*druid_power))
                    print('\n that are in need of conversion. It will take ',time,' days')
                    confirm = 'x'                    
                    while confirm != 'y' and confirm != 'n':
                        confirm = str.lower(input('Would you like to attempt to convert? Otherwise we will just kill them? y/n '))
                        if confirm == 'y':
                            total_time +=time
                            moral_bonus = m.ceil((int(city[6])+int(city[6])+int(city[9]))/int(city[10])+(int(city[10])/100))
                            print(moral_bonus)
                            commoner_conv = conversion(int(city[10]),2+moral_bonus)
                            scholar_conv = conversion(int(city[7]),6+moral_bonus)
                            guard_conv = conversion(int(city[5]),5+moral_bonus)
                            conscript_conv = conversion(int(city[6]),4+moral_bonus)
                            warrior_conv =conversion(int(city[9]),6+moral_bonus)
                            total_conv = commoner_conv+scholar_conv+guard_conv+conscript_conv+warrior_conv
                            print('You have converterted:\n')
                            print(commoner_conv,' commoners to level 1 soliders')
                            print(scholar_conv,' scholars to level 1 druids')
                            print(guard_conv,' guards to level 2 soldiers')
                            print(conscript_conv,' conscripts to level 1 soliders')
                            print(warrior_conv,' warriors to level 3 soldiers')
                            print('\n You have ', (2-i), ' tries left to convert the rest of the population')
                            gain_xp(total_conv*100,'d')
                            gain_xp(total_conv,'c')
                        elif confirm == 'n':
                            commoner_conv =0
                            scholar_conv = 0
                            guard_conv = 0
                            conscript_conv = 0
                            warrior_conv = 0
                            break
                        else:
                            print('That is not an acceptable answer')
                    
                    druid_conv = 0
                    sold_conv = symp_conv + conscript_conv + commoner_conv

                    for j in range(commoner_conv):
                        if r.randint(1,100) <= comm_druid:
                            druid_conv+=1
                            sold_conv -=1
                    for j in range(sold_conv):
                        roster = np.vstack((roster,['Sold1',exp_list[1],exp_list[2],1]))
                    for j in range(guard_conv):
                        roster = np.vstack((roster,['Sold2',exp_list[2],exp_list[3],2]))                        
                    for j in range(warrior_conv):
                        roster = np.vstack((roster,['Sold3',exp_list[3],exp_list[4],3]))
                    for j in range(scholar_conv+druid_conv):
                        roster = np.vstack((roster,['Druid1',exp_list[1],exp_list[5],1]))
                    print(druid_conv,' commoners have shown connection to nature and have become Druids')
                    symp_conv = 0
                    update_army([])
                    #update city numbers
                    city[10] = int(city[10])-commoner_conv
                    commoner_esc = 0
                    for j in range(int(city[10])):
                        if r.randint(1,20)+m.ceil(int(city[10])/100)>r.randint(1,20)+m.ceil(int(soldiers_available)/100):
                            commoner_esc+=1
                    city[10] = int(city[10])-commoner_esc
                    city[7] = int(city[7]) - scholar_conv
                    city[5] = int(city[5]) - guard_conv
                    city[6] = int(city[6])- conscript_conv
                    city[9] = int(city[9]) - warrior_conv
                    city[8] = 0
                    Cities[selection+1][10] = int(Cities[selection+1][10])+commoner_esc
                    print(commoner_esc, ' of the population escaped during the night')
                
                temp = np.array([calendar, 'You spend days converting the masses'])
                Journal = np.vstack((Journal,temp))
                calendar += int(total_time)
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
                for i in range(1,3):   
                    if Cities[selection+i][0] not in Known_cities[:,0]:
                        print('You have learned of a new city!',Cities[selection+i][1],'\n')
                        start = current_loc
                        end = [city_loc[selection+i][1],city_loc[selection+i][2]]
                        distance = Map.Travel_route(start, end)
                        new_city = [Cities[selection+i][0],Cities[selection+i][1],
                                     Cities[selection+i][2],'',Cities[selection+i][4],
                                     '','','','','','',distance]
                        Known_cities = np.vstack((Known_cities,new_city))
            
            #Update security level of city win or lose
            
            for i in range(1,len(Cities)): 
                sec_lvl = int(Cities[i][3])
                if int(Cities[i][0])>=selection-2 and int(Cities[i][0])<=selection+2:
                    Cities[i][3]=int(Cities[i][3])+1 #update security lvl
                    sec_lvl = int(Cities[i][3])
                    guards = int(Cities[i][5])
                    conscript = int(Cities[i][6])
                    warrior = int(Cities[i][9])
                    commoners = int(Cities[i][10])

                    #updates disrtibution to account for growing concern
                    Cities[i][10]= commoners - m.ceil(commoners*sec_lvl*0.03)
                    Cities[i][6]= conscript + m.ceil(commoners*sec_lvl*0.03) - m.ceil(conscript*sec_lvl*0.02)
                    Cities[i][5]= guards + m.ceil(conscript*sec_lvl*0.02) - m.ceil(guards*sec_lvl*0.01)
                    Cities[i][9]= warrior + m.ceil(guards*sec_lvl*0.01)               
            break
        elif confirm == 'n':
            print('Look again at the cities')
        else:
            print()

    #Print out city list    
    return()
def Send_troops():
    global Journal
    global calendar
    print('********* Send troops out on a mission ************')
    subaction = 1000
    selection = 1000
    support_time = 0
    rebel_time = 0
    scout_time = 0
    travel_time = 0
    actions=[]
    
    while subaction != 0 and len(actions)<3:        
        subaction = int(input('What would you like to do (enter all that apply with spaces)?\n'
               '1. Scout the city\n'
               '2. Bolster sympathy for your cause\n'
               '3. Incite a rebellion\n'
               '0. Done\n'))
        if subaction != 0:
            actions.append(subaction)
    if actions:
        while str(selection) not in Known_cities[1:,0]:
        #while selection !=0:
            View_cities()
            selection = int(input('Which city would you like send your troops to? 0 to exit.'))    
            if selection != 0:
                Lookup_city(selection)
                travel_time =  Map.Travel_route(current_loc,[city_loc[selection][1],city_loc[selection][2]])   
                break
            if selection == 0:
                actions = []
                
        event = 'Your men went to: '
        if 2 in actions:
            support_time = Gain_support(selection)
            event = event + 'preach '
        if 3 in actions:
            rebel_time = Rebellion(selection)
            event = event + 'incite a riot '
        if 1 in actions:
            scout_time = Scout(selection)
            event = event +'scout.'
        
        out_time = max(support_time,rebel_time,scout_time)
        
        for i in range(travel_time):
            drop_security()
            raid()
            gain_xp(soldiers_available*idle_exp,'s')
            gain_xp(druids_available*idle_exp,'d')
            temp = [calendar,'Troops are traveling to '+ city[1]]
            Journal = np.vstack((Journal,temp))
        calendar += travel_time
        
        for i in range(out_time):
            drop_security()
            raid()
            gain_xp(soldiers_available*idle_exp,'s')
            gain_xp(druids_available*idle_exp,'d')
            temp = [calendar,event]
            Journal = np.vstack((Journal,temp))
        calendar += out_time    
        
        for i in range(travel_time):
            drop_security()
            raid()
            gain_xp(soldiers_available*idle_exp,'s')
            gain_xp(druids_available*idle_exp,'d')
            temp = [calendar,'Troops are traveling back to camp ']
            Journal = np.vstack((Journal,temp))
        calendar += travel_time
        
    print()
    return()
    
def Scout(selection):
    global Known_cities
    print('****************Scouting*******************')
    scouts = 1000
    confirm = 'z'
    if city.size:
        while confirm != 'y':
            while scouts > soldiers_available:
                scouts = int(input('How many scouts will you send? (0 to exit) '))
                if scouts > soldiers_available:
                    print('You only have ', soldiers_available, 'available. Try again.')
                if scouts == 0:
                    break
                size = int(city[4])
                scout_time= m.ceil(size/(scouts*100000))
                travel_time =  Map.Travel_route(current_loc,[city_loc[selection][1],city_loc[selection][2]])               
                total_time = int(scout_time +2*travel_time)
                randmin= max(1-(0.5/scouts)-((scout_time+travel_time)/100),0)
                randmax= min(1+(0.5/scouts)+((scout_time+travel_time)/100),2)
                accuracy =int((1-randmin)*100)
                print('Scouting will take',int(total_time),'days with +/- ',accuracy,'% accuracy.')
                while confirm !='y' and confirm != 'n':
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
                        print()
                        for i in range(1,len(Known_cities)):
                            if int(gained_intel[0])==int(Known_cities[i][0]):
                                Known_cities[i] = gained_intel
                        
                        for i in range(1,3):   
                            if Cities[selection+i][0] not in Known_cities[:,0]:
                                print('You have learned of a new city!',Cities[selection+i][1],'\n')
                                start = current_loc
                                end = [city_loc[selection+i][1],city_loc[selection+i][2]]
                                distance = Map.Travel_route(start, end)
                                new_city = [Cities[selection+i][0],Cities[selection+i][1],
                                             Cities[selection+i][2],'',Cities[selection+i][4],
                                             '','','','','','',distance]
                                Known_cities = np.vstack((Known_cities,new_city))
                
                        View_cities()
                    elif confirm == 'n':
                        print()
                        break
                    else:
                        print()
    print()
    return(scout_time)
    
def Gain_support(selection):
    print('****************Gain some supporters*******************')
    druids = 1000
    soldiers = 1000
    time = 0
    confirm = 'x'
    if city.size:
        while confirm != 'y':
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
            while confirm !='y' and confirm != 'n':        
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
                            #print('Day ',(days+1),':Your troops got attacked', result[2],' survived')
                            g_kill = attackers - result[1]
                            s_kill = (druids + soldiers - result[2])
                            Guards -= g_kill
                            soldiers -= s_kill
                            Guards_killed += g_kill
                            soldiers_killed += s_kill
                            update_army(result[4])
        
                        else:
                            #print('Day ',(days+1),': Preaching in the city')
                            convert_chk = 0
                            for i in range(druids):                  
                                convert_chk = r.uniform(0,3)/100
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
                    
                    print('You have gained ', total_added,' sympathizers in ', city[1])
                    print()
                elif confirm == 'n':
                    print('Look again at the cities')
                    break
                else:
                    print()     
                      
    return(days)

def Rebellion(selection):
    print('****************Incite a Riot*******************')
    soldiers = 1000
    time = 0
    days = 0
    confirm = 'z'
    if city.size:
        while confirm != 'y':
            while soldiers > soldiers_available:
                soldiers = int(input('How many soldiers will you send to incite a riot? '))
                if soldiers > soldiers_available:
                    print('You only have ', soldiers_available, 'available. Try again.')
            while time <=0:
                time = int(input('How long should they stay in the city? '))
            print(soldiers, ' soldiers are off to cause trouble for ', time, 'days.')
            confirm = str.lower(input('Are you sure? (y/n) '))
            if confirm == 'y':
                print('\n Your mission is off!')
                area = int(city[4])/43560 #land area in acres
                Conscripts = int(city[6])
                Symp = int(city[8])      
                for i in range(time):
                    convinced = 0
                    days+=1
                    if convinced >= Symp*0.25:
                        break
                    Guards = int(city[5])
                    Encounter = ((soldiers)/area)*(Guards/area)
    
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
                                                   'Dmg rng','Crit','Exp','Level'])
                        unit_stat = Lookup_unit('Sold1','Enemy',soldiers)
                        Encounter_stat = np.vstack((Encounter_stat,unit_stat))
                        np.savetxt('Enemy.csv', Encounter_stat,fmt='%.20s', delimiter=",")                       
                        
                        #Uses battlecode to determine outcome
                        result = b.battle('Ally.csv','Enemy.csv',1)
                        
                        #Removes guards killed by encounter
                        unique, counts = np.unique(result[3], return_counts = True)            
                        city_killed = np.array([(key,val) for (key,val) in dict(zip(unique,counts)).items()],dtype=str)
                        
                        for j in range(len(city_killed)):
                            if city_killed[i][0] == 'Guards':
                                city[5] = int(city[5])-int(city_killed[j][1])
                        
                        soldiers-=len(result[4])
                        update_army(result[4])
    
                    else:
                        for j in range(int(city[8])):
                            if r.randint(1,20)+soldiers>r.randint(1,20):
                                convinced +=1
                        if convinced >= Symp*0.25:
                            print('Your men have sucessfully incited a riot!')
                            #Set up revolt
                            Encounter_stat = np.array(['Number',"Type",
                                                       'HP','AC','Hit Bonus','Dmg Bonus',
                                                       'Dmg rng','Crit','Exp','Level'])
                            unit_stat = Lookup_unit('Guards','City',Guards)
                            Encounter_stat = np.vstack((Encounter_stat,unit_stat)) 
                            unit_stat = Lookup_unit('Conscripts','City',Conscripts)
                            Encounter_stat = np.vstack((Encounter_stat,unit_stat)) 
                            np.savetxt('Ally.csv', Encounter_stat,fmt='%.20s', delimiter=",")
                            
                            #Sets up sympathizers stat blocks
                            Encounter_stat = np.array(['Number',"Type",
                                           'HP','AC','Hit Bonus','Dmg Bonus',
                                           'Dmg rng','Crit','Exp','Level'])
                            unit_stat = Lookup_unit('Symp','Enemy',Symp)
                            Encounter_stat = np.vstack((Encounter_stat,unit_stat))
                            np.savetxt('Enemy.csv', Encounter_stat,fmt='%.20s', delimiter=",")                       
                            
                            #Uses battlecode to determine outcome
                            result = b.battle('Ally.csv','Enemy.csv',1) #Alter battlecode for to the death
                            
                            #Removes guards killed by encounter
                            unique, counts = np.unique(result[3], return_counts = True)            
                            city_killed = np.array([(key,val) for (key,val) in dict(zip(unique,counts)).items()],dtype=str)
                            
                            for j in range(len(city_killed)):
                                if city_killed[j][0] == 'Guards':
                                    city[5] = int(city[5])-int(city_killed[j][1])
                                if city_killed[j][0] == 'Conscripts':
                                    city[6] = int(city[6])-int(city_killed[j][1])
                            
                            unique, counts = np.unique(result[4], return_counts = True)            
                            symp_killed = np.array([(key,val) for (key,val) in dict(zip(unique,counts)).items()],dtype=str)
                            for j in range(len(symp_killed)):
                                if symp_killed[j][0] == 'Symp':
                                    city[8] = int(city[8])-int(symp_killed[j][1])
                            break
                   
                    if soldiers<=0:
                        print('All your soldiers were killed.')
                        break                
                    raid()
    
            elif confirm =='n':
                print('Look again at the cities')
       
            else:
                print()
                
    return(days)

def raid():
    global roster
    
    encounter = len(roster)/1000
    if r.uniform(0,1)<encounter:
        #1-10 random units attacking
        attackers = r.randint(1,10)
        Encounter_stat = np.array(['Number',"Type",
                               'HP','AC','Hit Bonus','Dmg Bonus',
                               'Dmg rng','Crit','Exp','Pos'])
        for i in range(attackers):
            unit_stat = Lookup_unit(city_units[r.randint(1,3)][0],'City',1)
            Encounter_stat = np.vstack((Encounter_stat,unit_stat))
        np.savetxt('Ally.csv', Encounter_stat,fmt='%.20s', delimiter=",")
    
        #1-10 lvl 1 soldiers 
        defenders = r.randint(1,10)   
        Encounter_stat = np.array(['Number',"Type",
                                   'HP','AC','Hit Bonus','Dmg Bonus',
                                   'Dmg rng','Crit','Exp','Pos'])
        for i in range(defenders):
            unit = r.randint(1,len(roster)-1)
            unit_stat = Lookup_unit(roster[unit][0],'Enemy',1)
            Encounter_stat = np.vstack((Encounter_stat,unit_stat))
        
        np.savetxt('Enemy.csv', Encounter_stat,fmt='%.20s', delimiter=",")                       
        
        #Uses battlecode to determine outcome
        result = b.battle('Ally.csv','Enemy.csv',1)
        update_army(result[4])
        if result[0] ==1:
            print("A band of 'heroes' attacked you camp and got away")
            print("The group killed ", len(result[4])," of your men.")
        elif result[0]==0:
            print("Your men fought of a band of heroes", len(result[4]),' died in the process.')

    return()  
def conversion(number,save):
    convert = 0
    for j in range(number):
        if (r.randint(1,20)+intim) > (r.randint(1,20)+save):
            convert+=1
    return(convert)
    
def training():
    global Journal
    global calendar
    
    print('****************Train the troops*******************')
    days = 10000
    while days != 0:
        View_army()
        days = int(input('How many days do you want to train? 0 to exit.'))    
        if days == 0:
            break    
        temp = [calendar,'Your army is training for '+str(days)+' days.']
        Journal = np.vstack((Journal,temp))
        calendar += days
        drop_security()
        for i in range(days):
            gain_xp(soldiers_available*train_exp,'s')
            gain_xp(druids_available*train_exp,'d')
            gain_xp(100,'c')
            raid()

        update_army([])
        break
    return()
    
def drop_security():
    global citiyID
    global attack_date

    if calendar >= (attack_date + 30):
        for i in range(1,len(Cities)): 
            sec_lvl = int(Cities[i][3])
            if sec_lvl > 1:
                sec_lvl -=1
                Cities[i][3]=sec_lvl #update security lvl
                guards = int(Cities[i][5])
                conscript = int(Cities[i][6])
                warrior = int(Cities[i][9])
                commoners = int(Cities[i][10])
                #updates disrtibution to account for growing concern
                Cities[i][10]= commoners + m.ceil(conscript*sec_lvl*0.03)
                Cities[i][6]= conscript - m.ceil(conscript*sec_lvl*0.03) + m.ceil(guards*sec_lvl*0.02)
                Cities[i][5]= guards - m.ceil(guards*sec_lvl*0.02) + m.ceil(warrior*sec_lvl*0.01)
                Cities[i][9]= warrior - m.ceil(warrior*sec_lvl*0.01)
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
    if soldiers_available == 0:
        print('You have no troops remaining. You have failed on your mission')
        return(0)
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
    global Character
    global intim
    if unit == 's':
        if soldiers_available > 0:     
            unit_exp = int(exp/soldiers_available)
            for i in range(1,len(roster)):
                if roster[i][0] == 'Sold1' or roster[i][0] == 'Sold2' or roster[i][0] == 'Sold3' or roster[i][0] == 'Sold4':
                    roster[i][1]=int(roster[i][1])+unit_exp #add experience to each unit
                    if int(roster[i][1])>=int(roster[i][2]) and int(roster[i][3])<4: #level up
                        lvl = int(roster[i][3])+1                    
                        roster[i][3] = lvl
                        roster[i][2] = exp_list[lvl+1]
                        roster[i][0] = "Sold"+str(lvl)
    elif unit == 'd':
        if druids_available > 0:
            unit_exp = int(exp/druids_available)
            for i in range(1,len(roster)):
                if roster[i][0] == 'Druid1' or roster[i][0] == 'Druid2' or roster[i][0] == 'Druid3' or roster[i][0] == 'Druid4':
                    roster[i][1]=int(roster[i][1])+unit_exp #add experience to each unit
                    if int(roster[i][1])>=int(roster[i][2])and int(roster[i][3])<4: #level up
                        lvl = int(roster[i][3])+1                    
                        roster[i][3] = lvl
                        roster[i][2] = exp_list[lvl+1]
                        roster[i][0] = "Druid"+str(lvl)
    elif unit == 'c':
        unit_exp = int(exp)
        Character[1][1]=int(Character[1][1])+unit_exp #add experience to each unit
        if int(Character[1][1])>=int(Character[1][2]): #level up
            lvl = int(Character[1][3])+1                    
            Character[1][3] = lvl
            Character[1][2] = exp_list[lvl+1]
            Character[1][4] = int(Character[1][4])+3
        intim = int(Character[1][4])
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
            print()
        if selection == int(Cities[i][0]):
            city = Cities[i]  
    return()
    
def View_army():
    print("Here's the troop breakdown\n")
    print(army,'\n')
    return()

def View_cities():
    global Known_cities
    update_distance()
    print("Here's what you know about the cities\n")
    print(Known_cities,'\n') 
    return()

def update_distance():
    global Known_cities
    global current_loc
    global city_loc
    global cityID
    
    for i in range(1,len(Known_cities)):
        start = current_loc 
        end = [city_loc[i][1],city_loc[i][2]]
        distance = Map.Travel_route(start, end)
        Known_cities[i][11]= distance
        if distance == 0:
            Known_cities[i][11]= 'X'
    
    cityID = np.argwhere(Known_cities == 'X')[0][0]

    return()
def gen_cities():
    
    return()
    
def Save_game():
    global gamestate
    global Character

    gamestate = str.lower(input('Save game as:'))
    if not os.path.isdir(gamestate):    
        os.makedirs(gamestate)
    np.savetxt(os.path.join(gamestate,'City list.csv'), Cities, fmt='%.20s', delimiter = ',')
    np.savetxt(os.path.join(gamestate,'Full Roster.csv'), roster, fmt='%.20s', delimiter = ',')
    np.savetxt(os.path.join(gamestate,'Known Cities.csv'),Known_cities,  fmt='%.20s',  delimiter = ',')
    np.savetxt(os.path.join(gamestate,'Journal.csv'),Journal,fmt='%.50s',delimiter = ',')
    np.savetxt(os.path.join(gamestate,'Character.csv'),Character,fmt='%.20s',delimiter=',')
    return()
    
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
    global Journal
    global calendar
    global cityID
    global attack_date
    global Character
    
    game = 0
    city_units = np.genfromtxt('City unit stats.csv', dtype = str, delimiter = ',')
    Army_units = np.genfromtxt('Army unit stats.csv', dtype = str, delimiter = ',')
    city_loc = np.genfromtxt('City locations.csv',dtype = int, delimiter = ",")
    while game ==0:    
        gamestate = str.lower(input('Load game as (0 for new game): '))
        print()
        if gamestate == '0':
            Cities = np.genfromtxt(os.path.join('newgame','City list.csv'), dtype = str, delimiter = ',')
            roster = np.genfromtxt(os.path.join('newgame','Full roster.csv'),dtype = str, delimiter = ",")
            update_army([])
            Known_cities = np.genfromtxt(os.path.join('newgame','Known Cities.csv'), dtype = str, delimiter = ',')  
            Journal = np.array([['Day','Event'],[1,'You wander upon a new town']])
            Character = np.genfromtxt(os.path.join('newgame','Character.csv'),dtype = str, delimiter = ",")
            name =str(input("What is your crusader's name?"))
            Character[1][0] = str.lower(name)
            attack_date = 0
            Save_game()
            game = 1
        else:
            try:            
                Cities = np.genfromtxt(os.path.join(gamestate,'City list.csv'), dtype = str, delimiter = ',')
                roster = np.genfromtxt(os.path.join(gamestate,'Full roster.csv'),dtype = str, delimiter = ",")
                Journal = np.genfromtxt(os.path.join(gamestate,'Journal.csv'),dtype = str, delimiter = ",")
                update_army([])
                Known_cities = np.genfromtxt(os.path.join(gamestate,'Known Cities.csv'), dtype = str, delimiter = ',')  
                game = 1
                try:
                    attack_date = int(Journal[np.argwhere(Journal =='Attacking the city')[len(np.argwhere(Journal =='Attacking the city'))-1][0]][0])
                except:
                    attack_date = 0
                Character = np.genfromtxt(os.path.join(gamestate,'Character.csv'),dtype = str, delimiter = ",")
            except:
                print('Cannot file file. Try a new name')
                game = 0
    cityID = np.argwhere(Known_cities == 'X')[0][0]
    current_loc = [city_loc[cityID][1],city_loc[cityID][2]]
    calendar = int(Journal[len(Journal)-1][0])
        
    print(Journal[len(Journal)-1][1],'\n')

    #print(Journal)
    return()       


#Reference materials
global Journal
global calendar
global Character

#game parameters
idle_exp = 50
train_exp = 100
exp_list = [0,0,2000,5000,9000,15000,23000,35000,51000,75000,105000]    
comm_druid = 5

load_game()

action = 0
while action != 7:
    print('It has been ', calendar,' days since you began your crusade.\n')
    action = int(input('What would you like to do?\n'
                   '1. Send out troops\n'
                   '2. Attack a city\n'
                   '3. Wait and train\n'
                   '4. View army\n'
                   '5. View cities\n'
                   '6. Save and continue\n'
                   '7. End session and save\n'))

    if action ==1:
        Send_troops()            
    elif action ==2:
        Attack_city()
    elif action ==3:
        training()
    elif action ==4:
        View_army()
    elif action ==5:
        View_cities()
    elif action == 6:
        Save_game()
    elif action ==7:
        Save_game()
        print('Until next time')
        break

    else:
        print('You need to pick an action')

#######Improvements to make
#Randomize cities on new game
#Druid vs Character conversion
#GUI
#Roll stats for character
#xheck for the right input
#fix y/n confirmation