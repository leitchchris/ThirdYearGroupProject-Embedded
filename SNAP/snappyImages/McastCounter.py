# Copyright (C) 2011 Synapse Wireless, Inc.
# Subject to your agreement of the disclaimer set forth below, permission is given by Synapse Wireless, Inc. ("Synapse") to you to freely modify, redistribute or include this SNAPpy code in any program. The purpose of this code is to help you understand and learn about SNAPpy by code examples.
# BY USING ALL OR ANY PORTION OF THIS SNAPPY CODE, YOU ACCEPT AND AGREE TO THE BELOW DISCLAIMER. If you do not accept or agree to the below disclaimer, then you may not use, modify, or distribute this SNAPpy code.
# THE CODE IS PROVIDED UNDER THIS LICENSE ON AN "AS IS" BASIS, WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, WITHOUT LIMITATION, WARRANTIES THAT THE COVERED CODE IS FREE OF DEFECTS, MERCHANTABLE, FIT FOR A PARTICULAR PURPOSE OR NON-INFRINGING. THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE COVERED CODE IS WITH YOU. SHOULD ANY COVERED CODE PROVE DEFECTIVE IN ANY RESPECT, YOU (NOT THE INITIAL DEVELOPER OR ANY OTHER CONTRIBUTOR) ASSUME THE COST OF ANY NECESSARY SERVICING, REPAIR OR CORRECTION. UNDER NO CIRCUMSTANCES WILL SYNAPSE BE LIABLE TO YOU, OR ANY OTHER PERSON OR ENTITY, FOR ANY LOSS OF USE, REVENUE OR PROFIT, LOST OR DAMAGED DATA, OR OTHER COMMERCIAL OR ECONOMIC LOSS OR FOR ANY DAMAGES WHATSOEVER RELATED TO YOUR USE OR RELIANCE UPON THE SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGES OR IF SUCH DAMAGES ARE FORESEEABLE. THIS DISCLAIMER OF WARRANTY AND LIABILITY CONSTITUTES AN ESSENTIAL PART OF THIS LICENSE. NO USE OF ANY COVERED CODE IS AUTHORIZED HEREUNDER EXCEPT UNDER THIS DISCLAIMER.

"""
Sample SNAPpy file for Evaluation Kit Boards (Bridge, End Device, ProtoBoard, and SNAPStick)
  Press the select-switch on any device to increment counter on all devices.
"""


# Use Synapse Evaluation Board definitions
from synapse.evalBase import *

# Comment the following out if you have your own HOOK_10MS handler
# (and be sure to call updateSevenSegmentDisplay() from your own handler)
@setHook(HOOK_10MS)
def defaultTimerHandler():
    updateSevenSegmentDisplay()

secondCounter = 0
buttonCount = 0
numPatterns = 4
curPattern = 0


@setHook(HOOK_STARTUP)
def startupEvent():
    """This is hooked into the HOOK_STARTUP event"""
    global buttonState, buttonTime

    # Detect and initialize the hardware (assumes running on an evaluation board)
    detectEvalBoards()

    # Monitor for button-press events
    monitorPin(BUTTON_PIN, True)

    # Initialize button-detect variables
    buttonState = readPin(BUTTON_PIN)
    buttonTime = getMs()

@setHook(HOOK_GPIN)
def buttonEvent(pinNum, isSet):
    """Hooked into the HOOK_GPIN event"""
    global buttonState, buttonTime, buttonCount
    if pinNum == BUTTON_PIN:
        buttonState = isSet
        if not isSet:
            buttonTime = getMs()
            incrementCount()

def incrementCount():
    """Button press action - increment and report new count"""
    global buttonCount
    buttonCount = buttonCount + 1
    buttonCount %= 100    # Wrap count at 99
    reportButtonCount()

def doEverySecond():
    """Tasks that are executed every second"""
    global curPattern, deviceType
    if platform == 'RF300' or platform == 'RF301':
        blinkLed(90)
    else:    
        blinkDurationMs = 200 + (curPattern * 200)
        if deviceType != "Stick" and deviceType != 'SS200':
            blinkLed(blinkDurationMs)

@setHook(HOOK_100MS)
def timer100msEvent(currentMs):
    """Hooked into the HOOK_100MS event"""
    global secondCounter
    global buttonState,buttonTime,buttonCount

    secondCounter += 1
    if secondCounter >= 10:
        doEverySecond()
        secondCounter = 0

    # Use a LONG (> 1 second) button press as a "counter reset"
    if buttonState == False and deviceType != "Stick":
        if buttonCount > 0:
            if currentMs - buttonTime >= 1000:
                buttonCount = 0
                reportButtonCount()

def setButtonCount(newCount):
    """Set the new button count"""
    global buttonCount
    buttonCount = newCount
    display2digits(buttonCount)
    changeLedPattern()

def reportButtonCount():
    """Report to others that button press took place"""
    global buttonCount
    mcastRpc(1,2,'setButtonCount',buttonCount)
    display2digits(buttonCount)
    changeLedPattern(buttonCount)

def changeLedPattern():
    """Change the LED display pattern after a button press"""
    global curPattern

    if deviceType == 'Bridge':
        return

    curPattern = buttonCount % numPatterns
    ledsOff()
    if curPattern == 1:
        lightLed2()
    elif curPattern == 2:
        lightLed()
    elif curPattern == 3:
        lightLed3()
