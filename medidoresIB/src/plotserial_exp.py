#!/usr/bin/env python
# coding: utf-8

## lee el puerto serial que escribe el medidor
## e imprime co2, T, H en un file "medidor.dat"

#instalar serial:
#https://pyserial.readthedocs.io/en/latest/pyserial.html#installation

# import serial
# import numpy as np
# import matplotlib.pyplot as plt
# import time
# import datetime

# N=10000000

# co2=[]
# T=[]
# H=[]

# start=time.time()
# with open('medidor.dat', 'w') as the_file:
#     the_file.write("fecha,elap,co2,temp,humedad\n")
#     with serial.Serial('/dev/ttyACM0', 9600, timeout=1) as ser:
#         for i in range(0,N,1):
#             line = ser.readline()
#             s=line.decode("utf-8")
#             if len(s)>0: 
#                 lista=s.split(sep=" ")
#                 if lista[0]=="co2(ppm):":
#                     elap=time.time()-start
#                     the_file.write(str(datetime.datetime.now())+","+str(elap)+","+str(lista[1])+","+str(lista[3])+","+str(lista[5]))
#                     co2.append(lista[1])
#                     T.append(lista[3])
#                     H.append(lista[5])
#                 the_file.flush()
# por ejemplo, uno podria el script en backgrou y correr cada 5 minutos, estos comandos, para visualizar en una pagina web
# cp medidor.dat ~/Codigos/loscoihues/ventilacion/
# git add medidor.dat dibujo.html; git commit -m "medidor CO2 update"; git push

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import numpy as np
import random
import serial
import time
import datetime
#import plotly.graph_objects as go
#import plotly.io as pio
#pio.renderers.default = 'browser'
#from plotly.offline import plot as plotoff 
#import streamlit as st

#initialize serial port
ser = serial.Serial()
ser.port = '/dev/ttyACM0' #Arduino serial port
ser.baudrate = 9600
ser.timeout = 10 #specify timeout when using readline()
ser.open()
if ser.is_open==True:
	print("\nAll right, serial port now open. Configuration:\n")
	print(ser, "\n") #print serial parameters

# Create figure for plotting
#fig = plt.figure()
#ax = fig.add_subplot(1, 1, 1)

co2now=400

fig, ax = plt.subplots(3)
fig.tight_layout()

# fig2 = go.Figure(go.Indicator(
#     domain = {'x': [0, 1], 'y': [0, 1]},
#     value = co2now,
#     mode = "gauge+number+delta",
#     title = {'text': "CO2 [ppm]"},
#     delta = {'reference': 400},
#     gauge = {'axis': {'range': [400, 2000]},
#              'steps' : [
#                  {'range': [400, 500], 'color': "lightblue"},
#                  {'range': [500, 600], 'color': "lightgreen"},
#                  {'range': [600, 700], 'color': "yellow"},
#                  {'range': [700, 800], 'color': "orange"},
#                  {'range': [800, 2000], 'color': "red"}],
#              'threshold' : {'line': {'color': "black", 'width': 4}, 'thickness': 0.75, 'value': 800}}))
#fig2.update_traces(value=888, selector=dict(type='indicator'))


fig.show()
#fig2.show()
#plotoff(fig2)
#pio.show(fig2)
#st.plotly_chart(fig2) 

co2=[]
T=[]
H=[]
elap=[]
fecha=[]

start=time.time()

# This function is called periodically from FuncAnimation
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
            #xs = xs[-20:]
            #ys = ys[-20:]
        
            # Draw x and y lists
            # Format plot
            
            ax[0].clear()
            ax[0].plot(elap, co2,"-r", label="CO2 ppm")
            ax[0].set(xlabel='segundos', ylabel='CO2 [ppm]')
            
            ax[1].clear()
            ax[1].plot(elap, T,"-b", label="Temperatura")
            ax[1].set(xlabel='segundos', ylabel='T [C]')

            ax[2].clear()
            ax[2].plot(elap, H, "-m", label="CO2 ppm")
            ax[2].set(xlabel='segundos', ylabel='Humedad Relativa [%]')

            #fig2.update_traces(value=co2now, selector=dict(type='indicator'))
            #pio.show(fig2)
            #plotoff(fig2)
            #st.plotly_chart(fig2) 
            
            # plt.xticks(rotation=45, ha='right')
            # plt.subplots_adjust(bottom=0.30)
            # plt.title('Serie temporal de CO2')
            # plt.ylabel('concentración de CO2 [ppm]')
            # plt.xlabel('tiempo')
            # plt.legend()
            # plt.axis([1, None, 0, 1.1]) #Use for arbitrary number of trials
            #plt.axis([1, 100, 0, 1.1]) #Use for 100 trial demo


# Set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig, animate, fargs=(fecha,elap,co2,T,H), interval=1000)
plt.show()
