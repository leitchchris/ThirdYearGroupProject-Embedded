# Copyright (C) 2011 Synapse Wireless, Inc.
# Subject to your agreement of the disclaimer set forth below, permission is given by Synapse Wireless, Inc. ("Synapse") to you to freely modify, redistribute or include this SNAPpy code in any program. The purpose of this code is to help you understand and learn about SNAPpy by code examples.
# BY USING ALL OR ANY PORTION OF THIS SNAPPY CODE, YOU ACCEPT AND AGREE TO THE BELOW DISCLAIMER. If you do not accept or agree to the below disclaimer, then you may not use, modify, or distribute this SNAPpy code.
# THE CODE IS PROVIDED UNDER THIS LICENSE ON AN "AS IS" BASIS, WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, WITHOUT LIMITATION, WARRANTIES THAT THE COVERED CODE IS FREE OF DEFECTS, MERCHANTABLE, FIT FOR A PARTICULAR PURPOSE OR NON-INFRINGING. THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE COVERED CODE IS WITH YOU. SHOULD ANY COVERED CODE PROVE DEFECTIVE IN ANY RESPECT, YOU (NOT THE INITIAL DEVELOPER OR ANY OTHER CONTRIBUTOR) ASSUME THE COST OF ANY NECESSARY SERVICING, REPAIR OR CORRECTION. UNDER NO CIRCUMSTANCES WILL SYNAPSE BE LIABLE TO YOU, OR ANY OTHER PERSON OR ENTITY, FOR ANY LOSS OF USE, REVENUE OR PROFIT, LOST OR DAMAGED DATA, OR OTHER COMMERCIAL OR ECONOMIC LOSS OR FOR ANY DAMAGES WHATSOEVER RELATED TO YOUR USE OR RELIANCE UPON THE SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGES OR IF SUCH DAMAGES ARE FORESEEABLE. THIS DISCLAIMER OF WARRANTY AND LIABILITY CONSTITUTES AN ESSENTIAL PART OF THIS LICENSE. NO USE OF ANY COVERED CODE IS AUTHORIZED HEREUNDER EXCEPT UNDER THIS DISCLAIMER.

"""
Just a simple demo to show SNAP running on the ATMEL STK600 board.
The LEDs act as a 3-bit counter, and advance once a second.
Pushing the button on the STK600 will reverse the count.
"""

from synapse.STK600 import *

state = 0
dir = 1

@setHook(HOOK_STARTUP)
def startupEvent():
    setPinDir(RED_LED_IO, True)
    writePin(RED_LED_IO, RED_LED_OFF)
    setPinDir(YELLOW_LED_IO, True)
    writePin(YELLOW_LED_IO, RED_LED_OFF)
    setPinDir(GREEN_LED_IO, True)
    writePin(GREEN_LED_IO, RED_LED_OFF)

    setPinDir(BUTTON_IO, False)
    setPinPullup(BUTTON_IO, True)
    monitorPin(BUTTON_IO, True)

def advanceState():
    global state
    state += dir
    state &= 7

def updateLeds():
    redLed(state & 1)
    yellowLed(state & 2)
    greenLed(state & 4)

@setHook(HOOK_GPIN)
def buttonEvent(pin, isSet):
    global dir
    if pin == BUTTON_IO:
        if not isSet: # toggle dir only on the button PRESS...
            dir = -dir

@setHook(HOOK_1S)
def everySecond():
    advanceState()
    updateLeds()
