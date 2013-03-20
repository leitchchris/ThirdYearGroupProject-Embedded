# Copyright (C) 2011 Synapse Wireless, Inc.
# Subject to your agreement of the disclaimer set forth below, permission is given by Synapse Wireless, Inc. ("Synapse") to you to freely modify, redistribute or include this SNAPpy code in any program. The purpose of this code is to help you understand and learn about SNAPpy by code examples.
# BY USING ALL OR ANY PORTION OF THIS SNAPPY CODE, YOU ACCEPT AND AGREE TO THE BELOW DISCLAIMER. If you do not accept or agree to the below disclaimer, then you may not use, modify, or distribute this SNAPpy code.
# THE CODE IS PROVIDED UNDER THIS LICENSE ON AN "AS IS" BASIS, WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, WITHOUT LIMITATION, WARRANTIES THAT THE COVERED CODE IS FREE OF DEFECTS, MERCHANTABLE, FIT FOR A PARTICULAR PURPOSE OR NON-INFRINGING. THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE COVERED CODE IS WITH YOU. SHOULD ANY COVERED CODE PROVE DEFECTIVE IN ANY RESPECT, YOU (NOT THE INITIAL DEVELOPER OR ANY OTHER CONTRIBUTOR) ASSUME THE COST OF ANY NECESSARY SERVICING, REPAIR OR CORRECTION. UNDER NO CIRCUMSTANCES WILL SYNAPSE BE LIABLE TO YOU, OR ANY OTHER PERSON OR ENTITY, FOR ANY LOSS OF USE, REVENUE OR PROFIT, LOST OR DAMAGED DATA, OR OTHER COMMERCIAL OR ECONOMIC LOSS OR FOR ANY DAMAGES WHATSOEVER RELATED TO YOUR USE OR RELIANCE UPON THE SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGES OR IF SUCH DAMAGES ARE FORESEEABLE. THIS DISCLAIMER OF WARRANTY AND LIABILITY CONSTITUTES AN ESSENTIAL PART OF THIS LICENSE. NO USE OF ANY COVERED CODE IS AUTHORIZED HEREUNDER EXCEPT UNDER THIS DISCLAIMER.

"""
  Buzzer - an example script for the EK2500 Evaluation Kit

    Demonstrates how a node can provide a service to other nodes

    Written for the SN171 Proto Board
        * Device Type = "Buzz"
        * Has a Piezo buzzer attached to GPIO9
        * All SN171 boards have a LED on GPIO2
        * All SN171 boards can be jumpered for a push-button switch on GPIO5
        * All SN171 boards have another LED on GPIO1 but this script does not use it

"""
from synapse.platforms import *

secondCounter = 0
LED_PIN = GPIO_2
BUTTON_PIN = GPIO_5
BUZZER_PIN = GPIO_9

@setHook(HOOK_STARTUP)
def startupEvent():
    """This is hooked into the HOOK_STARTUP event"""
    writePin(LED_PIN, False)
    setPinDir(LED_PIN, True)

    setPinDir(BUTTON_PIN, False)
    setPinPullup(BUTTON_PIN, True)
    monitorPin(BUTTON_PIN, True)

    writePin(BUZZER_PIN, False)
    setPinDir(BUZZER_PIN, True)

    # announce our presence to anyone listening
    mcastRpc(1,5,'buzzerAt',localAddr())

def findBuzzer():
    """Devices who WANT buzzer capability call this function"""
    rpc(rpcSourceAddr(), 'buzzerAt', localAddr())

def buzzer(duration):
    """Call this to get a beep"""
    global BUZZER_PIN
    pulsePin(BUZZER_PIN, duration, True)

@setHook(HOOK_100MS)
def poll100ms(msTick):
    global secondCounter, LED_PIN

    secondCounter += 1
    if secondCounter >= 10:
        pulsePin(LED_PIN, 200, True)
        secondCounter = 0

@setHook(HOOK_GPIN)
def buttonEvent(pinNum, isSet):
    """Hooked into the HOOK_GPIN event"""
    global BUTTON_PIN

    if pinNum == BUTTON_PIN:
        if not isSet:
            buzzer(100)