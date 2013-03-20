# Copyright (C) 2011 Synapse Wireless, Inc.
# Subject to your agreement of the disclaimer set forth below, permission is given by Synapse Wireless, Inc. ("Synapse") to you to freely modify, redistribute or include this SNAPpy code in any program. The purpose of this code is to help you understand and learn about SNAPpy by code examples.
# BY USING ALL OR ANY PORTION OF THIS SNAPPY CODE, YOU ACCEPT AND AGREE TO THE BELOW DISCLAIMER. If you do not accept or agree to the below disclaimer, then you may not use, modify, or distribute this SNAPpy code.
# THE CODE IS PROVIDED UNDER THIS LICENSE ON AN "AS IS" BASIS, WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, WITHOUT LIMITATION, WARRANTIES THAT THE COVERED CODE IS FREE OF DEFECTS, MERCHANTABLE, FIT FOR A PARTICULAR PURPOSE OR NON-INFRINGING. THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE COVERED CODE IS WITH YOU. SHOULD ANY COVERED CODE PROVE DEFECTIVE IN ANY RESPECT, YOU (NOT THE INITIAL DEVELOPER OR ANY OTHER CONTRIBUTOR) ASSUME THE COST OF ANY NECESSARY SERVICING, REPAIR OR CORRECTION. UNDER NO CIRCUMSTANCES WILL SYNAPSE BE LIABLE TO YOU, OR ANY OTHER PERSON OR ENTITY, FOR ANY LOSS OF USE, REVENUE OR PROFIT, LOST OR DAMAGED DATA, OR OTHER COMMERCIAL OR ECONOMIC LOSS OR FOR ANY DAMAGES WHATSOEVER RELATED TO YOUR USE OR RELIANCE UPON THE SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGES OR IF SUCH DAMAGES ARE FORESEEABLE. THIS DISCLAIMER OF WARRANTY AND LIABILITY CONSTITUTES AN ESSENTIAL PART OF THIS LICENSE. NO USE OF ANY COVERED CODE IS AUTHORIZED HEREUNDER EXCEPT UNDER THIS DISCLAIMER.

"""
  Holiday Light Show Demo for EK2100 Kit (for use on Proto-Board)

    This Snappy script demonstrates how information gathered from 
    sensors onboard a SNAP node can be communicated to other 
    nodes and used to initiate other tasks.
    
    To be run on the Proto-Board only
    
    Requires: Photo Cell
              Pull-up resistor
              3 LEDs
    
"""

# Use Synapse Evaluation Board definitions
from synapse.evalBase import *

# Globals
secondCounter = 0
reachedThresholdOnce = False
doChristmasPulse = False # Do not strobe the LEDs by default
doHalloweenPulse = False
darkThreshold = 85 # default to 85%, but user can change this on the fly
requiredRange = 100 # another default
# Photocell calibration values (fullscale endpoints)
# Start with opposite-scale values.  Auto-calibration will push these out to observed limits.
photoMax = 0x0000
photoMin = 0x03FF

# Pin Definitions
buttonPin = GPIO_5 # The built-in button is configured for GPIO 5
orangeLEDPin = GPIO_0
orangeLEDPinGND = GPIO_3
redLEDPin = GPIO_4
redLEDPinGND = GPIO_6 
greenLEDPin = GPIO_7
greenLEDPinGND = GPIO_8 
photoCellPin = GPIO_12


@setHook(HOOK_STARTUP)
def startupEvent():
    """This is hooked into the HOOK_STARTUP event"""
    global photoVal

    initProtoHw() # intialize the proto board  
    initLEDPins() # setup the GPIO pins for each LED
      
    monitorPin(buttonPin, True) # Monitor the button
     
    # Setup photo cell power
    setPinDir(photoCellPin,True) 
    writePin(photoCellPin, True) # Set the pin high to power the device
      

      
    photoVal = photoRead() # take an initial reading to get things started

def initLEDPins():
    """ Setup each of the pins used by the connected LEDs """  
     # set the associated pins to be 'outputs'
    setPinDir(redLEDPin,True) 
    setPinDir(redLEDPinGND,True)
    setPinDir(orangeLEDPin,True)
    setPinDir(orangeLEDPinGND,True)  
    setPinDir(greenLEDPin,True) 
    setPinDir(greenLEDPinGND,True) 
  
    # Set each pin to a low value
    writePin(redLEDPin, False) 
    writePin(redLEDPinGND, False) 
    writePin(orangeLEDPin, False) 
    writePin(orangeLEDPinGND, False) 
    writePin(greenLEDPin, False) 
    writePin(greenLEDPinGND, False) 
  
def doEverySecond():
    """Things to be done every second""" 
    blinkLed(200)
    if doChristmasPulse:
        pulsePin(redLEDPin, 800, True) 
        pulsePin(greenLEDPin, 400, True)
        pulsePin(1, 200, True)
    if doHalloweenPulse:
        pulsePin(redLEDPin, 400, True)      
        pulsePin(orangeLEDPin, 800, True) 

@setHook(HOOK_100MS)
def timer100msEvent(currentMs):
    """Hooked into the HOOK_100MS event. Called every 100ms"""
    global secondCounter
    secondCounter += 1
    updatePhoto()
    if secondCounter >= 10:
        doEverySecond()
        secondCounter = 0

@setHook(HOOK_GPIN)
def buttonEvent(pinNum, isSet):
    """Action taken when the on-board buttton is pressed (i.e. turn lights off)"""  
    lightsOff()
    
def setThreshold(newThreshold):
    """Use this to change the 'darkness' threshold from the default of 85%"""
    global darkThreshold
    darkThreshold = newThreshold

def updatePhoto():
    """Update by taking a photo cell reading"""
    global photoVal, reachedThresholdOnce
       
    newValue = photoRead()
  
    # if it is dark this time and was not last time
    if (newValue >= darkThreshold) and (photoVal < darkThreshold): 
        if reachedThresholdOnce:
            changeSeason()
        else:
            startChristmasDisplay()
            reachedThresholdOnce = True

    # remember the value for next time
    photoVal = newValue

def photoRead():
    """Get darkness value from photo cell reading, scaled 0-99"""
    global photoMax, photoMin

    # Sample the photocell (connected to ADC channel 0)
    curReading = readAdc(7) # connected to GPIO11
    
    # Auto-Calibrate min/max photocell readings
    if photoMax < curReading:
        photoMax = curReading
    if photoMin > curReading:
        photoMin = curReading

    #print 'min=',photoMin,' cur=',curReading,' max=',photoMax

    if photoMax <= photoMin:
        return 0

    photoRange = photoMax - photoMin
    if photoRange < requiredRange: # if not yet calibrated
        return 0

    # Remove zero-offset to get value in range 0-1024 (10-bit ADC)
    curReading -= photoMin

    # Scale 0-100, careful not to exceed 16-bit integer positive range (32768)
    curReading = (curReading * 10) / (photoRange / 10)

    # Return value scaled 0-99
    return (curReading * 99) / 100

def startChristmasDisplay():
    """Pulse the red and green LEDS""" 
    global doChristmasPulse
    doChristmasPulse = True
    # Now tell anyone else out there it's Christmas time    
    print "calling Christmas RPC!"    
    mcastRpc(1,2,"christmasBlink")
   
def startHalloweenDisplay():
    """Pulse the red and orange LEDS"""   
    global doHalloweenPulse
    doHalloweenPulse = True
    # Now tell anyone else out there it's halloween time
    print "calling halloween RPC!"
    mcastRpc(1,2,"halloweenBlink") 

def endChristmasDisplay():
    """Turn off the red and green LEDS""" 
    global doChristmasPulse
    doChristmasPulse = False  

def endHalloweenDisplay():
    """Turn off the red and orange LEDS"""   
    global doHalloweenPulse
    doHalloweenPulse = False
   
def changeSeason():
    """Change the light configuration"""
    if doChristmasPulse:
        endChristmasDisplay()
        startHalloweenDisplay()
    elif doHalloweenPulse:
        endHalloweenDisplay()
        startChristmasDisplay()

def lightsOff():
    """Disable the LEDs and inform other nodes"""
    global reachedThresholdOnce
    endChristmasDisplay()
    endHalloweenDisplay()
    reachedThresholdOnce = False
    mcastRpc(1,2, "disableLEDs")
