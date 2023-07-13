# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 12:11:40 2023

@author: User
"""
#Variables
lattice = []

#Nodes (stored in "sequence" variable)
class node:
    def __init__(self, ID, HP):
        self.ID = ID
        self.HP = HP
        self.coord = None
        
    def __repr__(self):
      return repr(str(self.HP) + ", " + str(self.coord))



#Read file and validate
def file_check(fileName):
    sequence = []
    
    #Read text file, add nodes to sequence
    with open(fileName) as f:
        contents = f.read().rstrip()
    contents = contents.upper() #Convert string to upper
    
    if not contents: valid = False
    else:
        valid = True
        #If sequence contains anything but H/h or P/p (or empty), input is invalid
        for i in contents:
            if i != 'H' and i != 'P' or not contents:
                valid = False
                break

    #Input validation check
    if valid:
        #Create each node
        for x in range(len(contents)):
            x = node(x, contents[x])
            sequence.append(x)
        return (sequence)
    else:
        return (False)


#Create sequence array and starting lattice
def lattice_get(sequence):
    #Assigning values to list
    lattice = []
    
    x = round(len(sequence)/2)
    for i in range (len(sequence)):
        lattice.append([None] * len(sequence))
    
    for i in range (len(sequence)):
        lattice[i][x] = sequence[i].ID #Lattice stores ints of IDs
        sequence[i].coord = (i, x)

    return(lattice)