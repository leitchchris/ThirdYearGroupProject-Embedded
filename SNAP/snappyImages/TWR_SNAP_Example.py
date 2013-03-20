# Copyright (C) 2011 Synapse Wireless, Inc.
# Subject to your agreement of the disclaimer set forth below, permission is given by Synapse Wireless, Inc. ("Synapse") to you to freely modify, redistribute or include this SNAPpy code in any program. The purpose of this code is to help you understand and learn about SNAPpy by code examples.
# BY USING ALL OR ANY PORTION OF THIS SNAPPY CODE, YOU ACCEPT AND AGREE TO THE BELOW DISCLAIMER. If you do not accept or agree to the below disclaimer, then you may not use, modify, or distribute this SNAPpy code.
# THE CODE IS PROVIDED UNDER THIS LICENSE ON AN "AS IS" BASIS, WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, WITHOUT LIMITATION, WARRANTIES THAT THE COVERED CODE IS FREE OF DEFECTS, MERCHANTABLE, FIT FOR A PARTICULAR PURPOSE OR NON-INFRINGING. THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE COVERED CODE IS WITH YOU. SHOULD ANY COVERED CODE PROVE DEFECTIVE IN ANY RESPECT, YOU (NOT THE INITIAL DEVELOPER OR ANY OTHER CONTRIBUTOR) ASSUME THE COST OF ANY NECESSARY SERVICING, REPAIR OR CORRECTION. UNDER NO CIRCUMSTANCES WILL SYNAPSE BE LIABLE TO YOU, OR ANY OTHER PERSON OR ENTITY, FOR ANY LOSS OF USE, REVENUE OR PROFIT, LOST OR DAMAGED DATA, OR OTHER COMMERCIAL OR ECONOMIC LOSS OR FOR ANY DAMAGES WHATSOEVER RELATED TO YOUR USE OR RELIANCE UPON THE SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGES OR IF SUCH DAMAGES ARE FORESEEABLE. THIS DISCLAIMER OF WARRANTY AND LIABILITY CONSTITUTES AN ESSENTIAL PART OF THIS LICENSE. NO USE OF ANY COVERED CODE IS AUTHORIZED HEREUNDER EXCEPT UNDER THIS DISCLAIMER.

'''-----Freescale Tower board example script using SM700/TWR-RF-SNAP module-----
This script will continuously blink the RED LED and use the push buttons (SWITCH2
and SWITCH3) to turn the GREEN LED ON and OFF

Actions:
    Press SWITCH3 - Turn ON the GREEN LED
    Press SWITCH2 - Turn OFF the GREEN LED
'''
from synapse.platforms import *

# Pin Definitions - mapping IO to the SM700 functionality
TMR0_GP8 = 8
TMR1_GP9 = 9
KBI0_GP22 = 22
KBI1_GP23 = 23

RED_LED = TMR0_GP8
GRN_LED = TMR1_GP9

SW2 = KBI0_GP22
SW3 = KBI1_GP23

if platform != "SM700":
    compileError #script only valid on SM700
    
@setHook(HOOK_STARTUP)
def init():
    '''Start-up event'''
    # Configure LED pins
    setPinDir(RED_LED, True)
    setPinDir(GRN_LED, True)
    
    # Pulse the LEDs once during start-up
    pulsePin(RED_LED, 80, True)
    pulsePin(GRN_LED, 80, True)
    
    #Configure switch pins - monitor for button press
    setPinDir(SW2, False)
    setPinPullup(SW2, True)
    monitorPin(SW2, True)
    setPinDir(SW3, False)
    setPinPullup(SW3, True)
    monitorPin(SW3, True)
    
def controlGreenLed(lightLed):
    '''Turn the green LED ON or OFF'''
    if lightLed:
        writePin(GRN_LED, True)
    else:
        writePin(GRN_LED, False)

@setHook(HOOK_GPIN)
def buttonPress(pin, isSet):
    '''Pin transition event handler (button press)'''
    print "Button Press ", pin, "=", isSet
    
    if pin == SW2 and not isSet:
        writePin(GRN_LED, True)
    elif pin == SW3 and not isSet:
        writePin(GRN_LED, False)        
        
@setHook(HOOK_1S)
def tick():
    '''Timer tick event handler (1 second)'''
    pulsePin(RED_LED, 200, True)
    
