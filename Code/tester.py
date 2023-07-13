# -*- coding: utf-8 -*-
"""
Created on Mon May 29 08:46:55 2023

@author: User
"""
import numpy as np
import sequence as Sq

def valid_config(sequence):
    lattice = Sq.lattice_get(sequence)
    print(sequence)
    
    #checker stores each ID of the nodes in lattice
    checker = [0] * len(sequence)
    
    #Checking off each node in lattice
    for i in range(len(lattice)):
        for j in range(len(lattice[i])):
            if lattice[i][j] != None:
                checker[lattice[i][j]] += 1
                
    #If a node has not been checked off, report error         
    for x in checker:
        if x != 1:
            print (np.matrix(lattice))
            print ("INCORRECT!\n",checker,"\n",sequence,"\n\n")
            return()
        
    print ("OK!\n",checker,"\n",sequence,"\n\n")
    return()
