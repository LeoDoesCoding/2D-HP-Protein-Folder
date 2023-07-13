# -*- coding: utf-8 -*-
"""
Created on Thu Apr  6 07:40:22 2023

@author: User
"""
import matplotlib.pyplot as plt
from datetime import datetime

energyList = [0] #index = runs
graph = plt.figure(figsize=(5, 4))

#Update graph
def draw_graph():
    graph.clear()
    axes = graph.add_subplot()
    axes.plot(range(len(energyList)), energyList)
    axes.set_xlabel('Generation', fontsize=12)
    axes.set_ylabel('Energy', fontsize=12)
    axes.locator_params(axis="both", integer=True, tight=True) #Set to integers only
    graph.subplots_adjust(bottom=0.3)
    
    axes.set_title((title+"\n"+file), fontsize=17)
    footer="Final energy score: {}\nNumber of generations: {}\nFolds per generation: {}".format(energyList[-1],gens,moves)
    footer+=temperature
    footer+=parent
    axes.plot(range(len(energyList)), energyList)
    axes.annotate(footer, (0,0), (0, -50), xycoords='axes fraction', textcoords='offset points', va='top', fontsize=14)
    
    
 
#Each generation, add energy output to list
def append_energy(newEnergy):
    energyList.append(int(newEnergy))
    

    
#If user wishes to save their data, save graph and return file name   
def save_data():
    fileName = ("../output/"+str(datetime.now().strftime("%d%m%y-%H%M%S")))
    plt.savefig(fileName+'(graph).png')
    return(fileName)


#Set variables when "Generate" is clicked
def set_vars(g, m, t, p, filename):
    global title, temperature, parent, gens, moves, file, energyList
    gens = g
    moves = m
    if isinstance(t, int):
        temperature = "\nAnnealing temperature: "+str(t)
        parent = ""
        title = "Annealing"
    elif p > 1:
        parent = "\nParent candidates: "+str(p)
        title = "Genetic Algorithm"
        temperature = ""
    else:
        title = "Hill Climb"
        parent = ""
        temperature = ""
    file = filename
    
    energyList=[0]