# Copyright (C) 2011 Synapse Wireless, Inc.
# Subject to your agreement of the disclaimer set forth below, permission is given by Synapse Wireless, Inc. ("Synapse") to you to freely modify, redistribute or include this SNAPpy code in any program. The purpose of this code is to help you understand and learn about SNAPpy by code examples.
# BY USING ALL OR ANY PORTION OF THIS SNAPPY CODE, YOU ACCEPT AND AGREE TO THE BELOW DISCLAIMER. If you do not accept or agree to the below disclaimer, then you may not use, modify, or distribute this SNAPpy code.
# THE CODE IS PROVIDED UNDER THIS LICENSE ON AN "AS IS" BASIS, WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, WITHOUT LIMITATION, WARRANTIES THAT THE COVERED CODE IS FREE OF DEFECTS, MERCHANTABLE, FIT FOR A PARTICULAR PURPOSE OR NON-INFRINGING. THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE COVERED CODE IS WITH YOU. SHOULD ANY COVERED CODE PROVE DEFECTIVE IN ANY RESPECT, YOU (NOT THE INITIAL DEVELOPER OR ANY OTHER CONTRIBUTOR) ASSUME THE COST OF ANY NECESSARY SERVICING, REPAIR OR CORRECTION. UNDER NO CIRCUMSTANCES WILL SYNAPSE BE LIABLE TO YOU, OR ANY OTHER PERSON OR ENTITY, FOR ANY LOSS OF USE, REVENUE OR PROFIT, LOST OR DAMAGED DATA, OR OTHER COMMERCIAL OR ECONOMIC LOSS OR FOR ANY DAMAGES WHATSOEVER RELATED TO YOUR USE OR RELIANCE UPON THE SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGES OR IF SUCH DAMAGES ARE FORESEEABLE. THIS DISCLAIMER OF WARRANTY AND LIABILITY CONSTITUTES AN ESSENTIAL PART OF THIS LICENSE. NO USE OF ANY COVERED CODE IS AUTHORIZED HEREUNDER EXCEPT UNDER THIS DISCLAIMER.

"""
Sample SNAPpy script for a single Demonstration Board (SN111/163)
    The seven segment display will show the channel, network id, and network address in sequence.
"""

from synapse.evalBase import *

secondCounter = 0
addrIndex = 0

@setHook(HOOK_STARTUP)
def startupEvent():
    """This is hooked into the HOOK_STARTUP event"""
    # Perform base eval-board initialization
    initDemoHw()

def hexToSegments(nibble):
    """Map hexadecimal digits onto 7-segment display"""
    hexFont = '\x3F\x06\x5B\x4F\x66\x6D\x7D\x07\x7F\x67\x77\x7c\x39\x5e\x79\x71'
    if nibble < 0 or nibble > 15:
        return 0x04
    return ord(hexFont[nibble])

def hexDisplay(value):
    """
    Use
    0x100 for "  " (Off)
    0x101 for "--"
    0x102 for "__"
    """

    if value == 0x100:
        segmentValue = 0 # Off
    elif value == 0x101:
        segmentValue = 0x4040 # "--"
    elif value == 0x102:
        segmentValue = 0x0808 # "__"
    else: # handle everything between 0x00 and 0xFF
        msd = (value & 0x00F0) >> 4
        mss = hexToSegments(msd)
        lsd = value & 0x000F
        lss = hexToSegments(lsd)
        segmentValue = (mss << 8) + lss
    setSegments(segmentValue)

def displayLocalAddr():
    global addrIndex
    if addrIndex == 3 or addrIndex == 5 or addrIndex == 8:
        hexDisplay(0x100)  #blank the display
    elif addrIndex == 4:
        hexDisplay(getChannel())
    elif addrIndex == 6:
        hexDisplay( (getNetId() & 0xFF00 ) >> 8)
    elif addrIndex == 7:
        hexDisplay(getNetId() & 0x00FF)
    else:
        hexDisplay(ord(localAddr()[addrIndex]))
    addrIndex = (addrIndex + 1) % 9

def doEverySecond():
    blinkLed(200)
    displayLocalAddr()

@setHook(HOOK_100MS)
def timer100msEvent(currentMs):
    global secondCounter

    secondCounter += 1
    if secondCounter >= 10:
        doEverySecond()
        secondCounter = 0  
