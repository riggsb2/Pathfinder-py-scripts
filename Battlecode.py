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
                print( '{:<10}'.format(Ally_stats[i][j]), end=' ')
                units = Ally_stats[i][j] #sets number of units
            else:
                print('{:<10}'.format(Ally_stats[i][j]),end = ' ')
                Ally.append(Ally_stats[i][j]) #assembles Alley stat block
        if i != 0:
            for k in range(int(units)):
                Ally_army.append(copy.deepcopy(Ally))
        print() 
    print()
    
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
                print( '{:<10}'.format(Enemy_stats[i][j]), end=' ')
                units = Enemy_stats[i][j] #sets number of units
            else:
                print('{:<10}'.format(Enemy_stats[i][j]),end = ' ')
                Enemy.append(Enemy_stats[i][j]) #assembles Alley stat block
        if i != 0:
            for k in range(int(units)):
                Enemy_army.append(copy.deepcopy(Enemy))
        print()
    print()
    
    #Runs several simulations
    for run in range(simulations):
        Ally_army = []
        ##assigns stats into Army Array
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
        Battlefield = np.zeros([max(len(Ally_army),len(Enemy_army)),
                                4,
                                len(Ally)],
                                dtype='a2')
        Battlefield[0:len(Ally_army),0] = Ally_army[:]        
        Battlefield[0:len(Enemy_army),1] = Enemy_army[:]

        rnd=1      
        #Run the battle. As long as one army doesn't overwhelm the other (5x size), continue fighting
        #while len(Ally_army)<5*len(Enemy_army) and len(Enemy_army)<5*len(Ally_army):
        while len(Ally_army)>0 and len(Enemy_army)>0: #TO THE DEATH
            #print(len(Ally_army))
            #print(len(Enemy_army))
            rnd_length=(len(Battlefield))
            #loops through entire battlefiled
                        
            #print('Rnd length', len(Battlefield))
            #print(Battlefield)            
            for rnd_count in range(rnd_length):
                #Check who is in what slot of a position
                #print('Turn', rnd_count)                
                Ally_pos = []
                Enemy_pos = []                   
                for Slot in range(len(Battlefield[rnd_count])):
                    if Battlefield[rnd_count][Slot][9] ==b'A':
                        Ally_pos.append(Slot)
                    elif Battlefield[rnd_count][Slot][9] ==b'E':
                        Enemy_pos.append(Slot)
                
                for AT in range(len(Ally_pos)):
                    if Enemy_pos:   #Checks to see if there are enemies to fight                 
                        #print('Ally Attack')                    
                        dmg = attackroll(int(Battlefield[rnd_count][Ally_pos[AT]][3]),#Hit Bonus
                                      int(Battlefield[rnd_count][Ally_pos[AT]][4]),#Dmg Bonus
                                      int(Battlefield[rnd_count][Ally_pos[AT]][5]),#Dmg Range
                                      int(Battlefield[rnd_count][Ally_pos[AT]][6]),#Crit Range
                                      int(Battlefield[rnd_count][Enemy_pos[0]][2]))#Enemy AC
                        #print(dmg)  
                        HP = int(Battlefield[rnd_count][Enemy_pos[0]][1])
                        HP -= dmg
                        Battlefield[rnd_count][Enemy_pos[0]][1] = HP
                        #print(Battlefield[rnd_count][Enemy_pos[0]][1])
                        #print()
                    elif not Enemy_pos:
                        #print('No Enemies left')
                        for Slot in range(len(Battlefield[rnd_count])): #Check slots for ally
                            for opening in range(len(Battlefield[rnd_count-1])): #Finds opening in position above
                                if Battlefield[rnd_count-1][opening][0] == b'': #if there's an opening, fill it
                                    #print('Empty slot')
                                    Battlefield[rnd_count-1][opening] = Battlefield[rnd_count][Slot]
                                    Battlefield[rnd_count][Slot]=['','','','','','','','','','']                
                
                for ET in range(len(Enemy_pos)):
                    if Ally_pos:  #Checks to see if there are allies to fight                  
                        #print('Enemy Attack')                    
                        dmg = attackroll(int(Battlefield[rnd_count][Enemy_pos[ET]][3]),#Hit Bonus
                                      int(Battlefield[rnd_count][Enemy_pos[ET]][4]),#Dmg Bonus
                                      int(Battlefield[rnd_count][Enemy_pos[ET]][5]),#Dmg Range
                                      int(Battlefield[rnd_count][Enemy_pos[ET]][6]),#Crit Range
                                      int(Battlefield[rnd_count][Ally_pos[0]][2]))#Enemy AC
                        #print(dmg)  
                        HP = int(Battlefield[rnd_count][Ally_pos[0]][1])
                        HP -= dmg
                        Battlefield[rnd_count][Ally_pos[0]][1] = HP
                        #print(Battlefield[rnd_count][Ally_pos[0]][1])
                        #print()
                    elif not Ally_pos:
                        #print('No Allies left')
                        for Slot in range(len(Battlefield[rnd_count])): #Check slots for ally
                            for opening in range(len(Battlefield[rnd_count-1])): #Finds opening in position above
                                if Battlefield[rnd_count-1][opening][0] == b'': #if there's an opening, fill it
                                    #print('Empty slot')
                                    Battlefield[rnd_count-1][opening] = Battlefield[rnd_count][Slot]
                                    Battlefield[rnd_count][Slot]=['','','','','','','','','','']
               
                
            #print('Death Check')            
            #Check for dead bodies
            for rnd_count in range(rnd_length):
                for Slot in range(len(Battlefield[rnd_count])):
                    #print('Deathcheck',rnd_count,Slot)                    
                    if Battlefield[rnd_count][Slot][1] <=b'0':
                        if Battlefield[rnd_count][Slot][9] ==b'A':
                            del Ally_army[-1]
                        elif Battlefield[rnd_count][Slot][9] ==b'E':
                            del Enemy_army[-1]                        
                        #print('Dead', rnd_count, Slot, Battlefield[rnd_count][Slot])                        
                        Battlefield[rnd_count][Slot]=['','','','','','','','','','']
                                    
            
            #print('Remove bodies')
            #remove dead bodies from the field        
            Ally_army = [x for x in Ally_army if x]
            Enemy_army = [x for x in Enemy_army if x]
            
            #clear empty blocks of array
            #print('Clean up battfield array')
            for i in reversed(range(len(Battlefield))):
                #print(i)
                #print(np.count_nonzero(Battlefield[i]))
                if np.count_nonzero(Battlefield[i]) == 0:
                    Battlefield = np.delete(Battlefield,(i),axis = 0)
            rnd+=1
        
        #print('Win count')
        if len(Ally_army)<5*len(Enemy_army):
            #print('The Enemy army wins. Allies have ',len(Ally_army),' unit(s) remaining')
            Ewin +=1
        elif len(Enemy_army)<5*len(Ally_army):
            #print('The Ally army wins. Enemy army has ',len(Enemy_army),' unit(s) remaining')
            Awin +=1
        else:
            #print('Everyone is dead.')
            Dead+=1
    #print(Battlefield)
    WinRatio = round((Awin/simulations)*100)    
    return(WinRatio)
    #print('Ally wins: ',Awin)
    #print('Enemy wins: ', Ewin)
    #print('Complete destruction: ',Dead)

print('Allies win: ', battle('Party.csv','Encounter army.csv',1000),'%')  

