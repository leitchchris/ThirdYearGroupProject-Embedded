# Copyright (C) 2011 Synapse Wireless, Inc.
# Subject to your agreement of the disclaimer set forth below, permission is given by Synapse Wireless, Inc. ("Synapse") to you to freely modify, redistribute or include this SNAPpy code in any program. The purpose of this code is to help you understand and learn about SNAPpy by code examples.
# BY USING ALL OR ANY PORTION OF THIS SNAPPY CODE, YOU ACCEPT AND AGREE TO THE BELOW DISCLAIMER. If you do not accept or agree to the below disclaimer, then you may not use, modify, or distribute this SNAPpy code.
# THE CODE IS PROVIDED UNDER THIS LICENSE ON AN "AS IS" BASIS, WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, WITHOUT LIMITATION, WARRANTIES THAT THE COVERED CODE IS FREE OF DEFECTS, MERCHANTABLE, FIT FOR A PARTICULAR PURPOSE OR NON-INFRINGING. THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE COVERED CODE IS WITH YOU. SHOULD ANY COVERED CODE PROVE DEFECTIVE IN ANY RESPECT, YOU (NOT THE INITIAL DEVELOPER OR ANY OTHER CONTRIBUTOR) ASSUME THE COST OF ANY NECESSARY SERVICING, REPAIR OR CORRECTION. UNDER NO CIRCUMSTANCES WILL SYNAPSE BE LIABLE TO YOU, OR ANY OTHER PERSON OR ENTITY, FOR ANY LOSS OF USE, REVENUE OR PROFIT, LOST OR DAMAGED DATA, OR OTHER COMMERCIAL OR ECONOMIC LOSS OR FOR ANY DAMAGES WHATSOEVER RELATED TO YOUR USE OR RELIANCE UPON THE SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGES OR IF SUCH DAMAGES ARE FORESEEABLE. THIS DISCLAIMER OF WARRANTY AND LIABILITY CONSTITUTES AN ESSENTIAL PART OF THIS LICENSE. NO USE OF ANY COVERED CODE IS AUTHORIZED HEREUNDER EXCEPT UNDER THIS DISCLAIMER.
#
# STM32W108xB_Example1.py - blink the LEDs, read a push button switch.
# NOTE that this script runs on the DiZiC MB851 evaluation board. You would
# have to change the pin assignements (below) in order to run it on other hardware.
#
GREEN_LED_PIN = 14
GREEN_LED_OFF = 1
GREEN_LED_ON = 0

YELLOW_LED_PIN = 13
YELLOW_LED_OFF = 1
YELLOW_LED_ON = 0

IR_LED_PIN = 12
IR_LED_OFF = 0
IR_LED_ON = 1

BUTTON_PIN = 7

@setHook(HOOK_STARTUP)
def startup():
    setPinDir(GREEN_LED_PIN, True)
    writePin(GREEN_LED_PIN, GREEN_LED_OFF)

    setPinDir(YELLOW_LED_PIN, True)
    writePin(YELLOW_LED_PIN, YELLOW_LED_OFF)

    setPinDir(IR_LED_PIN, True)
    writePin(IR_LED_PIN, IR_LED_OFF)

    setPinDir(BUTTON_PIN, False)
    setPinPullup(BUTTON_PIN, True)
    monitorPin(BUTTON_PIN, True)

@setHook(HOOK_1S)
def everySecond():
    pulsePin(GREEN_LED_PIN, 250, GREEN_LED_ON)
    pulsePin(IR_LED_PIN, 500, IR_LED_ON)

@setHook(HOOK_GPIN)
def buttonEvent(pin, isSet):
    if pin == BUTTON_PIN:
        if isSet:
            print "released"
            writePin(YELLOW_LED_PIN, YELLOW_LED_OFF)
        else:
            writePin(YELLOW_LED_PIN, YELLOW_LED_ON)
            print "pressed"
