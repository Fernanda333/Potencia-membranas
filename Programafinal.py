# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 19:10:10 2020

@author: Ferna
"""

import tkinter as tk
import numpy as np
import math
import pandas as pd
from matplotlib import style
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from tkinter import Tk, Label, Button, Entry, StringVar, Frame


#Constantes Debye-Hückel
A= 0.50917
B= 0.32832
#Carga y radio de los iones
#0-Na+, 1-Cl-
Zi= 1.0
ai= [4.0, 3.5]
bi= [0.075, 0.015]
#Concentración
MM= 58.44 #g/mol NaCl

#Constantes de Ec. Nernst
R= 8.314 #J/mol K
F= 96485 #C/mol
T = 298.15 #K
#Permselectivity
CEM = 0.99
AEM = 0.95
df2 = pd.DataFrame({'Rext (ohm)':[92,47,22,10,6.8,5.6,4.7,3.3,
                                  2.2,1.8,1.2,0.56, 0.39,0.22,0.1,0.0]})
#Conductividad
ksal= 50 #Agua salada (mS/cm)
kdul= 7 #Agua dulce (mS/cm)
#Resistencias
R_H = 1/(ksal*(1000*10)) #ohm
R_L = 1/(kdul*(1000*10)) #ohm


class Programa:
    
    def __init__(self, master):
        self.master = master
        master.title("Programa")
        
        self.var = 0
        self.var2 = 0
        self.var3 = 0
        
        self.canvas = None
        
        self.frame = Frame(master)
        self.frame2 = Frame(master)
        self.entrada1 = Entry(self.frame)
        self.entrada2 = Entry(self.frame)
        self.entrada3 = Entry(self.frame)
        self.entrada5 = Entry(self.frame)


        #Resultados
        self.e4= Label(self.frame,text= "Diferencia de potencial (V): ").grid(pady=5, row=6, column=0)
        self.var = StringVar()
        self.resultE= Label(self.frame, textvariable = self.var).grid(padx=5, row=6, column=1)
        self.e6= Label(self.frame,text= "Potencia máxima (W): ").grid(pady=5, row=7, column=0)
        self.var2= StringVar()
        self.resultP= Label(self.frame, textvariable = self.var2).grid(padx=5, row=7, column=1)
        self.e7= Label(self.frame,text= "Intensidad máxima (A): ").grid(pady=5, row=8, column=0)
        self.var3= StringVar()
        self.resultI= Label(self.frame, textvariable = self.var3).grid(padx=5, row=8, column=1)


        self.button = Button(self.frame, text= "Calcular",fg="blue", command=self.Calculo).grid(padx=10, pady=10, row=5, column=1, columnspan=1)
        self.clear_button = Button(self.frame, text="Borrar todo", command=self.delete).grid(padx=10, pady=10, row=5, column=0, columnspan=1)
        self.botoncierra= Button(self.frame, text= "Cerrar", command= self.cerrar).grid(padx=10, pady=10, row=9, column=0, columnspan=2)
        
        type(self.var)
        
        #LAYOUT

        self.frame.pack(side=tk.LEFT, fill= tk.X)
        self.frame2.pack()
        self.Intro= Label(self.frame,text= "Introduzca sus datos:", font = '30').grid(pady=5, row=0, column=0, columnspan=2) 
        self.e1=tk.Label(self.frame,text= "Concentración baja (g/L): ").grid(pady=5, row=1, column=0) 
        self.e2=tk.Label(self.frame,text= "Concentración alta (g/L): ").grid( pady=5, row=2, column=0)
        self.e3=tk.Label(self.frame,text= "# pares de membranas: ").grid(pady=5, row=3, column=0)
        self.e5=tk.Label(self.frame,text= "Área de la celda (cm2): ").grid(pady=5, row=4, column=0)
    
        
        self.entrada1.grid(padx=5, row=1, column=1)
        self.entrada2.grid(padx=5, row=2, column=1)
        self.entrada3.grid(padx=5, row=3, column=1)
        self.entrada5.grid(padx=5, row=4, column=1)
        

    def Calculo(self):
        C_L= float(self.entrada1.get())
        C_H = float(self.entrada2.get())
        C_L2 = C_L/MM
        C_H2 = C_H/MM
        #Fuerza iónica Carga =1
        Io_L= 0.5*(Zi)**2*C_L2
        Io_H= 0.5*(Zi)**2*C_H2
        #Coeficiente de actividad
        g_NaL=10**((-A*(Zi)**2*math.sqrt(Io_L)/(1+B*ai[0]*math.sqrt(Io_L)))+bi[0]*(Io_L))
        g_NaH=10**((-A*(Zi)**2*math.sqrt(Io_H)/(1+B*ai[0]*math.sqrt(Io_H)))+bi[0]*(Io_H))
        g_ClL=10**((-A*(Zi)**2*math.sqrt(Io_L)/(1+B*ai[1]*math.sqrt(Io_L)))+bi[1]*(Io_L))
        g_ClH=10**((-A*(Zi)**2*math.sqrt(Io_H)/(1+B*ai[1]*math.sqrt(Io_H)))+bi[1]*(Io_H))
        #Actividad
        A_NaL= C_L2*g_NaL
        A_NaH= C_H2*g_NaH
        A_ClL= C_L2*g_ClL
        A_ClH= C_H2*g_ClH
        #Potencial
        E_CEM = (CEM*R*T/(Zi*F))*math.log(A_NaH/A_NaL)
        E_AEM = (AEM*R*T/(Zi*F))*math.log(A_ClH/A_ClL)
        Ecell = E_CEM + E_AEM
        N= int(self.entrada3.get())
        self.E= N*Ecell
        Acell= float(self.entrada5.get())
        Amem= Acell*N*2/10000 #m2
        Relec= 54/Acell #ohm
        R_CEM = 2.0/Acell #ohm
        R_AEM = 1.7/Acell #ohm
        r = R_L + R_H + R_CEM + R_AEM #ohm
        Ri= N*r + Relec #ohm
        self.I = self.E/(Ri + df2[:]) #A
        densI = self.I / Amem #A/m2
        self.Pgross = self.I**2*df2[:] #W
        densP = self.Pgross/ Amem #W/m2
        self.E2 = self.Pgross/self.I #V
        Maximo= self.Pgross.max() #W
        Pmax= float(Maximo)
        n = int(self.Pgross.idxmax())
        Imax = float(self.I.iloc[n]) #A
        
        
        self.fig = Figure(figsize=(8,8))
        ax1 = self.fig.add_subplot(1,2,1)
        ax2 = self.fig.add_subplot(1,2,2)
        ax1.plot(self.I,self.Pgross,'.',color='g')
        ax2.plot(self.I,self.E2,marker='.')
        ax1.set_xlabel('I (A)')
        ax1.set_ylabel('P (W)')
        ax2.set_xlabel('I (A)')
        ax2.set_ylabel('E (V)')
        ax1.set_title('Potencia vs intensidad')
        ax2.set_title('Voltaje vs intensidad')
        ax1.grid(color='white')
        ax2.grid(color='white')
        
        style.use('seaborn-darkgrid')
        
        self.canvas = FigureCanvasTkAgg(self.fig,self.frame2)  
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
           
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.frame2)
        self.toolbar.update()
    
        return (self.var.set("{:.4f}".format(self.E)), self.var2.set("{:.4f}".format(Pmax)), self.var3.set("{:.4f}".format(Imax)))


        
    def delete(self):
        self.entrada1.delete(0,'end')
        self.entrada2.delete(0,'end')
        self.entrada3.delete(0,'end')
        self.entrada5.delete(0,'end')
        self.var.set(0.0)
        self.var2.set(0.0)
        self.var3.set(0.0)
        self.canvas.get_tk_widget().destroy()
        self.toolbar.destroy()
        
        
    def cerrar(self):
        root.destroy()
        
root = Tk()
root.configure()
my_gui = Programa(root)
root.mainloop()