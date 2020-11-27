# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 22:37:44 2020

@author: Ferna
"""

import pandas as pd
import math
import matplotlib.pyplot as plt
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
C_H = 35 #g/L
C_L = 5 #g/L
df = pd.DataFrame({'Ci (g/L)': [C_L, C_H]})
def Concentracion(fila):
    return fila["Ci (g/L)"]/MM
df["Ci (mol/L)"] = df.apply(Concentracion,axis=1)
#Fuerza iónica Carga =1
def Io(fila):
    return 0.5*(Zi)**2*fila["Ci (mol/L)"]
df["F_I"] = df.apply(Io, axis=1)
#Coeficiente de actividad
def g_Na(fila):
    return 10**((-A*(Zi)**2*math.sqrt(fila["F_I"])/(1+B*ai[0]*math.sqrt(fila["F_I"])))+bi[0]*(fila["F_I"]))
df["gNa"] = df.apply(g_Na, axis=1)
def g_Cl(fila):
    return 10**((-A*(Zi)**2*math.sqrt(fila["F_I"])/(1+B*ai[1]*math.sqrt(fila["F_I"])))+bi[1]*(fila["F_I"]))
df["gCl"] = df.apply(g_Cl, axis=1)
#Actividad
def A_Na(fila):
    return fila["Ci (mol/L)"]*fila["gNa"]
df["A_Na"] = df.apply(A_Na, axis=1)
def A_Cl(fila):
    return fila["Ci (mol/L)"]*fila["gCl"]
df["A_Cl"] = df.apply(A_Cl, axis=1)
#Constantes de Ec. Nernst
R= 8.314 #J/mol K
F= 96485 #C/mol
T = 298.15 #K
#Permselectivity
CEM = 0.99
AEM = 0.95
def E_CEM():
    return (CEM*R*T/(Zi*F))*math.log(df.loc[1,["A_Na"]]/df.loc[0,["A_Na"]])
print("E_CEM = ")
print(E_CEM())
def E_AEM():
    return (AEM*R*T/(Zi*F))*math.log(df.loc[1,["A_Cl"]]/df.loc[0,["A_Cl"]])
print("E_AEM = ")
print(E_AEM())
def Ecell():
    return E_AEM()+E_CEM()
print("E_celda = ")
print(Ecell())
N=10
def E():
    return N*Ecell()
print("E =")
print(E())
#Conductividad
ksal= 50 #Agua salada (mS/cm)
kdul= 7 #Agua dulce (mS/cm)
#Resistencias
A= 10*10 #cm2
Amem= A*N*2/10000 #m2
Relec= 54/A #ohm
R_CEM = 2.0/A #ohm
R_AEM = 1.7/A #ohm
dfRmembranas = pd.DataFrame({'Membrana':['CEM','AEM'],
                            'R (ohm)':[R_CEM, R_AEM]})
print(dfRmembranas)
R_H = 1/(ksal*(1000*10)) #ohm
R_L = 1/(kdul*(1000*10)) #ohm
dfcompart = pd.DataFrame({'Compartimiento':['High','Low'],
                          'R (ohm)':[R_H,R_L]})
r = R_L + R_H + R_CEM + R_AEM #ohm
print (r)
print("Resistencia interna")
Ri= N*r + Relec #ohm
print(Ri)
df2 = pd.DataFrame({'Rext (ohm)':[92,47,22,10,6.8,5.6,4.7,3.3,
                                  2.2,1.8,1.2,0.56, 0.39,0.22,0.1,0]})
#Intensidad de corriente
def I(fila):
    return E()/(Ri + fila["Rext (ohm)"])
df2["I (A)"] = df2.apply(I, axis=1)
def densI(fila):
    return I(fila)/(Amem)
df2["I (A/m2)"] = df2.apply(densI, axis=1)
#Potencia
def Pgross(fila):
    return fila["I (A)"]**2*fila["Rext (ohm)"]
df2["P (W)"] = df2.apply(Pgross, axis=1)
def densP(fila):
    return fila["P (W)"]/Amem
df2["P (W/m2)"] = df2.apply(densP, axis=1)
#Diferencia de potencial
def E2(fila):
    return fila["P (W)"]/fila["I (A)"]
df2["E (V)"] = df2.apply(E2, axis=1)
#Gráficos
fig1, ax1 = plt.subplots()
fig2, ax2 = plt.subplots()
ax1.plot(df2["I (A)"],df2["E (V)"],'r')
ax2.plot(df2["I (A)"],df2["P (W)"],'g')
ax1.set_title('Voltaje vs Intensidad')
ax1.set_ylabel('E (V)')
ax1.set_xlabel('I (A)')
ax2.set_title('Potencia vs Intensidad')
ax2.set_ylabel('P (W)')
ax2.set_xlabel('I (A)')
plt.tight_layout()


