# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 19:10:10 2020

@author: Ferna
"""

import pandas as pd
import math
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import PhotoImage,TOP,BOTH
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
ventana = tk.Tk()
ventana.geometry("500x600")
ventana.title("Cálculo de diferencia de potencial")
ventana.configure()
var=tk.StringVar()

root = tk.Tk()
root.wm_title("Gráfica")

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

#Imagen 
RED=PhotoImage(file='Imagen5.png')
imagen1 = tk.Label(ventana, image=RED, anchor ="center")
imagen1.pack(side=TOP, fill=BOTH, expand=True, 
                          padx=10, pady=5)     

#Etiquetas
e1=tk.Label(ventana,text= "Concentración baja (g/L): ", bg = "#37667E", fg="white")
e1.pack(padx=5, pady=4, ipadx=5, fill=tk.X)
entrada1 = tk.Entry(ventana)
entrada1.pack(fill=tk.X, padx=5, pady=5, ipadx=5, ipady=5)

e2=tk.Label(ventana,text= "Concentración alta (g/L): ", bg = "#37667E", fg="white")
e2.pack(padx=5, pady=4, ipadx=5, fill=tk.X)
entrada2 = tk.Entry(ventana)
entrada2.pack(fill=tk.X, padx=5, pady=5, ipadx=5, ipady=5)

e3=tk.Label(ventana,text= "# pares de membranas: ", bg = "#37667E", fg="white")
e3.pack(padx=5, pady=4, ipadx=5, fill=tk.X)
entrada3 = tk.Entry(ventana)
entrada3.pack(fill=tk.X, padx=5, pady=5, ipadx=5, ipady=5)

e5=tk.Label(ventana,text= "Área de la celda (cm2): ", bg = "#37667E", fg="white")
e5.pack(padx=5, pady=4, ipadx=5, fill=tk.X)
entrada5 = tk.Entry(ventana)
entrada5.pack(fill=tk.X, padx=5, pady=5, ipadx=5, ipady=5)

#Constantes de Ec. Nernst
R= 8.314 #J/mol K
F= 96485 #C/mol
T = 298.15 #K
#Permselectivity
CEM = 0.99
AEM = 0.95
df2 = pd.DataFrame({'Rext (ohm)':[92,47,22,10,6.8,5.6,4.7,3.3,
                                  2.2,1.8,1.2,0.56, 0.39,0.22,0.1,0]})

#Conductividad
ksal= 50 #Agua salada (mS/cm)
kdul= 7 #Agua dulce (mS/cm)
#Resistencias
R_H = 1/(ksal*(1000*10)) #ohm
R_L = 1/(kdul*(1000*10)) #ohm

def E():
    C_L= float(entrada1.get())
    C_H = float(entrada2.get())
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
    N= int(entrada3.get())
    E= N*Ecell
    Acell= float(entrada5.get())
    Amem= Acell*N*2/10000 #m2
    Relec= 54/Acell #ohm
    R_CEM = 2.0/Acell #ohm
    R_AEM = 1.7/Acell #ohm
    r = R_L + R_H + R_CEM + R_AEM #ohm
    Ri= N*r + Relec #ohm
    I = E/(Ri + df2[0:]) #A
    densI = I / Amem #A/m2
    Pgross = I**2*df2[0:] #W
    densP = Pgross/ Amem #W/m2
    E2 = Pgross/I #V
    #Graficas
    fig = plt.figure(figsize=(10,10))
    fig.tight_layout()
    ax1 = fig.add_subplot(1,2,1)
    ax2 = fig.add_subplot(1,2,2)
    ax1.plot(I,Pgross,'r')
    ax2.plot(I,E2,marker='*')
    ax1.set_xlabel('I (A)')
    ax1.set_ylabel('P (W)')
    ax2.set_xlabel('I (A)')
    ax2.set_ylabel('E (V)')
    ax1.set_title('Potencia vs intensidad')
    ax2.set_title('Voltaje vs potencia')
    ax1.grid()
    ax2.grid()
    plt.show
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    return (var.set(E))

def cerrar():
    ventana.destroy()
    root.destroy()

botons=tk.Button(ventana, text="Calcular",
                 fg="blue", command=E)
botons.pack(side=tk.TOP)

e4=tk.Label(ventana,text= "Diferencia de potencial (V): ",bg = "#37667E", fg="white")
e4.pack(padx=5, pady=4, ipadx=5, fill=tk.X)
result=tk.Label(ventana, textvariable = var, padx=5, pady=5,width= 50)
result.pack()

botoncierra= tk.Button(ventana, text= "Cerrar", fg= "blue", command= cerrar)
botoncierra.pack(side = tk.TOP)

ventana.mainloop()
