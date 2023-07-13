# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 12:46:22 2023

@author: User
"""

#Uhhh slight issue, there is overlapping nodes, again :'))
#Also seems to discard all moves sometimes (likely annealing shiz)

from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from PIL import Image
import os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import sequence as Sq
import moves
import results


class program:    
    def __init__(self, master):
        self.master = master
        master.title("HP Protein Folding Simulation")
        master.geometry("900x620")
        master.resizable(False, False)
        master.iconbitmap("../assets/icon.ico")
        self.lines = 0
        self.nodeList = []
        self.lineList = []
        self.energy = 0
        self.sequence = None
        
        #Header (Title + help)
        self.header = Frame(master)
        self.header.pack(fill="both", expand=1)
        self.title = Label(self.header, text="HP protein Folding Simulation", font="Helvetica 14")
        self.helpico = PhotoImage(file='../assets/help.png')
        self.graphico = PhotoImage(file='../assets/graph.png')
        self.saveico = PhotoImage(file='../assets/save.png')
        self.helpButt = Button(self.header, image=self.helpico, command=self.helpCom, highlightthickness = 0, bd = 0)
        self.helpButt.pack(side=RIGHT, pady=(5,0), padx=10)
        self.graphButt = Button(self.header, image=self.graphico, command=self.graph_win)
        self.graphButt.pack(side=RIGHT, pady=(5,0), padx=10)
        self.saveButt = Button(self.header, image=self.saveico, command=self.save_data, state=DISABLED)
        self.saveButt.pack(side=RIGHT, pady=(5,0), padx=10)
        self.title.pack(side=LEFT, pady=(5,0), padx=10)
        
        #Frame (leftside GUI)
        self.frame = Frame(master, relief=RIDGE, borderwidth=5, width=300)
        self.frame.pack(side=LEFT, fill=Y, pady=(5,10), padx=10)
        self.frame.pack_propagate(0)

        #Canvas (rightside GUI)
        self.canWdth = 550
        self.canHght = 550
        self.canv = Canvas(master, width=self.canWdth, height=self.canHght, bg="white")
        self.canv.pack(fill=BOTH, expand=YES, pady=10, padx=10)

        #Frame buttons + labels
        self.fileSelectButt = self.buttonCreate("Select File", self.file_select, 1, TOP)
        
        Label(self.frame, text="Selected sequence preview:").pack(side=TOP)
        self.seqTxt = Label(self.frame, bg='#A5A5A5', height=5, wraplength=200)
        self.seqTxt.pack(side=TOP, padx=20, fill=X)
        
        self.fileDisTxt = Label(self.frame, font="Helvetica 8 italic")
        self.fileDisTxt.pack(side=TOP, padx=20, anchor='e')
        
        #Entry fields
        #Generations entry
        ttk.Separator(self.frame, orient='horizontal').pack(side=TOP, fill=X, padx=20, pady=[20,0], anchor='center')
        Label(self.frame, text='Number of generations:').pack(side=TOP, padx=20, anchor='w')
        self.genEntry = Entry(self.frame)
        self.genEntry.insert(END, '20')
        self.genEntry.pack(side=TOP, padx=20, anchor='w')
        #Moves entry
        Label(self.frame, text='Moves in each generation:').pack(side=TOP, padx=20, anchor='w')
        self.movesEntry = Entry(self.frame)
        self.movesEntry.insert(END, '10')
        self.movesEntry.pack(padx=20, anchor='w')
        
        
                
        #Methods Menu
        self.mFrame = Frame(self.frame, height=190)
        self.mFrame.pack(fill=X)
        ttk.Separator(self.mFrame, orient='horizontal').pack(side=TOP, fill=X, padx=20, pady=[20,0])
        self.mFrame.pack_propagate(0) 
        Label(self.mFrame, text="Generation selection method: ").pack(side=TOP, padx=20, anchor='w')
        self.method = ["Hill Climb", "Annealing", "Genetic (HC)"]
        self.selected = StringVar()
        self.selected.set("Hill Climb")
        self.dropMenu = OptionMenu(self.mFrame, self.selected, *self.method)
        self.dropMenu.pack(side=TOP, padx=20, anchor='w')
        
        #Temperature entry (simulated annealing)
        self.tempLabel = Label(self.mFrame, text='Temperature:')
        self.tEntry = Entry(self.mFrame)
        self.tEntry.insert(END, '3')
        Label(self.mFrame, text='Run mode').pack(side=BOTTOM, padx=20)
        ttk.Separator(self.mFrame, orient='horizontal').pack(side=BOTTOM, fill=X, padx=20, anchor='center')
                
        #Parent number (genetic algorithms)
        self.parLabel = Label(self.mFrame, text='Parent candidades:')
        self.parentEntry = Entry(self.mFrame)
        self.parentEntry.insert(END, '3')
        self.selected.trace_add('write', self.method_options)
        
        
        #Startover button (erases selected file)
        self.starOverButt = self.buttonCreate("Start Over", self.start_over, 3, BOTTOM)
        self.starOverButt.config(state= DISABLED, bg='grey')
        
        #Generate button (generates lattice on sequence + perameters)
        self.generateButt = self.buttonCreate("Generate", self.generate, 3, BOTTOM)
        self.generateButt.config(state= DISABLED, bg='grey')
        
        
        #Run mode options
        ttk.Separator(self.mFrame, orient='horizontal').pack(side=BOTTOM, padx=20)
        self.runMode = BooleanVar(self.frame)
        self.runFast = Radiobutton(self.frame, text="Fast", variable=self.runMode, value=0).pack(side=LEFT, padx=40)
        self.runSlow = Radiobutton(self.frame, text="Slow", variable=self.runMode, value=1).pack(side=RIGHT, padx=40)
        
                
        self.canv.pack(fill="x", expand=1, pady=10, padx=10)

    
    #File select
    def file_select(self):
        self.canv.delete('all')
        fileName = askopenfilename()
        self.sequence = Sq.file_check(fileName) #Checks if file is valid (only H and Ps)
        
        self.fileDisTxt.config(text = fileName.split("/")[-1])
        if isinstance (self.sequence, list): #If valid, assign to variables and draw display
            self.generateButt.config(state= NORMAL, bg='blue')
            self.draw_lattice()
        else:
            messagebox.showinfo(title="Error", message="Invalid file. Please chose a valid sequence txt.")
            self.seqTxt.config(text = "Invalid file.")         
        
    
    
    
    
    #Draw the initial lattice
    def draw_lattice(self):
        #Clear previous data
        lines = 0
        self.canv.delete('all')
        self.lineList.clear()
        self.nodeList.clear()
        self.score = self.canv.create_text(50, self.canHght - 15, font="Helvetica 12 italic")
        lattice = Sq.lattice_get(self.sequence)
        
       #Grid
        lines += (self.canWdth - 20) / (len(lattice[0]) + 1) #spacing of lines (padding of 10px)
        #Drawing grid
        for i in range (len(lattice[0]) + 1):
            self.canv.create_line(10, i * lines, self.canWdth - 10, i * lines, fill="light grey")
            self.canv.create_line(i * lines, 10, i * lines, self.canHght - 30, fill="light grey")
        #Drawing nodes
        dispText = ''
        for idx, i in enumerate(lattice):
            for jdx, j in enumerate(lattice[idx]):
                x = (jdx + 1) * lines
                y = (idx + 1) * lines
                if lattice[idx][jdx] != None:
                    #Connecting lines
                    if idx != len(lattice) and idx != 0:
                        newLine = self.canv.create_line(x, y, x, (y+1) - lines, fill="black", width=2, tags="connector")
                        self.lineList.append(newLine) #Append connecting line to list
                    #Nodes
                    HP = self.sequence[lattice[idx][jdx]].HP
                    if HP == "H":
                        fill = "blue"
                    else:
                        fill = "red"
                    newNode = self.canv.create_oval(x - lines/3, y - lines/3, x + lines/3, y + lines/3, fill=fill, width=0)
                    self.nodeList.append(newNode) #Append node to list
                    dispText += HP
        self.canv.tag_lower('connector')
        self.seqTxt.config(text = dispText)
        self.canv.itemconfig(self.score, text="Energy: 0")
        self.lines = lines
    
    
    
    #Update lattice after a valid move
    def upd_graphic(self, wait):
        self.canv.itemconfig(self.score, text="Energy: "+str(self.energy))
        #Move nodes on graph
        for idx, x in enumerate(self.nodeList):
            self.canv.moveto(x,(self.sequence[idx].coord[1] + 1) * self.lines - self.lines/3, (self.sequence[idx].coord[0] + 1) * self.lines - self.lines/3)
            if idx != len(self.nodeList)-1: #Move connecting lines
                self.canv.moveto(self.canv.coords(self.lineList[idx], (self.sequence[idx].coord[1] + 1) * self.lines, (self.sequence[idx].coord[0] + 1) * self.lines, (self.sequence[idx + 1].coord[1] + 1) * self.lines, (self.sequence[idx + 1].coord[0] + 1) * self.lines))

        if wait == 1:
            waitVar = IntVar()
            self.master.after(300, waitVar.set, 1)
            self.master.wait_variable(waitVar)
        
        
        
    #Generate new conformation
    def generate(self):
        #If input is valid, proceed
        if self.genEntry.get().isdigit() and self.movesEntry.get().isdigit() and (self.parentEntry.get().isdigit() or self.selected.get() != "Annealing") and (self.tEntry.get().isdigit() or self.selected.get() != "Genetic (HC)"):                  
            #Reset values
            self.energy = 0
            for i in self.sequence:
                i.coord = (i.ID, round(len(self.sequence)/2))
            
            #Disable buttons
            self.generateButt.config(state= DISABLED, bg='grey')
            self.fileSelectButt.config(state= DISABLED, bg='grey')
            #Get user entered(or default) perameters
            if self.selected.get() == "Annealing":sendt = float(self.tEntry.get())
            else: sendt = ""
            if self.selected.get() == "Genetic (HC)": sendPar = int(self.parentEntry.get())
            else: sendPar = 1
            results.set_vars(int(self.genEntry.get()), int(self.movesEntry.get()), sendt, sendPar, self.fileDisTxt.cget("text"))
           
            #Runs moveset for x ammount
            for x in range (results.gens):
                output = moves.move_manager(self.sequence, self.energy, int(self.movesEntry.get()), x, sendt, sendPar)
                
                #IF new generation returned
                if isinstance (output, tuple):
                    self.energy = output[0]
                    #Copy new coordinates
                    for i in self.sequence:
                        i.coord = output[1][i.ID]
                else: self.energy = output
                
                results.append_energy(self.energy)
                if (self.runMode.get() == 1 and isinstance (output, tuple)) or x == results.gens-1: self.upd_graphic(self.runMode.get()) #Update graphics
            
            #End
            results.draw_graph()
            self.generateButt.config(state= NORMAL, bg='blue')
            self.starOverButt.config(state= NORMAL, bg='blue')
            self.saveButt.config(state=NORMAL)
            self.graphButt.config(state=NORMAL)
            
            #If graph window is open, update graphics
            try:
                self.graphWin.winfo_exists()
            except (NameError, AttributeError):
                pass
            else:
                self.grapCanv.draw()
        else:
            messagebox.showinfo(title="Error", message="Invalid values. Please enter positive integers.")
        


    #If save button is clicked
    def save_data(self):
        fileName = (results.save_data()+"(image)")
        self.canv.postscript(file=fileName+".ps", colormode='color')
        self.saveForm = Image.open(fileName+".ps")
        self.saveForm.save(fileName+".png")
        self.saveForm.close()
        os.remove(fileName+".ps")
        messagebox.showinfo(title="Run saved", message="The run has been saved under\n "+fileName+"(graph/image).png")
           
    
    #Erase all values to start again
    def start_over(self):
        self.canv.delete('all')
        self.energy = 0
        self.fileDisTxt.config(text = "")
        self.seqTxt.config(text= "")
        self.generateButt.config(state=DISABLED, bg='grey')
        self.starOverButt.config(state=DISABLED, bg='blue')
        self.fileSelectButt.config(state=NORMAL, bg='blue')
        self.saveButt.config(state=DISABLED)
        self.graphButt.config(state=DISABLED)
        
    
    #Button template
    def buttonCreate(self, text, command, height, side):
        button = Button(self.frame, text=text, command=command, bg='blue', fg='white')
        button.pack(side=side, padx=10, pady=5, fill=X)
        return button
    
    #Enable/disable temperature entry with annealing selected/deselected
    def method_options(self, *args):
        if self.selected.get() == "Hill Climb":
            self.tempLabel.pack_forget()
            self.tEntry.pack_forget()
            self.parLabel.pack_forget()
            self.parentEntry.pack_forget()
        if self.selected.get() == "Annealing":
            self.tempLabel.pack(side=TOP, padx=30, anchor='w')
            self.tEntry.pack(side=TOP, padx=30, anchor='w')
            self.parLabel.pack_forget()
            self.parentEntry.pack_forget()
        elif self.selected.get() == "Genetic (HC)":
            self.tempLabel.pack_forget()
            self.tEntry.pack_forget()
            self.parLabel.pack(side=TOP, padx=30, anchor='w')
            self.parentEntry.pack(side=TOP, padx=30, anchor='w')

    #Graph display window
    def graph_win(self):
        self.graphWin = Toplevel(self.master)
        self.graphWin.geometry("500x500")
        self.graphWin.resizable(False, False)
        self.graphWin.iconbitmap("../assets/icon.ico")
        
        self.grapCanv = FigureCanvasTkAgg(results.graph, master=self.graphWin)
        self.grapCanv.draw()
        self.grapCanv.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)


    #Help window (triggered by right-top help icon of main window)
    def helpCom(self):
        self.helpWin = Toplevel(self.master)
        self.helpWin.geometry("550x300")
        self.helpWin.resizable(False, False)
        self.helpWin.iconbitmap("../assets/icon.ico")
        Label(self.helpWin, text="Program Instructions", font="Helvetica 13").pack(fill=X)
        self.helpFrame = Frame(self.helpWin, relief=RIDGE, bd=2)
        Label(self.helpFrame, wraplength=530, justify=LEFT,
              text="This HP protein folding simulation program provides a look at possible algorithms to find a 2D HP model protein's optimal fold. First, select a .txt file. This file must contain a sequence of only Hs and Ps (no spaces allowed.)\nNext, the perameters can be modified to produce different results.\n").pack()
        Label(self.helpFrame, wraplength=530,
              text="Generation number: The number of times new conformations are attempted.\n\nMoves per generations: In-plane moves that are performed each generation attempt.\n\nAnnealing: To accept a conformation based on annealing algorithms. If ticked no, only attempts that produce a more optimal conformation are accepted as a new generation.\n").pack()
        Label(self.helpFrame, wraplength=530, justify=LEFT,
              text="Saved results are saved as both a graph and a screenshot of the final generation in the program's output folder. Directory can be changed in the UI.py code.").pack()
        self.helpFrame.pack(anchor=N, fill=BOTH, expand=True, padx=5, pady=5)


#Tkinter window
win = Tk()
gui = program(win)
win.mainloop()