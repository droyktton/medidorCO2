#!/usr/bin/env python
# coding: utf-8

## lee el puerto serial que escribe el medidor
## e imprime co2, T, H en un file "medidor.dat"

import os, sys
import matplotlib
from matplotlib import cm
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import numpy as np
import random
import serial
import time
import datetime
from matplotlib.patches import Circle, Wedge, Rectangle

def degree_range(n): 
    start = np.linspace(0,180,n+1, endpoint=True)[0:-1]
    end = np.linspace(0,180,n+1, endpoint=True)[1::]
    mid_points = start + ((end-start)/2.)
    return np.c_[start, end], mid_points

def rot_text(ang): 
    rotation = np.degrees(np.radians(ang) * np.pi / np.pi - np.radians(90))
    return rotation

def gauge(N=5, labels=['LOW','MEDIUM','HIGH','VERY HIGH','EXTREME'], colors='inferno', cat=1, title='', fname='./meter.png',co2now=400):     
    
    """
    some sanity checks first
    """
    
    if len(labels) != N: 
        print("number of labels not equal to number of categories\n")
    
    """
    if colors is a string, we assume it's a matplotlib colormap
    and we discretize
    """
    
    if isinstance(colors, str):
        cmap = cm.get_cmap(colors, N)
        cmap = cmap(N-np.arange(N))
        colors = cmap[::-1,:].tolist()
    if isinstance(colors, list): 
        if len(colors) == N:
            colors = colors[::-1]
        else: 
            print("number of colors not equal to number of categories\n")

    """
    begins the plotting
    """
    #fig, ax = plt.subplots()

    ang_range, mid_points = degree_range(N)

    labels = labels[::-1]
    
    """
    plots the sectors and the arcs
    """
    patches = []
    for ang, c in zip(ang_range, colors): 
        # sectors
        patches.append(Wedge((0.,0.), .4, *ang, facecolor='w', lw=2))
        # arcs
        patches.append(Wedge((0.,0.), .4, *ang, width=0.10, facecolor=c, lw=2, alpha=0.5))
    
    [ax.add_patch(p) for p in patches]

    """
    set the labels (e.g. 'LOW','MEDIUM',...)
    """

    for mid, lab in zip(mid_points, labels): 

        ax.text(0.35 * np.cos(np.radians(mid)), 0.35 * np.sin(np.radians(mid)), lab, \
            horizontalalignment='center', verticalalignment='center', fontsize=16, \
            fontweight='bold', rotation = rot_text(mid))

    """
    set the bottom banner and the title
    """
    r = Rectangle((-0.4,-0.1),0.8,0.1, facecolor='w', lw=2)
    ax.add_patch(r)
    
    ax.text(0, -0.075, title, horizontalalignment='center', \
         verticalalignment='center', fontsize=26, fontweight='bold')

    """
    plots the arrow now
    """
    
    pos = mid_points[abs(cat - N)]
    ang = np.pi-(co2now-400.0)*np.pi/(1200.0)
    
    ax.arrow(0, 0, 0.225 * np.cos(ang), 0.225 * np.sin(ang), \
                 width=0.04, head_width=0.09, head_length=0.1, fc='k', ec='k')
    
    ax.add_patch(Circle((0, 0), radius=0.02, facecolor='k'))
    ax.add_patch(Circle((0, 0), radius=0.01, facecolor='w', zorder=11))

    """
    removes frame and ticks, and makes axis equal and tight
    """
    
    ax.set_frame_on(False)
    ax.axes.set_xticks([])
    ax.axes.set_yticks([])
    ax.axis('equal')


#initialize serial port
ser = serial.Serial()
ser.port = '/dev/ttyACM0' #Arduino serial port
ser.baudrate = 9600
ser.timeout = 10 #specify timeout when using readline()
ser.open()
if ser.is_open==True:
	print("\nAll right, serial port now open. Configuration:\n")
	print(ser, "\n") #print serial parameters

co2=[]
T=[]
H=[]
elap=[]
fecha=[]
co2now=400

fig, ax = plt.subplots()
gauge(N=5, labels=['Bajo','Medio','Ventilar','Ventilar!','Ventilar!!'], colors='rainbow', 
                cat=1, title="CO2 ppm", fname='./gauge.png',co2now=co2now)

plt.tight_layout()
fig.show()


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
            if(co2now<=600):
                cat=0
            if(co2now>600 and co2now<=800):
                cat=1
            if(co2now>800 and co2now<=1000):
                cat=2
            if(co2now>1000 and co2now<=1200):
                cat=3
            if(co2now>1200 and co2now<=1600):
                cat=4
                
            print(co2now,cat)
            titulo=str(co2now)+" ppm de CO2"
            #if(cat>1):
            #    titulo=titulo+"\n VENTILAR"
            ax.clear()
            gauge(N=5, labels=['Bajo','Medio','Ventilar','Ventilar!','Ventilar!!'], colors='rainbow', 
                cat=cat, title=titulo, fname='./gauge.png',co2now=co2now)


# Set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig, animate, fargs=(fecha,elap,co2,T,H), interval=1000)
plt.show()
