# Copyright (C) 2011 Synapse Wireless, Inc.
# Subject to your agreement of the disclaimer set forth below, permission is given by Synapse Wireless, Inc. ("Synapse") to you to freely modify, redistribute or include this SNAPpy code in any program. The purpose of this code is to help you understand and learn about SNAPpy by code examples.
# BY USING ALL OR ANY PORTION OF THIS SNAPPY CODE, YOU ACCEPT AND AGREE TO THE BELOW DISCLAIMER. If you do not accept or agree to the below disclaimer, then you may not use, modify, or distribute this SNAPpy code.
# THE CODE IS PROVIDED UNDER THIS LICENSE ON AN "AS IS" BASIS, WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, WITHOUT LIMITATION, WARRANTIES THAT THE COVERED CODE IS FREE OF DEFECTS, MERCHANTABLE, FIT FOR A PARTICULAR PURPOSE OR NON-INFRINGING. THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE COVERED CODE IS WITH YOU. SHOULD ANY COVERED CODE PROVE DEFECTIVE IN ANY RESPECT, YOU (NOT THE INITIAL DEVELOPER OR ANY OTHER CONTRIBUTOR) ASSUME THE COST OF ANY NECESSARY SERVICING, REPAIR OR CORRECTION. UNDER NO CIRCUMSTANCES WILL SYNAPSE BE LIABLE TO YOU, OR ANY OTHER PERSON OR ENTITY, FOR ANY LOSS OF USE, REVENUE OR PROFIT, LOST OR DAMAGED DATA, OR OTHER COMMERCIAL OR ECONOMIC LOSS OR FOR ANY DAMAGES WHATSOEVER RELATED TO YOUR USE OR RELIANCE UPON THE SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGES OR IF SUCH DAMAGES ARE FORESEEABLE. THIS DISCLAIMER OF WARRANTY AND LIABILITY CONSTITUTES AN ESSENTIAL PART OF THIS LICENSE. NO USE OF ANY COVERED CODE IS AUTHORIZED HEREUNDER EXCEPT UNDER THIS DISCLAIMER.

'''
  Link Quality Ranger
    Sample SNAPpy script for evaluation boards. Demonstrates receive link quality from peer unit.
    Instructions:  Load script into two evaluation boards and watch the 2 digit display.
'''

from synapse.evalBase import *

lqTimeout = 0
lqSum = 0
lqCount = 0

@setHook(HOOK_STARTUP)
def startupEvent():
    display2digits(0)

# Comment the following out if you have your own HOOK_10MS handler
# (and be sure to call updateSevenSegmentDisplay() from your own handler)
@setHook(HOOK_10MS)
def defaultTimerHandler():
    updateSevenSegmentDisplay()

def getPercentLq():
    maxDbm = 18
    minDbm = 95
    percent = 100 - ((getLq() - maxDbm) * 100) / (minDbm - maxDbm)
    return percent

def displayLq(value):
    display2digits(value)

def remoteLQ():
    """Called from remote end.  Display LQ averaged over previous second."""
    global lqSum, lqCount, lqTimeout
    lqCount += 1
    lqSum += getPercentLq()
    if lqCount == 10:
        displayLq(lqSum / lqCount)
        lqSum = 0
        lqCount = 0
        
    # Reset the "not receiving" timeout    
    lqTimeout = 10

@setHook(HOOK_100MS)
def time100MsHook(time):
    """Broadcast ONE HOP remoteLQ() call every 100ms"""
    mcastRpc(1, 1, "remoteLQ")
    
    # If we haven't received a remoteLQ() call in the last second, zero the display
    global lqTimeout
    if lqTimeout > 0:
        lqTimeout -= 1
        if lqTimeout == 0:
            display2digits(0)

