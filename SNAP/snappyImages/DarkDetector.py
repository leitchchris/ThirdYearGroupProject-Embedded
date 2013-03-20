# Copyright (C) 2011 Synapse Wireless, Inc.
# Subject to your agreement of the disclaimer set forth below, permission is given by Synapse Wireless, Inc. ("Synapse") to you to freely modify, redistribute or include this SNAPpy code in any program. The purpose of this code is to help you understand and learn about SNAPpy by code examples.
# BY USING ALL OR ANY PORTION OF THIS SNAPPY CODE, YOU ACCEPT AND AGREE TO THE BELOW DISCLAIMER. If you do not accept or agree to the below disclaimer, then you may not use, modify, or distribute this SNAPpy code.
# THE CODE IS PROVIDED UNDER THIS LICENSE ON AN "AS IS" BASIS, WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, WITHOUT LIMITATION, WARRANTIES THAT THE COVERED CODE IS FREE OF DEFECTS, MERCHANTABLE, FIT FOR A PARTICULAR PURPOSE OR NON-INFRINGING. THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE COVERED CODE IS WITH YOU. SHOULD ANY COVERED CODE PROVE DEFECTIVE IN ANY RESPECT, YOU (NOT THE INITIAL DEVELOPER OR ANY OTHER CONTRIBUTOR) ASSUME THE COST OF ANY NECESSARY SERVICING, REPAIR OR CORRECTION. UNDER NO CIRCUMSTANCES WILL SYNAPSE BE LIABLE TO YOU, OR ANY OTHER PERSON OR ENTITY, FOR ANY LOSS OF USE, REVENUE OR PROFIT, LOST OR DAMAGED DATA, OR OTHER COMMERCIAL OR ECONOMIC LOSS OR FOR ANY DAMAGES WHATSOEVER RELATED TO YOUR USE OR RELIANCE UPON THE SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGES OR IF SUCH DAMAGES ARE FORESEEABLE. THIS DISCLAIMER OF WARRANTY AND LIABILITY CONSTITUTES AN ESSENTIAL PART OF THIS LICENSE. NO USE OF ANY COVERED CODE IS AUTHORIZED HEREUNDER EXCEPT UNDER THIS DISCLAIMER.

"""
  Dark Detector Demo for EK2500

    Demonstrates two nodes cooperativly performing a task

      Uses two of the three EK2500 devices:
        * SN111 End Device Demonstration Board
            * Device Type = "Photo"
            * Has a CDS Photocell attached to the "Sensor Input"
            * Must be running this script
        * SN171 Proto Board
            * Device Type = "Buzz"
            * Has a Piezo buzzer attached to GPIO-9
            * Must be running SNAPpy script "buzzer.py"

"""

# Use Synapse Evaluation Board definitions
from synapse.evalBase import *
ADC_PHOTO = 0 # The photocell is connected to this ADC channel

@setHook(HOOK_STARTUP)
def startupEvent():
    """This is hooked into the HOOK_STARTUP event"""
    global secondCounter, buzzerAddr, photoVal, darkThreshold
    global photoMax, photoMin, requiredRange

    secondCounter = 0
    buzzerAddr = ""

    # Photocell calibration values (fullscale endpoints)
    #   Start with opposite-scale values.  Auto-calibration will push these out to observed limits.
    photoMax = 0x0000
    photoMin = 0x03FF

    darkThreshold = 85 # default to 85%, but user can change this on the fly
    requiredRange = 100 # another default that the user can change

    initDemoHw()
    findBuzzer() # try to find a node with a buzzer we can use

    photoVal = photoRead() # take an initial reading to get things started

def setThreshold(newThreshold):
    """Use this to change the 'darkness' threshold from the default of 85%"""
    global darkThreshold
    darkThreshold = newThreshold

def setRange(newRange):
    """Use this to change the default 'required light range' from the default of 100 ADC counts"""
    global requiredRange
    requiredrange = newRange

def findBuzzer():
    """try and find a buzzer to use"""
    mcastRpc(1,5,'findBuzzer')

def buzzerAt(addr):
    """a Buzzer has reported itself to us"""
    global buzzerAddr
    # remember where it is
    buzzerAddr = addr[:] # notice the use of [:] to force a persistent copy to be made

def update():
    """This is the actual 'Dark Detection'"""
    global photoMax, photoMin, photoVal, darkThreshold

    # If we have not yet found a companion buzzer, look again
    if buzzerAddr == "":
        findBuzzer()

    newValue = photoRead()

    display2digits(newValue)

    if buzzerAddr != "": # if we know where a buzzer is
        if newValue >= darkThreshold: # if it's dark this time
            if photoVal < darkThreshold: # and it was not dark last time
                rpc(buzzerAddr, 'buzzer', 100) # then beep to report the new darkness

    # remember the value for next time
    photoVal = newValue

def photoRead():
    """Get darkness value from photocell reading, scaled 0-99"""
    global photoMax, photoMin, requiredRange

    # Sample the photocell (connected to ADC channel 0)
    curReading = readAdc(ADC_PHOTO)

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

@setHook(HOOK_100MS)
def poll100ms(msTick):
    global secondCounter
    
    secondCounter += 1
    if secondCounter >= 3:
        secondCounter = 0
        if platform == 'RF300' or platform == 'RF301':
            update()
            blinkLed(50)
        else:
            blinkLed(200)
    
    if not (platform == 'RF300' or platform == 'RF301'):
        update()
    
# Comment the following out if you have your own HOOK_10MS handler
# (and be sure to call updateSevenSegmentDisplay() from your own handler)
if platform == 'RF300' or platform == 'RF301':
    @setHook(HOOK_10MS)
    def defaultTimerHandler():
        updateSevenSegmentDisplay()

