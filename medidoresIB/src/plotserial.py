#!/usr/bin/env python
# coding: utf-8

## lee el puerto serial que escribe el medidor
## y dibuja co2, T, H en un gráfico

#instalar serial:
#https://pyserial.readthedocs.io/en/latest/pyserial.html#installation

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import numpy as np
import random
import serial
import time
import datetime

#inicializa el serial port
ser = serial.Serial()
ser.port = '/dev/ttyACM0' #Arduino serial port
ser.baudrate = 9600
ser.timeout = 10 #specify timeout when using readline()
ser.open()
if ser.is_open==True:
	print("\nAll right, serial port now open. Configuration:\n")
	print(ser, "\n") #print serial parameters

#figura
fig, ax = plt.subplots(3)
fig.tight_layout()
fig.show()

#arrays
co2=[]
T=[]
H=[]
elap=[]
fecha=[]

start=time.time()

# Esta funcion se llama periodicamente desde FuncAnimation
def animate(i,fecha,elap,co2,T,H):

    #Aquire and parse data from serial port
    line = ser.readline()
    s=line.decode("utf-8")
    if len(s)>0: 
        lista=s.split(sep=" ")
        if lista[0]=="co2(ppm):":
            co2now=int(lista[1])
            co2.append(lista[1])
            T.append(lista[3])
            H.append(lista[5])		
            elap.append(time.time()-start)
            fecha.append(str(datetime.datetime.now()))
            
            # Limit x and y lists to 20 items
            #co2 = co2[-20:]
            #T = T[-20:]
            #H = H[-20:]
            #elap = elap[-20:]
            #fecha = fecha[-20:]
        
            # Dibuja las tres series temporales
            ax[0].clear()
            ax[0].plot(elap, co2,"-r", label="CO2 ppm")
            ax[0].set(xlabel='segundos', ylabel='CO2 [ppm]')
            
            ax[1].clear()
            ax[1].plot(elap, T,"-b", label="Temperatura")
            ax[1].set(xlabel='segundos', ylabel='T [C]')

            ax[2].clear()
            ax[2].plot(elap, H, "-m", label="CO2 ppm")
            ax[2].set(xlabel='segundos', ylabel='Humedad Relativa [%]')

# Set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig, animate, fargs=(fecha,elap,co2,T,H), interval=1000)
plt.show()
