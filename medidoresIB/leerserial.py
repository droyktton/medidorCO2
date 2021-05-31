#!/usr/bin/env python
# coding: utf-8

## lee el puerto serial que escribe el medidor
## e imprime co2, T, H en un file "medidor.dat"

#instalar serial:
#https://pyserial.readthedocs.io/en/latest/pyserial.html#installation

import serial
import numpy as np
import matplotlib.pyplot as plt
import time
import datetime

N=10000000

co2=[]
T=[]
H=[]

start=time.time()
with open('medidor.dat', 'w') as the_file:
    with serial.Serial('/dev/ttyACM0', 9600, timeout=1) as ser:
        for i in range(0,N,1):
            line = ser.readline()
            s=line.decode("utf-8")
            if len(s)>0: 
                lista=s.split(sep=" ")
                if lista[0]=="co2(ppm):":
                    elap=time.time()-start
                    the_file.write(str(datetime.datetime.now())+" "+str(elap)+" "+str(lista[1])+" "+str(lista[3])+" "+str(lista[5]))
                    co2.append(lista[1])
                    T.append(lista[3])
                    H.append(lista[5])
                the_file.flush()

# serie temporal de co2
# plt.plot(np.arange(0,len(co2)), co2, label='CO2')
# plt.legend()
# plt.show()






