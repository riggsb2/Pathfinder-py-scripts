# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
import random as r
import math as m
import Battlecode as bc

filename = 'Random Encounter Table.csv'
encounter_table = np.genfromtxt(filename, dtype = str, delimiter=',')

#Create probability stack
roll_table = np.empty([1,len(encounter_table[0])])
for i in range(1,len(encounter_table)):
    for j in range(int(encounter_table[i,0])):
        roll_table = np.vstack((roll_table,encounter_table[i]))
        
#Imports creature list
filename = 'Monster list.csv'

Monster_table = np.genfromtxt(filename, dtype = str, delimiter = ',')

#reads travel and party information
filename = 'Travel Itinerary.csv'
Itinerary = np.genfromtxt(filename, delimiter=',')

total_exp = 0

travel_record = np.array(['Day','CR Zone', 'APL', 'Monster', 'Monster level',
                         '# creatures', 'Win%', 'Experience'])
for i in range(1,len(Itinerary)):   #loops through the days of travel
    APL = Itinerary[i,2]    
    CR = Itinerary[i,1]
    Exp = int(290.95*m.e**(0.3466*(CR)))
    monster = roll_table[r.randint(1,100),CR]
    #Search for monster in monster table    
    for j in range(len(Monster_table)):    
        win = 0        
        if Monster_table[j][0] == monster:
            monster_lvl = int(Monster_table[j,1])
            monster_exp = int(290.95*m.e**(0.3466*(monster_lvl)))
            monster_cnt = round(Exp/monster_exp)
            HP = int(Monster_table[j][2])
            AC = int(Monster_table[j][3])
            HitBonus = int(Monster_table[j][4])
            DmgBonus = int(Monster_table[j][5])
            DmgRng = int(Monster_table[j][6])
                    
            Exp = int(monster_cnt*monster_exp)
            #print(monster)
            
            #print(Exp) 
            if monster == 'Nothing':
                Exp = 0
            Encounter_stat = np.array(['Number',"Type",
                                       'HP','AC','Hit Bonus','Dmg Bonus',
                                       'Dmg rng','Roll','Dmg','Pos'])
            monster_stat = np.array([monster_cnt,monster,
                            HP,AC,HitBonus,DmgBonus,DmgRng,
                            0,0,0])
            total_exp += Exp
            #print(total_exp)

            Encounter_stat = np.vstack((Encounter_stat,monster_stat))
            np.savetxt('Encounter army.csv', Encounter_stat,fmt='%.20s', delimiter=",")
    if monster_lvl*2 <= APL:
        win = 100
    else:
        win = bc.battle('Party.csv','Encounter army.csv',100)
        print('###########################################################')

    temp = [i,CR,APL,monster,monster_lvl,monster_cnt,win,Exp]
    travel_record = np.vstack((travel_record,temp))

temp = ['','','','','','','Total Exp',total_exp]
travel_record = np.vstack((travel_record,temp))

np.savetxt('Travel Record.csv', travel_record,fmt='%.20s', delimiter=",")
print(travel_record)
