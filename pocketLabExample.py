# -*- coding: utf-8 -*-
"""
Created on Tue Apr 20 16:57:05 2021

@author: Sean Ward
"""

# %% Liraries are imported to be used

import numpy as np #Great library for arrays. Many predefined functions
import math as mt #Helpful library for math functions
import pandas as pd #Useful library for reading and writing to csv, and working with excel
import matplotlib.pyplot as plt #Most widely used plotting library, creating figures

# %% Functions are defined

#Function reads in data in the form of a data frame. Parses this data frame into variable arrays that we can work with easier
def parseData(data): #Item in quotes defines the input of the function
    
    #np.array() converted the series data (from data frame) to an array
    time = np.array(data.Time)
    xAcc = np.array(data.X_Acc)
    yAcc = np.array(data.Y_Acc)
    zAcc = np.array(data.Z_Acc)
    press = np.array(data.Pressure_mBar)
    altData = np.array(data.Altitude_ft)
    xAng = np.array(data.Ang_Vel_X)
    yAng = np.array(data.Ang_Vel_Y)
    zAng = np.array(data.Ang_Vel_Z)
    temp = np.array(data.Temp)
    
    return(time, xAcc, yAcc, zAcc, xAng, yAng, zAng, press, altData, temp) #return defines what we output from the function, in this case our numpy arrays

#Function to convert the barometric pressure readings to altitude (ft) 
def press2Alt(press,bias): #Input the pressure reading, and any bias (identified by doing a calibration step - take reading with bias=0, plot results, subtract bias)
    
    #Constants used for unit conversion and atmospheric pressure at sea level
    m2ft = 3.28084
    po = 1013.25
    
    #Create an array of the same size as the pressure readings to be filled
    altCalc = np.zeros(len(press))
    
    #Loop through entire length of pressure readings, calculating the corresponding altitide
    for i in range(len(press)):
        altCalc[i] = ((((((po/press[i])**(1/5.5257))-1)*temp[i])/.0065)*m2ft)-bias
    
    return altCalc #Output altitude in feet array (MSL) would need to subtract reading at ground to get altitude Above Ground Level

#Function to calculate numerical derivative given an array and a time step
def deriv(array, dt):
    darray = np.zeros(len(array))
    for i in range(1,len(array)):
        darray[i]= (array[i]-array[i-1])/dt
    darray[0] = darray[1]
    return darray

#Function to calculate a numerical integral using the trapezoidal rule
def trap(array, dt):
    intArray = np.zeros(len(array))
    for i in range(1,len(array)):
        intArray[i] = intArray[i-1] + 0.5*(array[i-1]+array[i])*dt
    return intArray


# %% MAIN PROGRAM

# Define directory where the data lives
location = r'C:\Users\Sean\Box\EXPLO\Sean Ward\pocketLabTest.csv'
data = pd.read_csv(location) #read in csv

#Parse data to arrays
time, xAcc, yAcc, zAcc, xAng, yAng, zAng, press, altData, temp = parseData(data)

# Define constants
dt = 0.1
bias = -15.71


altCalc = press2Alt(press,bias) #Calculate altitude based on barometric pressure
velAltDeriv = deriv(altCalc,dt) #Calculate vertical velocity by taking derivative of height
accAlt = deriv(velAltDeriv,dt) #Calculate vertical acceleration by taking derivative of velocity

velAltInt = trap(zAcc, dt) #Integrate accelerometer data for velocity
altInt = trap(velAltInt, dt)+altData[0] #Integrate velocity data for height

plt.figure(1) #Start a Figure 1
plt.title('Effect of Derivative on Acceleration Estimate') #Define title
plt.plot(time, accAlt, label='Derivative') #Plot data, include label for use in legend
plt.plot(time, zAcc, label='Measured') #Plot data, include label for use in legend
plt.legend() #Show legend

plt.figure(2)
plt.title('Effect of Integral on Altitude Estimate')
plt.plot(time, altInt, label='Integrated')
plt.plot(time, altCalc, label='Measured')
plt.legend()

plt.figure(3)
plt.title('Velocity Estimation')
plt.plot(time, velAltDeriv, label='Derivative')
plt.plot(time, velAltInt, label='Integral')
plt.legend()

plt.figure(4)
plt.title('Altitude')
plt.plot(time, altCalc, label='Pressure Calculated')
plt.plot(time, altData, label='Measured')
plt.legend()