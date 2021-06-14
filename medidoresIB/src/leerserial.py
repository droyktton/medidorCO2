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

#un numero máximo de lecturas
N=10000000

start=time.time()
with open('medidor.dat', 'w') as the_file:
    print("preparado el archivo (medidor.dat)")
    the_file.write("fecha,elap,co2,temp,humedad\n")
    with serial.Serial('/dev/ttyACM0', 9600, timeout=1) as ser:
        print("preparado el puerto serial")
        print("midiendo...")
        for i in range(0,N,1):
            line = ser.readline()
            s=line.decode("utf-8")
            if len(s)>0: 
                lista=s.split(sep=" ")
                if lista[0]=="co2(ppm):":
                    elap=time.time()-start
                    the_file.write(str(datetime.datetime.now())+","+str(elap)+","+str(lista[1])+","+str(lista[3])+","+str(lista[5]))
                the_file.flush()





