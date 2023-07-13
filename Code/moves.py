# -*- coding: utf-8 -*-
"""
Created on Wed Mar  8 10:50:27 2023

@author: User
"""
import random
import math


#Generate random values (pivot, clockwise/anticlockwise, front/back) and passes into inPlane mover
def move_manager(original, initEnergy, moveItr, run, t, parents):
    #List of sequence candidates (in case genetic is used. Else, it will be sequence[0])
    energyList = []
    sequence = []
    
    #Moves before comparing energy of configurations
    for i in range (0, parents):
        #Copy original for new candidate
        sequence.append([x.coord for x in original])
        
        for x in range (moveItr):
            #For each sequence in list, generate possible move(s)
            result = "Invalid"
            while isinstance(result, str): #Until a valid move is generated, re-attempt generation
                clock = 1 if random.random() < 0.5 else -1 #1 = clockwise around pivot, -1 = anticlockwise around pivot
                forb = -1 if random.random() < 0.5 else -1 #1 = move elements after, -1 = move elements before
                pivot = random.randint(0,len(sequence[0])-1) #Pivot
                result = inplane(sequence[i].copy(), pivot, clock, forb)
            #If valid, apply new coordinates as candidate
            sequence[i] = result[0]
        energyList.append(energy_calc(original, sequence[i], result[1]))      
                
                
    
    #If genetic algorithm is being used    
    if parents > 1:
        #Sort sequence list based on energy score.
        sequence = [x for _, x in sorted(zip(energyList, sequence))]

        #Iterate through sequence looking for possible combination. Return first valid combination  
        for ind, i in enumerate(sequence[:-1]):
            for j in sequence[ind + 1:]:
                valid = "invalid"
                #Pass first half of sequence i and second of seuqnce j into move_checker
                valid = move_checker(i[:int(len(i)/2)] + j[-int(len(i)/2):])
                if isinstance (valid, str): #If invalid, attempt clockwise join 
                    valid = inplane(i[:int(len(i)/2)] + j[-int(len(i)/2):], int(len(sequence[0])/2), 1, 1)
                if isinstance (valid, str): #If still invalid,attempt anti-clockwise join
                    valid = inplane(i[:int(len(i)/2)] + j[-int(len(i)/2):], int(len(sequence[0])/2), 2, 1)  
                if isinstance(valid, tuple): #If valid, break nested loop
                    sequence[0] = result[0]
                    energyList[0] = (energy_calc(original, result[0], result[1]))
                    break
            else:
                continue
            break
        
        
    
    #If annealing is used
    if isinstance(t, float):
        #Annealing time, bby! Let's see if I do this right...
        diff = energyList[0] - initEnergy
        newT = t / float(run + 1)
        metr = math.exp(-diff / newT) #Metropolis acceptance [approach
        if diff < 0 or random.random() < metr:
            return (energyList[0],sequence[0])
        else:
            return(initEnergy)
        
    #Else, hill climbing is being used (copy over if better energy score)           
    else:
        if energyList[0] < initEnergy:
            return(energyList[0],sequence[0])
        else:
            return(initEnergy)


#----------


#Calculates where nodes move, then calls on apply_move
def inplane(sequence, pivot, direction, forb):
    newCoord = [(sequence[pivot][0], sequence[pivot][1])] #Add pivot to list
    shiftx = 0 #Lattice shift needed on x axis
    shifty = 0 #Lattice shift needed on y axis
    ind = 0 #local sequence index
    end = len(sequence)-1 if forb == 1 else 0 #Value to iterate to
    
    #From start value to last value of sequence
    for i in range(pivot + forb, end + forb, forb):
        #If down, shift to left/right
        if sequence[i][0] > sequence[i-forb][0]:
            x = -1 * direction
            y = 0 * direction
        #If up, shift to right/left
        elif sequence[i][0] < sequence[i-forb][0]:
            x = 1 * direction
            y = 0 * direction
        #If right, shift to down/up
        elif sequence[i][1] > sequence[i-forb][1]:
            x = 0 * direction
            y = 1 * direction
        #If left, shift up/down
        else:
            x = 0 * direction
            y = -1 * direction
        
        
        #Valid if needs shift (thus no overlaps)
        newCoord.append((newCoord[ind][0] + y, newCoord[ind][1] + x))
        ind += 1
        #Shift down
        if newCoord[ind][0] + shiftx < 0:
            shiftx += 1
        #Shift up
        elif newCoord[ind][0] + shiftx > len(sequence) -1:
            shiftx -= 1
        #Shift right
        elif newCoord[ind][1] + shifty < 0:
            shifty += 1
        #Shift left   
        elif newCoord[ind][1] + shifty > len(sequence) -1:
            shifty -= 1
    
    #Check move is valid
    newCoord.pop(0)#Remove pivot
    return (apply_move(sequence, pivot, newCoord, shiftx, shifty, forb))
    



#Applies new values to sequence
def apply_move(sequence, pivot, newCoord, shiftx, shifty, forb):
    #Assign unmoved values (with shift)
    start = 0 if forb == 1 else len(sequence)-1
    for i in range (start, pivot+forb, forb):
        sequence[i] = (sequence[i][0] + shiftx, sequence[i][1] + shifty)
        
    #Apply new values
    for i in range (len(newCoord)):
        itr = (i*forb)+pivot+forb
        #At node, replace coords with previous node coords and add modifier sequence[i] to it.
        sequence[itr] = (newCoord[i][0]+shiftx, newCoord[i][1]+shifty)   

    #If no invalid returned, return new sequence + lattice            
    return move_checker(sequence)




#Check for collissions and create lattice (sepperated so it can be called on by genetic alg)
def move_checker(sequence):
    lattice = [[None for x in range(len(sequence))] for i in range(len(sequence))]
    
    for i in range (len(sequence)):
        if lattice[sequence[i][0]][sequence[i][1]] != None:
            #IF ID at the coord I want to move to is lower, it won't be moved, thus an invalid move
            return ("Invalid")
        else:
            lattice[sequence[i][0]][sequence[i][1]] = i
    return(sequence, lattice)




#Returns energy value for current configuration
def energy_calc(original, sequence, lattice):
    #Check adjacencies of H nodes in new configuration, calculate score
    energy = 0
    for i in range (len(sequence)):
        if original[i].HP == "H":
            #If not on right border, check space to right
            if sequence[i][0] != len(lattice)-1:
                if lattice[sequence[i][0] + 1][sequence[i][1]] not in (i-1, i+1, None) and original[lattice[sequence[i][0] + 1][sequence[i][1]]].HP == "H": #If not sequential AND = H
                    energy -= 1
            #If not on left border, check space to left
            if sequence[i][0] != 0:
                if lattice[sequence[i][0] - 1][sequence[i][1]] not in (i-1, i+1, None) and original[lattice[sequence[i][0] - 1][sequence[i][1]]].HP == "H": #If not sequential AND = H
                    energy -= 1
            #If not on upper border, check space above
            if sequence[i][1] != len(lattice)-1:
                if lattice[sequence[i][0]][sequence[i][1] + 1] not in (i-1, i+1, None) and original[lattice[sequence[i][0]][sequence[i][1] + 1]].HP == "H": #If not sequential AND = H
                    energy -= 1
            #If not on lower border, check space below
            if sequence[i][1] != 0:
                if lattice[sequence[i][0]][sequence[i][1] - 1] not in (i-1, i+1, None) and original[lattice[sequence[i][0]][sequence[i][1] - 1]].HP == "H": #If not sequential AND = H
                    energy -= 1
    return (int(energy/2))