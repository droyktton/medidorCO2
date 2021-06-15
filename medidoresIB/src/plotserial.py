#!/usr/bin/env python
# coding: utf-8

## lee el puerto serial que escribe el medidor
## y dibuja co2, T, H en un gráfico

# referencia
#http://www.mikeburdis.com/wp/notes/plotting-serial-port-data-using-python-and-matplotlib/

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
	print("\nTodo ok, puerto serial abierto. Configuracion:\n")
	print(ser, "\n") #print serial parameters

#figura
fig, ax = plt.subplots(3)
plt.locator_params(axis="x", nbins=5)
plt.locator_params(axis="y", nbins=5)
fig.tight_layout(pad=2, w_pad=0.5, h_pad=1.0)
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
            co2.append(int(lista[1].strip()))
            T.append(int(lista[3].strip()))
            H.append(int(lista[5].strip()))		
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
            ax[0].plot(elap, co2,"-r*")
            ax[0].set(xlabel='segundos', ylabel='CO2 [ppm]')
            
            ax[1].clear()
            ax[1].plot(elap, T,"-b*")
            ax[1].set(xlabel='segundos', ylabel='T [C]')

            ax[2].clear()
            ax[2].plot(elap, H, "-m*")
            ax[2].set(xlabel='segundos', ylabel='Humedad Relativa [%]')
        
            for i in range(3):
                ax[i].xaxis.set_major_locator(plt.MaxNLocator(5))
                ax[i].yaxis.set_major_locator(plt.MaxNLocator(5))

# Set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig, animate, fargs=(fecha,elap,co2,T,H), interval=100)
plt.show()
