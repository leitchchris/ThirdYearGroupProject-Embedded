# Copyright (C) 2011 Synapse Wireless, Inc.
# Subject to your agreement of the disclaimer set forth below, permission is given by Synapse Wireless, Inc. ("Synapse") to you to freely modify, redistribute or include this SNAPpy code in any program. The purpose of this code is to help you understand and learn about SNAPpy by code examples.
# BY USING ALL OR ANY PORTION OF THIS SNAPPY CODE, YOU ACCEPT AND AGREE TO THE BELOW DISCLAIMER. If you do not accept or agree to the below disclaimer, then you may not use, modify, or distribute this SNAPpy code.
# THE CODE IS PROVIDED UNDER THIS LICENSE ON AN "AS IS" BASIS, WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, WITHOUT LIMITATION, WARRANTIES THAT THE COVERED CODE IS FREE OF DEFECTS, MERCHANTABLE, FIT FOR A PARTICULAR PURPOSE OR NON-INFRINGING. THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE COVERED CODE IS WITH YOU. SHOULD ANY COVERED CODE PROVE DEFECTIVE IN ANY RESPECT, YOU (NOT THE INITIAL DEVELOPER OR ANY OTHER CONTRIBUTOR) ASSUME THE COST OF ANY NECESSARY SERVICING, REPAIR OR CORRECTION. UNDER NO CIRCUMSTANCES WILL SYNAPSE BE LIABLE TO YOU, OR ANY OTHER PERSON OR ENTITY, FOR ANY LOSS OF USE, REVENUE OR PROFIT, LOST OR DAMAGED DATA, OR OTHER COMMERCIAL OR ECONOMIC LOSS OR FOR ANY DAMAGES WHATSOEVER RELATED TO YOUR USE OR RELIANCE UPON THE SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGES OR IF SUCH DAMAGES ARE FORESEEABLE. THIS DISCLAIMER OF WARRANTY AND LIABILITY CONSTITUTES AN ESSENTIAL PART OF THIS LICENSE. NO USE OF ANY COVERED CODE IS AUTHORIZED HEREUNDER EXCEPT UNDER THIS DISCLAIMER.

"""
Sample SNAPpy script for a single SN111 Demonstration Board

Darkroom Timer:
  Hardware Setup -
    120v (max 10A) Enlarger power is connected through the Relay (TB1) on the
    SN111 Demonstration End Device.
  
  Operation -
    * Press the select-switch on any device to increment the counter
    * Hold the select-switch for 1 second until "--" is displayed to trigger relay
    * Hold the select-switch for 2 seconds to reset counter to 0
"""


# Use Synapse Evaluation Board definitions
from synapse.evalBase import *

@setHook(HOOK_STARTUP)
def startupEvent():
    """This is hooked into the HOOK_STARTUP event"""
    # Perform base eval-board initialization
    initDemoHw()

    print "Begin startup"
    global secondCounter, secondTimer
    global buttonState, buttonTime, buttonCount

    setRelayState(False)

    secondCounter = 0
    secondTimer = 0

    # Monitor for button-press events
    monitorPin(BUTTON_PIN,True)

    # Initialize button-detect variables
    buttonCount = 0
    buttonState = readPin(BUTTON_PIN)
    buttonTime = getMs()
    display2digits(buttonCount)

    print "End startup"

def doEverySecond():
    global runSecondCounter, secondTimer
    display2digits(secondTimer)
    if not secondTimer:
        runSecondCounter = False
        setRelayState(False)
        display2digits(buttonCount)
    else:
        setRelayState(True)
    secondTimer -= 1

@setHook(HOOK_100MS)
def timer100msEvent(currentMs):
    """Hooked into the HOOK_100MS event"""
    global secondCounter, runSecondCounter, secondTimer
    global buttonState,buttonTime,buttonCount

    secondCounter += 1
    if runSecondCounter and secondCounter >= 10:
        doEverySecond()
        secondCounter = 0
    elif not runSecondCounter and not buttonState:
        timeElapsed = currentMs - buttonTime
        if timeElapsed >= 2000:
            display2digits(0)
        elif timeElapsed >= 1000:
            setSegments(0x4040)

@setHook(HOOK_GPIN)
def buttonEvent(pinNum, isSet):
    """Hooked into the HOOK_GPIN event"""
    global secondCounter, runSecondCounter, secondTimer
    global buttonState, buttonTime, buttonCount
    if pinNum == BUTTON_PIN:
        #print isSet
        buttonState = isSet
        if not isSet:
            buttonTime = getMs()
        else:
            timeElapsed = getMs() - buttonTime
            if timeElapsed >= 2000:
                buttonCount = 0
                display2digits(buttonCount)
            elif timeElapsed >= 1000:
                secondTimer = buttonCount
                runSecondCounter = True
                secondCounter = 10
            else:
                buttonCount = (buttonCount + 1) % 100    # Rolling count 0-99
                display2digits(buttonCount)

