# Copyright (C) 2011 Synapse Wireless, Inc.
# Subject to your agreement of the disclaimer set forth below, permission is given by Synapse Wireless, Inc. ("Synapse") to you to freely modify, redistribute or include this SNAPpy code in any program. The purpose of this code is to help you understand and learn about SNAPpy by code examples.
# BY USING ALL OR ANY PORTION OF THIS SNAPPY CODE, YOU ACCEPT AND AGREE TO THE BELOW DISCLAIMER. If you do not accept or agree to the below disclaimer, then you may not use, modify, or distribute this SNAPpy code.
# THE CODE IS PROVIDED UNDER THIS LICENSE ON AN "AS IS" BASIS, WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, WITHOUT LIMITATION, WARRANTIES THAT THE COVERED CODE IS FREE OF DEFECTS, MERCHANTABLE, FIT FOR A PARTICULAR PURPOSE OR NON-INFRINGING. THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE COVERED CODE IS WITH YOU. SHOULD ANY COVERED CODE PROVE DEFECTIVE IN ANY RESPECT, YOU (NOT THE INITIAL DEVELOPER OR ANY OTHER CONTRIBUTOR) ASSUME THE COST OF ANY NECESSARY SERVICING, REPAIR OR CORRECTION. UNDER NO CIRCUMSTANCES WILL SYNAPSE BE LIABLE TO YOU, OR ANY OTHER PERSON OR ENTITY, FOR ANY LOSS OF USE, REVENUE OR PROFIT, LOST OR DAMAGED DATA, OR OTHER COMMERCIAL OR ECONOMIC LOSS OR FOR ANY DAMAGES WHATSOEVER RELATED TO YOUR USE OR RELIANCE UPON THE SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGES OR IF SUCH DAMAGES ARE FORESEEABLE. THIS DISCLAIMER OF WARRANTY AND LIABILITY CONSTITUTES AN ESSENTIAL PART OF THIS LICENSE. NO USE OF ANY COVERED CODE IS AUTHORIZED HEREUNDER EXCEPT UNDER THIS DISCLAIMER.

"""
Sample SNAPpy script for CEL ZIC2410 "EVB3" Evaluation Board

** Multicast Counter **

"""

from ZIC2410EVB3 import *

lcdPresent = False
buttonCount = 0

@setHook(HOOK_STARTUP)
def startup():
    global lcdPresent

    # On an EVB3, LED4 is on the same pin as UART0 RX
    # Shut down UART0 so we can control the pin manually
    initUart(0,0)
    
    # Initialize and clear LCD
    lcdPresent = lcdPlot()
    
    if lcdPresent:
        lcdPlot("\x01CEL\x02 Multicast Counter!\n\n")
    else:
        # Use the four LEDs as a 4-bit counter
        setPinDir(LED1, True)
        setPinDir(LED2, True)
        setPinDir(LED3, True)
        setPinDir(LED4, True)
        displayCount("")
    
    # Initialize SW3 AKA "INT0" pin as an "up-count" button input
    setPinDir(SW3, False)
    setPinPullup(SW3, True)
    monitorPin(SW3, True)
    
    # Initialize SW4 AKA "INT1" pin as an "down-count" button input
    setPinDir(SW4, False)
    setPinPullup(SW4, True)
    monitorPin(SW4, True)

def showLcdStat():
    print "status = ", lcdPresent

def setButtonCount(count):
    global buttonCount
    buttonCount = count

    countStr = "Rx Count = " + str(count) + "\n"
    displayCount(countStr)

def reportButtonCount():
    """Report to others that button press took place"""
    global buttonCount
    mcastRpc(1,2,'setButtonCount',buttonCount)
    countStr = "Tx Count = " + str(buttonCount) + "\n"
    displayCount(countStr)

@setHook(HOOK_GPIN)
def buttonEvent(pin, isSet):
    global buttonCount
    if not isSet:
        countDir = +1 if pin == SW3 else -1
        deltaCount = 1
        buttonCount = buttonCount + countDir * deltaCount
        if buttonCount < 0:
            buttonCount += 100
            
        buttonCount %= 100    # Wrap count at 99
        reportButtonCount()
        
def updateLeds():
    """When no LCD present, we use LEDs to show a 4-bit count"""
    if not lcdPresent:
        writePin(LED1, buttonCount & 1)
        writePin(LED2, buttonCount & 2)
        writePin(LED3, buttonCount & 4)
        writePin(LED4, buttonCount & 8)

def displayCount(countStr):
    if lcdPresent:
        lcdPlot(countStr)
    else:
        updateLeds()
