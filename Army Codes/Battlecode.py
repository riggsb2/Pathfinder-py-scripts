import random
import copy
import numpy as np

def attackroll(HitBon,DmgBon,DmgRng,CritRng,AC):
    roll = random.randint(1,20)
    attack = roll + HitBon
    #print('HitBon',HitBon)    
    #print('DmgBon',DmgBon)    
    #print('DmgRng',DmgRng)    
    #print('Critrng',CritRng)  
    #print('AC', AC)
    #print('Roll',roll)
    #print('Attack',attack)

    if attack >= AC:
        if roll >= CritRng:
            #print('Crit!')            
            Damage = random.randint(1,DmgRng)+random.randint(1,DmgRng)+DmgBon
        else:
            #print('Hit')
            Damage = random.randint(1,DmgRng)+DmgBon
    else:
        #print('Miss')

        Damage = 0            
    return(Damage)

def battle(armyfile,enemyfile,simulations):    
    Ewin = 0
    Awin = 0
    Dead = 0
    
    #Read and print the CSV files
    
    Ally_stats = []
    Ally_army = []
    ##Inputs csv into array
    Ally_stats = np.genfromtxt(armyfile, dtype = str, delimiter=',')
    ##Prints and assigns stats into Army Array
    for i in range(len(Ally_stats)):
        Ally = []
        for j in range(len(Ally_stats[i])):
            if i!=0 and j!=1:
                Ally_stats[i][j]=int(Ally_stats[i][j])
            if j == 0: 
                #print( '{:<10}'.format(Ally_stats[i][j]), end=' ')
                units = Ally_stats[i][j] #sets number of units
            else:
                #print('{:<10}'.format(Ally_stats[i][j]),end = ' ')
                Ally.append(Ally_stats[i][j]) #assembles Alley stat block
        if i != 0:
            for k in range(int(units)):
                Ally_army.append(copy.deepcopy(Ally))
        #print() 
    #print()
    
    #Reads Enemy army from CSV file and prints on screen
    Enemy_stats = []
    Enemy_army = []
    
    ##Inputs csv into array
    Enemy_stats = np.genfromtxt(enemyfile, dtype = str, delimiter=',')
    
    ##Prints and assigns stats into Army Array
    for i in range(len(Enemy_stats)):
        Enemy = []
        for j in range(len(Enemy_stats[i])):
            if i!=0 and j!=1:
                Enemy_stats[i][j]=int(Enemy_stats[i][j])
            if j == 0: 
                #print( '{:<10}'.format(Enemy_stats[i][j]), end=' ')
                units = Enemy_stats[i][j] #sets number of units
            else:
                #print('{:<10}'.format(Enemy_stats[i][j]),end = ' ')
                Enemy.append(Enemy_stats[i][j]) #assembles Alley stat block
        if i != 0:
            for k in range(int(units)):
                Enemy_army.append(copy.deepcopy(Enemy))
        #print()
    #print()
    
    Ally_survlst =[]
    Enemy_survlst =[]
    #Runs several simulations
    for run in range(simulations):
        #print(run)        
        Ally_army = []
        ##assigns stats into Army list of lists
        for i in range(len(Ally_stats)):
            Ally = []
            for j in range(len(Ally_stats[i])):
                if i!=0 and j!=1:
                    Ally_stats[i][j]=int(Ally_stats[i][j])
                if j == 0: 
                    units = Ally_stats[i][j] #sets number of units
                else:
                    Ally.append(Ally_stats[i][j]) #assembles Alley stat block
            Ally.append('A')
            if i != 0:
                for k in range(int(units)):
                    Ally_army.append(copy.deepcopy(Ally))
        
        Enemy_army = []      
        #assigns stats into Army Array
        for i in range(len(Enemy_stats)):
            Enemy = []
            for j in range(len(Enemy_stats[i])):
                if i!=0 and j!=1:
                    Enemy_stats[i][j]=int(Enemy_stats[i][j])
                if j == 0: 
                    units = Enemy_stats[i][j] #sets number of units
                else:
                    Enemy.append(Enemy_stats[i][j]) #assembles Alley stat block
            Enemy.append('E')
            if i != 0:
                for k in range(int(units)):
                    Enemy_army.append(copy.deepcopy(Enemy))
        
        #Randomizes Unit Positions
        for i in range(1,len(Ally_army)):
            Pos1 = random.randint(0,len(Ally_army)-1)
            Pos2 = random.randint(0,len(Ally_army)-1)
            Ally_army[Pos1], Ally_army[Pos2] = Ally_army[Pos2], Ally_army[Pos1]
        
        for i in range(1,len(Enemy_army)):
            Pos1 = random.randint(0,len(Enemy_army)-1)
            Pos2 = random.randint(0,len(Enemy_army)-1)
            Enemy_army[Pos1], Enemy_army[Pos2] = Enemy_army[Pos2], Enemy_army[Pos1]
            
        #Issue with interpretation of values in 3D array        
        empty = ['','','','','','','','','','']
        Battlefield = np.array([[Enemy_army[0],Ally_army[0],empty,empty]])
        for i in range(1,min(len(Ally_army),len(Enemy_army))):
            temp = [[Enemy_army[i],Ally_army[i],empty,empty]]
            Battlefield = np.vstack((Battlefield,temp))
        for i in range(min(len(Ally_army),len(Enemy_army)),max(len(Ally_army),len(Enemy_army))):
            if len(Enemy_army) > i:
                temp = [[Enemy_army[i],empty,empty,empty]]
            if len(Ally_army) > i:
                temp = [[Ally_army[i],empty,empty,empty]]
            Battlefield = np.vstack((Battlefield,temp))           
                    
        rnd=1  
        #Run the battle. As long as one army doesn't overwhelm the other (5x size), continue fighting
        Ally_deadlist = []
        Enemy_deadlist = []
        while len(Ally_army)<5*len(Enemy_army) and len(Enemy_army)<5*len(Ally_army):
        #while len(Ally_army)>0 and len(Enemy_army)>0: #TO THE DEATH
            rnd_length=(len(Battlefield))
            #loops through entire battlefiled

            for rnd_count in range(rnd_length):

                #Check who is in what slot of a position
                Ally_pos = []
                Enemy_pos = []
                for Slot in range(len(Battlefield[rnd_count])):
                    if Battlefield[rnd_count][Slot][9] =='A':
                        Ally_pos.append(Slot)
                    elif Battlefield[rnd_count][Slot][9] =='E':
                        Enemy_pos.append(Slot)


                Ally_prevpos = []
                Enemy_prevpos = []                    
                for Slot in range(len(Battlefield[rnd_count-1])):
                    if Battlefield[rnd_count-1][Slot][9] =='A':
                        Ally_prevpos.append(Slot)
                    elif Battlefield[rnd_count-1][Slot][9] =='E':
                        Enemy_prevpos.append(Slot)
                
                Full = [0,1,2,3]              
                openings = [x for x in Full if x not in (Ally_prevpos + Enemy_prevpos)]
                
                for AT in range(len(Ally_pos)):
                    if Enemy_pos:   #Checks to see if there are enemies to fight                 
                        dmg = attackroll(int(Battlefield[rnd_count][Ally_pos[AT]][3]),#Hit Bonus
                                      int(Battlefield[rnd_count][Ally_pos[AT]][4]),#Dmg Bonus
                                      int(Battlefield[rnd_count][Ally_pos[AT]][5]),#Dmg Range
                                      int(Battlefield[rnd_count][Ally_pos[AT]][6]),#Crit Range
                                      int(Battlefield[rnd_count][Enemy_pos[0]][2]))#Enemy AC
                        HP = int(Battlefield[rnd_count][Enemy_pos[0]][1])
                        HP -= dmg
                        Battlefield[rnd_count][Enemy_pos[0]][1] = HP
                    elif not Enemy_pos:
                        if rnd_count != 0:
                            if openings and len(Ally_prevpos)<3:
                                Battlefield[rnd_count-1][openings[0]]= Battlefield[rnd_count][Ally_pos[AT]]
                                Ally_prevpos.append(openings[0])
                                Battlefield[rnd_count][Ally_pos[AT]]=['','','','','','','','','','']
  
    
                    openings = [x for x in Full if x not in (Ally_prevpos + Enemy_prevpos)]
                
                                  
                for ET in range(len(Enemy_pos)):
                    if Ally_pos:  #Checks to see if there are allies to fight                  
                        dmg = attackroll(int(Battlefield[rnd_count][Enemy_pos[ET]][3]),#Hit Bonus
                                      int(Battlefield[rnd_count][Enemy_pos[ET]][4]),#Dmg Bonus
                                      int(Battlefield[rnd_count][Enemy_pos[ET]][5]),#Dmg Range
                                      int(Battlefield[rnd_count][Enemy_pos[ET]][6]),#Crit Range
                                      int(Battlefield[rnd_count][Ally_pos[0]][2]))#Enemy AC
                        HP = int(Battlefield[rnd_count][Ally_pos[0]][1])
                        HP -= dmg
                        Battlefield[rnd_count][Ally_pos[0]][1] = HP
                    elif not Ally_pos:
                        if rnd_count !=0:
                            if openings and len(Enemy_prevpos)<3:
                                Battlefield[rnd_count-1][openings[0]]= Battlefield[rnd_count][Enemy_pos[ET]]
                                Enemy_prevpos.append(openings[0])
                                Battlefield[rnd_count][Enemy_pos[ET]]=['','','','','','','','','','']


                    openings = [x for x in Full if x not in (Ally_prevpos + Enemy_prevpos)]
              
            #Check for dead bodies
            for rnd_count in range(rnd_length):
                for Slot in range(len(Battlefield[rnd_count])):
                    if Battlefield[rnd_count][Slot][1] <='0':
                        if Battlefield[rnd_count][Slot][9] =='A':
                            Ally_deadlist.append(Battlefield[rnd_count][Slot][0])
                            try: 
                                del Ally_army[-1]
                            except:
                                break
                        elif Battlefield[rnd_count][Slot][9] =='E':
                            Enemy_deadlist.append(Battlefield[rnd_count][Slot][0])
                            try: 
                                del Enemy_army[-1]
                            except:
                                break
                        Battlefield[rnd_count][Slot]=['','','','','','','','','','']
                                    
            #remove dead bodies from the field        
            Ally_army = [x for x in Ally_army if x]
            Enemy_army = [x for x in Enemy_army if x]
            
            #clear empty blocks of array
            for i in reversed(range(len(Battlefield))):
                if np.count_nonzero(Battlefield[i]) == 0:
                    Battlefield = np.delete(Battlefield,(i),axis = 0)
            rnd+=1
        
        if len(Ally_army)<5*len(Enemy_army):
            Ewin +=1
        elif len(Enemy_army)<5*len(Ally_army):
            Awin +=1
        else:
            Dead+=1
        Ally_surv = len(Ally_army)
        Enemy_surv = len(Enemy_army)
        Ally_survlst.append(Ally_surv)
        Enemy_survlst.append(Enemy_surv)
    
    #print("Battles Complete")
    Ally_avg = int(sum(Ally_survlst)/len(Ally_survlst))
    Enemy_avg= int(sum(Enemy_survlst)/len(Enemy_survlst))
    

        
    WinRatio = round((Awin/simulations)*100)    
    return(WinRatio, Ally_avg, Enemy_avg, Ally_deadlist, Enemy_deadlist, rnd/10)


#print('Allies win: ', battle('Ally.csv','Enemy.csv',1),'%')  

