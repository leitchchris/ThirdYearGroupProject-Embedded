# Copyright (C) 2011 Synapse Wireless, Inc.
# Subject to your agreement of the disclaimer set forth below, permission is given by Synapse Wireless, Inc. ("Synapse") to you to freely modify, redistribute or include this SNAPpy code in any program. The purpose of this code is to help you understand and learn about SNAPpy by code examples.
# BY USING ALL OR ANY PORTION OF THIS SNAPPY CODE, YOU ACCEPT AND AGREE TO THE BELOW DISCLAIMER. If you do not accept or agree to the below disclaimer, then you may not use, modify, or distribute this SNAPpy code.
# THE CODE IS PROVIDED UNDER THIS LICENSE ON AN "AS IS" BASIS, WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, WITHOUT LIMITATION, WARRANTIES THAT THE COVERED CODE IS FREE OF DEFECTS, MERCHANTABLE, FIT FOR A PARTICULAR PURPOSE OR NON-INFRINGING. THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE COVERED CODE IS WITH YOU. SHOULD ANY COVERED CODE PROVE DEFECTIVE IN ANY RESPECT, YOU (NOT THE INITIAL DEVELOPER OR ANY OTHER CONTRIBUTOR) ASSUME THE COST OF ANY NECESSARY SERVICING, REPAIR OR CORRECTION. UNDER NO CIRCUMSTANCES WILL SYNAPSE BE LIABLE TO YOU, OR ANY OTHER PERSON OR ENTITY, FOR ANY LOSS OF USE, REVENUE OR PROFIT, LOST OR DAMAGED DATA, OR OTHER COMMERCIAL OR ECONOMIC LOSS OR FOR ANY DAMAGES WHATSOEVER RELATED TO YOUR USE OR RELIANCE UPON THE SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGES OR IF SUCH DAMAGES ARE FORESEEABLE. THIS DISCLAIMER OF WARRANTY AND LIABILITY CONSTITUTES AN ESSENTIAL PART OF THIS LICENSE. NO USE OF ANY COVERED CODE IS AUTHORIZED HEREUNDER EXCEPT UNDER THIS DISCLAIMER.


'''-----Freescale Tower board example script using SM700/TWR_SNAP module-----
Lab 2 - Sensors
The RED LED will come on once the temperature sensor detects a value higher than the 
configured threshold. The user can adjust this level up and down using the buttons on 
the board.  
The GREEN LED will come on if the photocell detects a light level below its configured 
threshold. 
The user can change the low light threshold by calling a function over the air. 

Actions:
    Press SW3 - Increases the temperature threshold
    Press SW2 - decreases the temperature threshold    
    setLightThreshold(newThreshold) - sets a new light threshold
'''
from synapse.platforms import *

if platform != "SM700":
    compileError #script only valid on SM700
    
#---Pin Definitions - mapping IO to the SM700 functionality---
TMR0_GP8 = 8
TMR1_GP9 = 9
KBI0_GP22 = 22
KBI1_GP23 = 23

RED_LED = TMR0_GP8
GRN_LED = TMR1_GP9

SW2 = KBI0_GP22
SW3 = KBI1_GP23

PHOTO_ADC = 0
TEMP_ADC  = 1

#--- Constants and Global Variables ---
MAX_PHOTO = 4095
MIN_PHOTO = 0
curTempThres = 25   # Default threshold of 25 C
curLightThres = 50  # Default threshold of 50% 

@setHook(HOOK_STARTUP)
def init():
    '''Start-up event'''
    # Configure LED pins
    setPinDir(RED_LED, True)
    setPinDir(GRN_LED, True)
    # Pulse the LEDs once during start-up
    pulsePin(RED_LED, 80, True)
    pulsePin(GRN_LED, 80, True)

    #Configure switch pins - monitor for button press
    setPinDir(SW2, False)
    setPinPullup(SW2, True)
    monitorPin(SW2, True)
    
    setPinDir(SW3, False)
    setPinPullup(SW3, True)
    monitorPin(SW3, True)
    
def getTempThreshold():
    '''Return the current temperature threshold'''
    return curTempThres

def getLightThreshold():
    '''Return the current light threshold (between 1 and 100%)'''
    return curLightThres

def getCurTempVal():
    '''Return the current temperature reading in degree C'''
    return readTemperatureC()

def getCurLightVal():
    '''Return the current light reading (raw ADC value) '''
    return readPhotocell()

def setTempThreshold(newThreshold):
    '''Set the temperature threshold'''
    global curTempThres
    curTempThres = newThreshold
        
def setLightThreshold(newThreshold):
    '''Set the light threshold (between 1 and 100%)'''
    global curLightThres
    if 100 > newThreshold > 0:
        curLightThres =  newThreshold
    else:
        print "error - invalid threshold" #For DEBUG
        
def incTempThreshold():
    '''Increment the temperature threshold'''
    global curTempThres
    curTempThres += 1  # Increment by 1 degree C

def decTempThreshold():
    '''Decrement the temperature threshold'''
    global curTempThres
    curTempThres -= 1 #  Decrement by 1 degree C
    
def convertToRange(percent):
    '''Convert a percent value to a value between 0-4095 (expected LED range).
       Formula: conversion = (percent*maxValue)/100 '''
    if percent >= 100:
        percent = 100
    if percent < 0:
        percent = 0
       
    # Use approx of maxValue and scale by a factor to avoid overflow of signed 16 bit Integer
    conv = percent * (4100/100) # Use approx of 4100 for 4095
    if conv > 4095:
        conv = 4095
    return conv
    
def selectAdc1(chan):
    '''Select ADC1 2.5v precision reference'''
    readAdc(0)                              # Init ADC
    # poke into underlying hardware registers to select the correct reference
    poke(0x8000, 0xD018, 1, 0x0031)         # Control ON
    poke(0x8000, 0xD044, 1, 0x0001)         # Enable override
    poke(0x8000, 0xD040, 1, 0x0100 | chan)  # Select ADC1
    
#-------------------------------- Sensor Readings --------------------------------   
def readTemperatureC():
    '''Read the temperature sensor and return degrees C.  
       1C per 10 mV, with zero offset of 500mV
       Take care to keep all values within 16-bit signed integer range.
    '''
    selectAdc1(TEMP_ADC)
    
    raw = 0
    i = 25    # Averaging, and multiplier corresponding to 2.5v reference
    while i > 0:
        i -= 1
        raw += (readAdc(TEMP_ADC) >> 2)  # Use 10-bits of sample for averaging (25*1024=25k max)
    
    raw >>= 3  # Reduce to 7-bits: max of 25*128=3200
    tempC = ((raw * 10) / 128) - 50
    return tempC

def readPhotocell():
    '''Return raw 12-bit ADC value (0-4095) for photocell'''
    selectAdc1(PHOTO_ADC)
    
    raw = 0
    i = 8
    while i > 0:
        i -= 1
        raw += (readAdc(PHOTO_ADC))

    return raw / 8
    
#-------------------------------- Event Handlers --------------------------------
@setHook(HOOK_GPIN)
def buttonPress(pin, isSet):
    '''Pin transition event handler (button press)'''
    
    print "Button Press ", pin, "=", isSet # For Debug
    
    if pin == SW2 and not isSet:
        decTempThreshold()
        print "New Temp Threshold: ", curTempThres
    elif pin == SW3 and not isSet:
        incTempThreshold()
        print "New Temp Threshold: ", curTempThres
        
@setHook(HOOK_100MS)
def tick():
    '''Timer tick event handler (100MS)'''
    tempr = readTemperatureC()
    #print "tempr= ",tempr," ",curTempThres  #For DEBUG
    if tempr > curTempThres:
        writePin(RED_LED, True)
        #Inform any other devices of the condition
        mcastRpc(1,1,"pulseRedLed", 200)
    else:
        writePin(RED_LED, False)
                
    rawLight = readPhotocell()
    rawLightThres = convertToRange(curLightThres)
    #print "light= ",rawLight," ",rawLightThres #For DEBUG
    if rawLight > rawLightThres:
        writePin(GRN_LED, True)
        #Inform any other devices of the condition
        mcastRpc(1,1,"pulseGreenLed", 200)
    else:
        writePin(GRN_LED, False)

