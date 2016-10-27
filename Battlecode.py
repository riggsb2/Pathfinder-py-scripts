import random
import copy
import csv


def battlelog(rnd_count):
    if Ally_army[rnd_count][6]>=Enemy_army[rnd_count][2]:
        print(Ally_army[rnd_count][0], ' Hit  Roll', Ally_army[rnd_count][6],Ally_army[rnd_count][7],'dmg. HP: ',Ally_army[rnd_count][1]) 
    else:
        print(Ally_army[rnd_count][0], ' Miss Roll', Ally_army[rnd_count][6],'HP: ',Ally_army[rnd_count][1])

    if Enemy_army[rnd_count][6]>=Ally_army[rnd_count][2]:
        print(Enemy_army[rnd_count][0], ' Hit  Roll', Enemy_army[rnd_count][6],Enemy_army[rnd_count][7],'dmg. HP: ',Enemy_army[rnd_count][1]) 
    else:
        print(Enemy_army[rnd_count][0], 'Miss Roll', Enemy_army[rnd_count][6], 'HP: ',Enemy_army[rnd_count][1]) 
        
    print()
    print('Allied units left ', len(Ally_army))
    print('Enemy units left ', len(Enemy_army))

def battle(armyfile,Enemyfile,simulations):    
    Ewin = 0
    Awin = 0
    Dead = 0
    
    #Read and print the CSV files
    
    Ally_stats = []
    Ally_army = []
    ##Inputs csv into array
    with open(armyfile,'r') as csvfile:
        data = csv.reader(csvfile, delimiter=',')
        for row in data:
            Ally_stats.append(row)
    
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
    with open(Enemyfile,'r') as csvfile:
        data = csv.reader(csvfile, delimiter=',')
        for row in data:
            Enemy_stats.append(row)
    
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
        #Reads ally army from CSV file and prints on screen
        #armyfile ='Alley_army.csv'
        #Ally_stats = []
        Ally_army = []
        #print(Ally_stats)
        ##Inputs csv into array
        #with open(armyfile,'r') as csvfile:
         #   data = csv.reader(csvfile, delimiter=',')
          #  for row in data:
           #     Ally_stats.append(row)
            #print()
        
        ##Prints and assigns stats into Army Array
        for i in range(len(Ally_stats)):
            Ally = []
            for j in range(len(Ally_stats[i])):
                if i!=0 and j!=1:
                    Ally_stats[i][j]=int(Ally_stats[i][j])
                if j == 0: 
                    units = Ally_stats[i][j] #sets number of units
                else:
                    Ally.append(Ally_stats[i][j]) #assembles Alley stat block
            if i != 0:
                for k in range(int(units)):
                    Ally_army.append(copy.deepcopy(Ally))
            #print() 
        
        #Reads Enemy army from CSV file and prints on screen
        #Enemyfile ='Enemy_army.csv'
        #Enemy_stats = []
        Enemy_army = []

        ##Inputs csv into array
        #with open(Enemyfile,'r') as csvfile:
        #    data = csv.reader(csvfile, delimiter=',')
        #    for row in data:
        #        Enemy_stats.append(row)
            #print()
        
        ##Prints and assigns stats into Army Array
        for i in range(len(Enemy_stats)):
            Enemy = []
            for j in range(len(Enemy_stats[i])):
                if i!=0 and j!=1:
                    Enemy_stats[i][j]=int(Enemy_stats[i][j])
                if j == 0: 
                    units = Enemy_stats[i][j] #sets number of units
                else:
                    Enemy.append(Enemy_stats[i][j]) #assembles Alley stat block
            if i != 0:
                for k in range(int(units)):
                    Enemy_army.append(copy.deepcopy(Enemy))
            #print()
        
        #Randomizes Unit Positions
        for i in range(1,len(Ally_army)):
            Pos1 = random.randint(0,len(Ally_army)-1)
            Pos2 = random.randint(0,len(Ally_army)-1)
            Ally_army[Pos1], Ally_army[Pos2] = Ally_army[Pos2], Ally_army[Pos1]
        
        for i in range(1,len(Enemy_army)):
            Pos1 = random.randint(0,len(Enemy_army)-1)
            Pos2 = random.randint(0,len(Enemy_army)-1)
            Enemy_army[Pos1], Enemy_army[Pos2] = Enemy_army[Pos2], Enemy_army[Pos1]
        
        rnd=1
        
        #Run the battle. As long as one army doesn't overwhelm the other (5x size), continue fighting
        #while len(Ally_army)<5*len(Enemy_army) and len(Enemy_army)<5*len(Ally_army):
        while len(Ally_army)>0 and len(Enemy_army)>0: #TO THE DEATH
            #print('********************* Round, ',rnd,' *********************')
            rnd_length=(min(len(Ally_army),len(Enemy_army)))
            #print('Round is ', rnd_length, ' turns.')
        
            #loops through entire army for 1v1 combat
            for rnd_count in range(rnd_length):
        
                #print(rnd_count+1)
                #print()
                #Assigned to hit and damage for each active unit
                Ally_army[rnd_count][6] = random.randint(1,20)+int(Ally_army[rnd_count][3])
                Ally_army[rnd_count][7] = random.randint(1,int(Ally_army[rnd_count][5]))+int(Ally_army[rnd_count][4])
                Enemy_army[rnd_count][6] = random.randint(1,20)+ int(Enemy_army[rnd_count][3])
                Enemy_army[rnd_count][7] = random.randint(1,int(Enemy_army[rnd_count][5]))+ int(Enemy_army[rnd_count][4])
        
                #Checks to see if they hit their opponent
                if Ally_army[rnd_count][6]>=int(Enemy_army[rnd_count][2]):
                    Enemy_army[rnd_count][1]-=Ally_army[rnd_count][7]
        
                if Enemy_army[rnd_count][6]>=Ally_army[rnd_count][2]:
                    Ally_army[rnd_count][1]-=Enemy_army[rnd_count][7]
            
            #Check for dead bodies
            for rnd_count in range(rnd_length):
                if Ally_army[rnd_count][1] <=0:
                    Ally_army[rnd_count] = []
                if Enemy_army[rnd_count][1] <=0:
                    Enemy_army[rnd_count] = []
        
            #remove dead bodies from the field        
            Ally_army = [x for x in Ally_army if x]
            Enemy_army = [x for x in Enemy_army if x]
        
            rnd+=1
            
        if len(Ally_army)<5*len(Enemy_army):
            #print('The Enemy army wins. Allies have ',len(Ally_army),' unit(s) remaining')
            Ewin +=1
        elif len(Enemy_army)<5*len(Ally_army):
            #print('The Ally army wins. Enemy army has ',len(Enemy_army),' unit(s) remaining')
            Awin +=1
        else:
            #print('Everyone is dead.')
            Dead+=1
    
    WinRatio = round((Awin/simulations)*100)
    return(WinRatio)
    #print('Ally wins: ',Awin)
    #print('Enemy wins: ', Ewin)
    #print('Complete destruction: ',Dead)

#print('Allies win: ', battle('Party.csv','Blaze Boa.csv',1000),'%')       
