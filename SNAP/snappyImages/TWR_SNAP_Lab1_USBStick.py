# Copyright (C) 2011 Synapse Wireless, Inc.
# Subject to your agreement of the disclaimer set forth below, permission is given by Synapse Wireless, Inc. ("Synapse") to you to freely modify, redistribute or include this SNAPpy code in any program. The purpose of this code is to help you understand and learn about SNAPpy by code examples.
# BY USING ALL OR ANY PORTION OF THIS SNAPPY CODE, YOU ACCEPT AND AGREE TO THE BELOW DISCLAIMER. If you do not accept or agree to the below disclaimer, then you may not use, modify, or distribute this SNAPpy code.
# THE CODE IS PROVIDED UNDER THIS LICENSE ON AN "AS IS" BASIS, WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, WITHOUT LIMITATION, WARRANTIES THAT THE COVERED CODE IS FREE OF DEFECTS, MERCHANTABLE, FIT FOR A PARTICULAR PURPOSE OR NON-INFRINGING. THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE COVERED CODE IS WITH YOU. SHOULD ANY COVERED CODE PROVE DEFECTIVE IN ANY RESPECT, YOU (NOT THE INITIAL DEVELOPER OR ANY OTHER CONTRIBUTOR) ASSUME THE COST OF ANY NECESSARY SERVICING, REPAIR OR CORRECTION. UNDER NO CIRCUMSTANCES WILL SYNAPSE BE LIABLE TO YOU, OR ANY OTHER PERSON OR ENTITY, FOR ANY LOSS OF USE, REVENUE OR PROFIT, LOST OR DAMAGED DATA, OR OTHER COMMERCIAL OR ECONOMIC LOSS OR FOR ANY DAMAGES WHATSOEVER RELATED TO YOUR USE OR RELIANCE UPON THE SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGES OR IF SUCH DAMAGES ARE FORESEEABLE. THIS DISCLAIMER OF WARRANTY AND LIABILITY CONSTITUTES AN ESSENTIAL PART OF THIS LICENSE. NO USE OF ANY COVERED CODE IS AUTHORIZED HEREUNDER EXCEPT UNDER THIS DISCLAIMER.

'''-----Freescale Tower board example script using USB module-----
Script will allow for remote control of on-board LEDs.

Actions:
    GREEN LED and RED LED will mimic the equivalent LEDs on the
    tower board.
    
    Press tower board Switch-3 - Flash the RED LED
    Press tower board Switch-2 - Flash the GREEN LED
'''

from synapse.platforms import *

if platform != "SM700":
    compileError #script only valid on SM700

#---Pin Definitions - mapping IO to the SM700 functionality---
RED_LED = GPIO_8
GRN_LED = GPIO_26

@setHook(HOOK_STARTUP)
def init():
    '''Start-up routine'''
    # Configure LED pins
    setPinDir(RED_LED, True)
    setPinDir(GRN_LED, True)
    
    # Pulse the LEDs once during start-up
    pulsePin(RED_LED, 80, False)
    pulsePin(GRN_LED, 80, False)
    
def pulseRedLed(msec):
    '''Pulse the RED LED for the specified time (in ms)'''
    pulsePin(RED_LED, msec, False)
    
def pulseGreenLed(msec):
    '''Pulse the GREEN LED for the specified time (in ms)'''
    pulsePin(GRN_LED, msec, False)
        