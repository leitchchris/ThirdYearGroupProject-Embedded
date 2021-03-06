# Copyright (C) 2011 Synapse Wireless, Inc.
# Subject to your agreement of the disclaimer set forth below, permission is given by Synapse Wireless, Inc. ("Synapse") to you to freely modify, redistribute or include this SNAPpy code in any program. The purpose of this code is to help you understand and learn about SNAPpy by code examples.
# BY USING ALL OR ANY PORTION OF THIS SNAPPY CODE, YOU ACCEPT AND AGREE TO THE BELOW DISCLAIMER. If you do not accept or agree to the below disclaimer, then you may not use, modify, or distribute this SNAPpy code.
# THE CODE IS PROVIDED UNDER THIS LICENSE ON AN "AS IS" BASIS, WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, WITHOUT LIMITATION, WARRANTIES THAT THE COVERED CODE IS FREE OF DEFECTS, MERCHANTABLE, FIT FOR A PARTICULAR PURPOSE OR NON-INFRINGING. THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE COVERED CODE IS WITH YOU. SHOULD ANY COVERED CODE PROVE DEFECTIVE IN ANY RESPECT, YOU (NOT THE INITIAL DEVELOPER OR ANY OTHER CONTRIBUTOR) ASSUME THE COST OF ANY NECESSARY SERVICING, REPAIR OR CORRECTION. UNDER NO CIRCUMSTANCES WILL SYNAPSE BE LIABLE TO YOU, OR ANY OTHER PERSON OR ENTITY, FOR ANY LOSS OF USE, REVENUE OR PROFIT, LOST OR DAMAGED DATA, OR OTHER COMMERCIAL OR ECONOMIC LOSS OR FOR ANY DAMAGES WHATSOEVER RELATED TO YOUR USE OR RELIANCE UPON THE SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGES OR IF SUCH DAMAGES ARE FORESEEABLE. THIS DISCLAIMER OF WARRANTY AND LIABILITY CONSTITUTES AN ESSENTIAL PART OF THIS LICENSE. NO USE OF ANY COVERED CODE IS AUTHORIZED HEREUNDER EXCEPT UNDER THIS DISCLAIMER.

"""
Multicast Counter script for ATmega128RFA1 on the Dresden RCB
"""

# Defininitions of Dresden RCB

# IO16 - IO23 = PE0 - PE7
LED2 = 18    # PE2
LED3 = 19    # PE3
LED4 = 20    # PE4
BUTTON = 21  # PE5

buttonCount = 1  # Init to 1 so we see an LED on power-up

@setHook(HOOK_STARTUP)
def startupEvent():
    """Called at system startup"""
    
    # Initialize LEDs
    setPinDir(LED2, True)
    setPinDir(LED3, True)
    setPinDir(LED4, True)
    setLedCount(buttonCount)
    
    # Monitor for button-press events
    setPinDir(BUTTON, False)
    setPinPullup(BUTTON, True)
    monitorPin(BUTTON, True)

@setHook(HOOK_GPIN)
def gpinEvent(pin, isSet):
    """Detect button-press"""
    if pin == BUTTON and not isSet:
        buttonPress()

def setLedCount(count):
    """Display binary 3-bit count on LEDs"""
    writePin(LED2, not (count & 0x04))
    writePin(LED3, not (count & 0x02))
    writePin(LED4, not (count & 0x01))

def buttonPress():
    """Handle button press"""
    global buttonCount
    buttonCount += 1
    
    # Display the count on LEDs
    setLedCount(buttonCount)
    
    # Broadcast count over Radio
    mcastRpc(1, 2, 'setButtonCount', buttonCount)    
    
def setButtonCount(newCount):
    """Receive new count over the air"""
    global buttonCount
    buttonCount = newCount
    setLedCount(buttonCount)
    