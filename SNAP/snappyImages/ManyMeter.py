# Copyright (C) 2011 Synapse Wireless, Inc.
# Subject to your agreement of the disclaimer set forth below, permission is given by Synapse Wireless, Inc. ("Synapse") to you to freely modify, redistribute or include this SNAPpy code in any program. The purpose of this code is to help you understand and learn about SNAPpy by code examples.
# BY USING ALL OR ANY PORTION OF THIS SNAPPY CODE, YOU ACCEPT AND AGREE TO THE BELOW DISCLAIMER. If you do not accept or agree to the below disclaimer, then you may not use, modify, or distribute this SNAPpy code.
# THE CODE IS PROVIDED UNDER THIS LICENSE ON AN "AS IS" BASIS, WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, WITHOUT LIMITATION, WARRANTIES THAT THE COVERED CODE IS FREE OF DEFECTS, MERCHANTABLE, FIT FOR A PARTICULAR PURPOSE OR NON-INFRINGING. THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE COVERED CODE IS WITH YOU. SHOULD ANY COVERED CODE PROVE DEFECTIVE IN ANY RESPECT, YOU (NOT THE INITIAL DEVELOPER OR ANY OTHER CONTRIBUTOR) ASSUME THE COST OF ANY NECESSARY SERVICING, REPAIR OR CORRECTION. UNDER NO CIRCUMSTANCES WILL SYNAPSE BE LIABLE TO YOU, OR ANY OTHER PERSON OR ENTITY, FOR ANY LOSS OF USE, REVENUE OR PROFIT, LOST OR DAMAGED DATA, OR OTHER COMMERCIAL OR ECONOMIC LOSS OR FOR ANY DAMAGES WHATSOEVER RELATED TO YOUR USE OR RELIANCE UPON THE SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGES OR IF SUCH DAMAGES ARE FORESEEABLE. THIS DISCLAIMER OF WARRANTY AND LIABILITY CONSTITUTES AN ESSENTIAL PART OF THIS LICENSE. NO USE OF ANY COVERED CODE IS AUTHORIZED HEREUNDER EXCEPT UNDER THIS DISCLAIMER.

"""

  Many Meter Demo for EK2100 Kit (for use on Proto-Board)

    This Snappy script demonstrates how information can be gathered on a SNAP node 
    sent back to Portal for display, tracking, or processing.
    
    To be run on the Proto-Board only
    
    Requires: Photo Cell (with Pull-up resistor)
              Thermistor (with Pull-up resistor)
             

"""
# Use Synapse Evaluation Board definitions
from synapse.evalBase import *
from synapse.nvparams import *

portalAddr = '\x00\x00\x01' # hard-coded address for Portal
PHOTO_PIN = GPIO_12

@setHook(HOOK_STARTUP)
def startupEvent():
    """This is hooked into the HOOK_STARTUP event"""  
    global secondCounter, photoVal, photoMax, photoMin, requiredRange
    global curMeterType, numOfRpc
    
    curMeterType = "photo"
    numOfRpc = 0 # Number of RPCs that will be sent
    secondCounter = 0 # Used by the system for one second count

    initProtoHw() # Intialize the proto board  

    # Setup photo cell power
    setPinDir(PHOTO_PIN, True) 
    writePin(PHOTO_PIN, True) # Power the pin for the Photocell

    monitorPin(BUTTON_PIN, True) # Monitor for button press

    # Photocell calibration values (fullscale endpoints)
    # Start with opposite-scale values.  Auto-calibration will push these out to observed limits.
    photoMax = 0x0000
    photoMin = 0x03FF
    requiredRange = 100

    photoVal = photoRead() # Take an initial reading to get things started

def doEverySecond():
    """Things to be done every second"""
    global numOfRpc
    blinkLed(200)  
    if curMeterType == "photo":
        updatePhoto()
        numOfRpc = 2
    if curMeterType == "LQ":
        updateLinkQuality()        
        numOfRpc = 2 
    if curMeterType == "temp":
        updateTempSensor()
        numOfRpc = 2 
    if curMeterType == "group":
        updatePhoto()        
        numOfRpc = 4  

@setHook(HOOK_RPC_SENT)
def rpcSentEvent():
    """This is hooked into the HOOK_RPC_SENT event that is called after every RPC"""  
    global curMeterType, numOfRpc
    
    if numOfRpc == 0:
        return
        
    if curMeterType == "photo":
        if numOfRpc == 2:
            numOfRpc -= 1
            graphPhoto()
        elif numOfRpc == 1:
            numOfRpc -= 1
            popupPhoto()
    
    if curMeterType == "LQ":
        if numOfRpc == 2:
            numOfRpc -= 1
            graphLq()
        elif numOfRpc == 1:
            numOfRpc -= 1
            popupLq()
    
    if curMeterType == "temp" :
        if numOfRpc == 2:
            numOfRpc -= 1
            graphTemp()
        elif numOfRpc == 1:
            numOfRpc -= 1
            popupTemp()    
   
   # Graph the photo and temperature readings at the same time 
    if curMeterType == "group": 
        if numOfRpc == 4:
            updateTempSensor()
            numOfRpc -= 1
        elif numOfRpc == 3:
            numOfRpc -= 1
            graphPhoto()
        elif numOfRpc == 2:
            numOfRpc -= 1
            graphTemp()
        elif numOfRpc == 1:
            numOfRpc -= 1
            popupTemp()

@setHook(HOOK_100MS)
def timer100msEvent(currentMs):
    """Hooked into the HOOK_100MS event. Called every 100ms"""
    global secondCounter, lqSum  
    secondCounter += 1
    lqSum += getPercentLq() # get the link Quality every 100ms
    if secondCounter >= 10:
        doEverySecond()
        secondCounter = 0
        lqSum = 0 # reset the link quality sum after updating

@setHook(HOOK_GPIN)
def buttonEvent(pinNum, isSet):
    """Action taken when the on-board buttton is pressed (i.e. change meter)"""  
    if pinNum == BUTTON_PIN and isSet:
        changeMeterType()

def updatePhoto():
    """This will gather the info from the sensor and display it"""
    global photoMax, photoMin, photoVal

    photoVal = photoRead()

    # Send the data to the Portal node
    eventString = "The current light reading is " + str(photoVal)
    rpc(portalAddr, "logEvent", eventString)
    
def photoRead():
    """Get darkness value from photocell reading, scaled 0-99"""
    global photoMax, photoMin, requiredRange

    # Sample the photocell
    curReading = readAdc(7) # connected to GPIO11

    # Auto-Calibrate min/max photocell readings
    if photoMax < curReading:
        photoMax = curReading
    if photoMin > curReading:
        photoMin = curReading

    if photoMax <= photoMin:
        return 0

    photoRange = photoMax - photoMin
    if photoRange < requiredRange: # if not yet calibrated
        return 0

    # Remove zero-offset to get value in range 0-1023 (10-bit ADC)
    curReading -= photoMin

    # Scale 0-100, careful not to exceed 16-bit integer positive range (32768)
    curReading = (curReading * 10) / (photoRange / 10)

    # Return value scaled 0-99
    return (curReading * 99) / 100

def graphPhoto():
    """This will display the reading in the data logger"""
    global photoVal
    # Get from the name from NVParams every time you update- in case the name has changed
    deviceName = "DRK_" + loadNvParam(NV_DEVICE_NAME_ID)
    rpc(portalAddr, "logData", deviceName, photoVal, 100)
    
def popupPhoto():
    """This will display the reading in a new window (when used with portalManyMeter Portal script)"""
    global photoVal
    # EDIT NEXT LINE: This is special code to call into the wxPython functionality of Portal  
    #rpc(portalAddr,"DisplayData",photoVal,"Dark Meter",loadNvParam(NV_DEVICE_NAME_ID)) 
    return
        
def updateLinkQuality():
    """Send the current link quality back to Portal for logging"""
    global lqSum, theLqAvg, secondCounter    

    theLqAvg = (lqSum / secondCounter) # calc the avg to send

    # Send the data to the Portal node
    eventString = "The link quality reading is " + str(theLqAvg)
    rpc(portalAddr, "logEvent", eventString) 

def graphLq():
    """This will display the reading in the data logger"""
    global theLqAvg
    # Get from the name from NVParams every time you update- in case the name has changed
    deviceName = "LQ_" + loadNvParam(NV_DEVICE_NAME_ID) 
    rpc(portalAddr, "logData", deviceName, theLqAvg, 100)
    
def popupLq():
    """This will display the reading in a new window (when used with portalManyMeter Portal script)"""
    global theLqAvg
    # EDIT NEXT LINE: This is special code to call into the wxPython functionality of Portal
    #rpc(portalAddr,"DisplayData",theLqAvg,"Link Quality Meter",loadNvParam(NV_DEVICE_NAME_ID))
    return
 
def updateTempSensor():
    """Send the current temperature back to Portal for logging"""
    global curRawTemp  

    curRawTemp = tempRead() # Read the current value

    # Send the data to the Portal node
    eventString = "The raw thermistor reading is " + str(curRawTemp)
    rpc(portalAddr, "logEvent", eventString) 

def tempRead():
    """Read the current temperature from the sensor"""
    # For this simple example we will not calculate the actual temperature in degrees 
    return readAdc(0) # Read Adc on GPIO 18

def graphTemp():
    """This will display the reading in the data logger"""
    global curRawTemp
    # Get from the name from NVParams every time you update- in case the name has changed
    deviceName = "TMP_" + loadNvParam(NV_DEVICE_NAME_ID)
    rpc(portalAddr, "logData", deviceName, curRawTemp/10, 100)

def popupTemp():
    """This will display the reading in a new window (when used with portalManyMeter Portal script)"""
    # EDIT NEXT LINE:  This is special code to call into the wxPython functionality of Portal  
    #rpc(portalAddr,"DisplayData",curRawTemp/10,"Raw Thermistor Reading",loadNvParam(NV_DEVICE_NAME_ID))
    return

def getPercentLq():
    """Calculate the Link Quality as a percentage"""
    maxDbm = 18
    minDbm = 95
    # Use the built-in function to get the current LQ reading
    percent = 100 - ((getLq() - maxDbm) * 100) / (minDbm - maxDbm)
    return percent

def changeMeterType():
    """Change the type of meter you are running (light or link quality or temperature)"""
    global curMeterType 
    if curMeterType == "photo":
        curMeterType = "temp"
    elif curMeterType == "temp":
        curMeterType = "LQ"
    elif curMeterType == "LQ":
        curMeterType = "group"
    elif curMeterType == "group":
        curMeterType = "none"
    elif curMeterType == "none":
        curMeterType = "photo"

