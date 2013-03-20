# Copyright (C) 2011 Synapse Wireless, Inc.
# Subject to your agreement of the disclaimer set forth below, permission is given by Synapse Wireless, Inc. ("Synapse") to you to freely modify, redistribute or include this SNAPpy code in any program. The purpose of this code is to help you understand and learn about SNAPpy by code examples.
# BY USING ALL OR ANY PORTION OF THIS SNAPPY CODE, YOU ACCEPT AND AGREE TO THE BELOW DISCLAIMER. If you do not accept or agree to the below disclaimer, then you may not use, modify, or distribute this SNAPpy code.
# THE CODE IS PROVIDED UNDER THIS LICENSE ON AN "AS IS" BASIS, WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, WITHOUT LIMITATION, WARRANTIES THAT THE COVERED CODE IS FREE OF DEFECTS, MERCHANTABLE, FIT FOR A PARTICULAR PURPOSE OR NON-INFRINGING. THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE COVERED CODE IS WITH YOU. SHOULD ANY COVERED CODE PROVE DEFECTIVE IN ANY RESPECT, YOU (NOT THE INITIAL DEVELOPER OR ANY OTHER CONTRIBUTOR) ASSUME THE COST OF ANY NECESSARY SERVICING, REPAIR OR CORRECTION. UNDER NO CIRCUMSTANCES WILL SYNAPSE BE LIABLE TO YOU, OR ANY OTHER PERSON OR ENTITY, FOR ANY LOSS OF USE, REVENUE OR PROFIT, LOST OR DAMAGED DATA, OR OTHER COMMERCIAL OR ECONOMIC LOSS OR FOR ANY DAMAGES WHATSOEVER RELATED TO YOUR USE OR RELIANCE UPON THE SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGES OR IF SUCH DAMAGES ARE FORESEEABLE. THIS DISCLAIMER OF WARRANTY AND LIABILITY CONSTITUTES AN ESSENTIAL PART OF THIS LICENSE. NO USE OF ANY COVERED CODE IS AUTHORIZED HEREUNDER EXCEPT UNDER THIS DISCLAIMER.

"""
ProtoBoard script:  Sleep after first button press, wake and send multicastCount on subsequent presses.
    Use this script along with McastCounter.py on Demonstration Boards.
    Note:
       * Once sleeping, you'll need to reset the board to access from Portal again!
       * To minimize power consumption remove the RS232 jumpers, and use VBAT power input
"""

# Use Synapse Evaluation Board definitions
from synapse.evalBase import *
from synapse.pinWakeup import *
from synapse.switchboard import *

secondCounter = 0
buttonCount = 0
started = False

@setHook(HOOK_STARTUP)
def startupEvent():
    """This is hooked into the HOOK_STARTUP event"""
    global secondCounter

    # Default all pins to output/low for minimum power consumption
    index = 0
    while index < len(GPIO_TO_IO_LIST):
        pin = GPIO_TO_IO_LIST[index]
        setPinDir(pin,True)
        writePin(pin,False)
        index += 1

    # Detect and initialize the hardware (assumes running on the Proto Board)
    initProtoHw()

    # Turn on LED until we enter low-power state (first button press)
    writePin(LED_PIN, True)
    
    # Monitor for button-press events
    monitorPin(BUTTON_PIN, True)
    wakeupOn(BUTTON_PIN, True, False)  # Wake on falling edge
    
    # Don't try to mcast rpc's over PacketSerial link
    crossConnect(DS_PACKET_SERIAL, DS_NULL)

@setHook(HOOK_GPIN)
def buttonEvent(pinNum, isSet):
    """Hooked into the HOOK_GPIN event"""
    global buttonCount
    if pinNum == BUTTON_PIN:
        # Send on rising edge, so 'wake' hardware will see transition before sleep
        if isSet:
            # Increment count of button-presses
            buttonCount = buttonCount + 1
            
            buttonCount %= 100    # Wrap count at 99
            reportButtonCount()
            
def setButtonCount(newCount):
    global buttonCount
    buttonCount = newCount

def reportButtonCount():
    global buttonCount, started
    mcastRpc(1,2,'setButtonCount',buttonCount)
    writePin(LED_PIN, True)
    started = True

@setHook(HOOK_RPC_SENT)
def rpcSentEvent():
    """Called after mcast(setButtonCount) is sent. Sleep until next button press"""
    if started:
        writePin(LED_PIN, False)
        sleep(0,0)  # Sleep mode 0 (lowest current), Forever


