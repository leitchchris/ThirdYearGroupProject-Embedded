# Copyright (C) 2011 Synapse Wireless, Inc.
# Subject to your agreement of the disclaimer set forth below, permission is given by Synapse Wireless, Inc. ("Synapse") to you to freely modify, redistribute or include this SNAPpy code in any program. The purpose of this code is to help you understand and learn about SNAPpy by code examples.
# BY USING ALL OR ANY PORTION OF THIS SNAPPY CODE, YOU ACCEPT AND AGREE TO THE BELOW DISCLAIMER. If you do not accept or agree to the below disclaimer, then you may not use, modify, or distribute this SNAPpy code.
# THE CODE IS PROVIDED UNDER THIS LICENSE ON AN "AS IS" BASIS, WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, WITHOUT LIMITATION, WARRANTIES THAT THE COVERED CODE IS FREE OF DEFECTS, MERCHANTABLE, FIT FOR A PARTICULAR PURPOSE OR NON-INFRINGING. THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE COVERED CODE IS WITH YOU. SHOULD ANY COVERED CODE PROVE DEFECTIVE IN ANY RESPECT, YOU (NOT THE INITIAL DEVELOPER OR ANY OTHER CONTRIBUTOR) ASSUME THE COST OF ANY NECESSARY SERVICING, REPAIR OR CORRECTION. UNDER NO CIRCUMSTANCES WILL SYNAPSE BE LIABLE TO YOU, OR ANY OTHER PERSON OR ENTITY, FOR ANY LOSS OF USE, REVENUE OR PROFIT, LOST OR DAMAGED DATA, OR OTHER COMMERCIAL OR ECONOMIC LOSS OR FOR ANY DAMAGES WHATSOEVER RELATED TO YOUR USE OR RELIANCE UPON THE SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGES OR IF SUCH DAMAGES ARE FORESEEABLE. THIS DISCLAIMER OF WARRANTY AND LIABILITY CONSTITUTES AN ESSENTIAL PART OF THIS LICENSE. NO USE OF ANY COVERED CODE IS AUTHORIZED HEREUNDER EXCEPT UNDER THIS DISCLAIMER.

'''
  Link Quality Ranger for the ZIC2410 "EVB3" Evaluation Board
    Sample SNAPpy script for evaluation boards. Demonstrates receive link quality from peer unit.
    Instructions:  Load script into two evaluation boards and watch the display.
'''

from ZIC2410EVB3 import *

lqTimeout = 0
lqSum = 0
lqCount = 0
lcdPresent = False

@setHook(HOOK_STARTUP)
def startupEvent():
    global lcdPresent
    
    # On an EVB3, LED4 is on the same pin as UART0 RX
    # Shut down UART0 so we can control the pin manually
    initUart(0,0)

    # Uncomment the following line to disable PacketSerial (increases performance when used remotely)
    # crossConnect(0,6)
    
    # Initialize and clear LCD
    lcdPresent = lcdPlot()
    if lcdPresent:
        lcdPlot("\x01  Link Quality Test!  \x02\n\n")
    else:
        # Use LEDs as a "bar graph"
        setPinDir(LED1, True)
        setPinDir(LED2, True)
        setPinDir(LED3, True)
        setPinDir(LED4, True)

def displayLq(value):
    if lcdPresent:
        lcdPlot("LQ = -" + str(value) + "dBm\n")
    else:
        bars5 = value / 20   # 5 Bars: assume range of 0 to 100 dBm
        ledMask = 0x0F << bars5
        writePin(LED1, ledMask & 1)
        writePin(LED2, ledMask & 2)
        writePin(LED3, ledMask & 4)
        writePin(LED4, ledMask & 8)

def remoteLQ():
    """Called from remote end.  Display LQ averaged over previous second."""
    global lqSum, lqCount, lqTimeout
    lqCount += 1
    lqSum += getLq()
    if lqCount == 10:
        displayLq(lqSum / lqCount)
        lqSum = 0
        lqCount = 0
        
    # Reset the "not receiving" timeout    
    lqTimeout = 10

@setHook(HOOK_100MS)
def time100MsHook(time):
    """Broadcast ONE HOP remoteLQ() call every 100ms"""
    global secCount
    
    # Broadcast rpc to all listeners
    mcastRpc(1, 1, "remoteLQ")

    # If we haven't received a remoteLQ() call in the last second, zero the display
    global lqTimeout
    if lqTimeout > 0:
        lqTimeout -= 1
        if lqTimeout == 0:
            if lcdPresent:
                lcdPlot("No rx\n")
            else:
                displayLq(100)
