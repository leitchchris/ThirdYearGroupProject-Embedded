# Copyright (C) 2011 Synapse Wireless, Inc.
# Subject to your agreement of the disclaimer set forth below, permission is given by Synapse Wireless, Inc. ("Synapse") to you to freely modify, redistribute or include this SNAPpy code in any program. The purpose of this code is to help you understand and learn about SNAPpy by code examples.
# BY USING ALL OR ANY PORTION OF THIS SNAPPY CODE, YOU ACCEPT AND AGREE TO THE BELOW DISCLAIMER. If you do not accept or agree to the below disclaimer, then you may not use, modify, or distribute this SNAPpy code.
# THE CODE IS PROVIDED UNDER THIS LICENSE ON AN "AS IS" BASIS, WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, WITHOUT LIMITATION, WARRANTIES THAT THE COVERED CODE IS FREE OF DEFECTS, MERCHANTABLE, FIT FOR A PARTICULAR PURPOSE OR NON-INFRINGING. THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE COVERED CODE IS WITH YOU. SHOULD ANY COVERED CODE PROVE DEFECTIVE IN ANY RESPECT, YOU (NOT THE INITIAL DEVELOPER OR ANY OTHER CONTRIBUTOR) ASSUME THE COST OF ANY NECESSARY SERVICING, REPAIR OR CORRECTION. UNDER NO CIRCUMSTANCES WILL SYNAPSE BE LIABLE TO YOU, OR ANY OTHER PERSON OR ENTITY, FOR ANY LOSS OF USE, REVENUE OR PROFIT, LOST OR DAMAGED DATA, OR OTHER COMMERCIAL OR ECONOMIC LOSS OR FOR ANY DAMAGES WHATSOEVER RELATED TO YOUR USE OR RELIANCE UPON THE SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGES OR IF SUCH DAMAGES ARE FORESEEABLE. THIS DISCLAIMER OF WARRANTY AND LIABILITY CONSTITUTES AN ESSENTIAL PART OF THIS LICENSE. NO USE OF ANY COVERED CODE IS AUTHORIZED HEREUNDER EXCEPT UNDER THIS DISCLAIMER.

"""
  Temperature Alarm Demo for EK2100 (for use on SNAPstick)

    This Snappy script is used on the SNAPstick module and accompanies
    the Temperature Alarm script running on a proto-board.

    To be run on: SNAPstick only
"""

# Use Synapse Evaluation Board definitions
from synapse.evalBase import *

@setHook(HOOK_STARTUP)
def startupEvent():
    """This is hooked into the HOOK_STARTUP event"""
    global secondCounter, alarmArmed
    secondCounter = 0
    alarmArmed = False # Do not strobe the LEDs by default  
    initStickHw()

def doEveryHalfSecond():
    """Things to be done every half-second""" 
    global alarmArmed
    if alarmArmed:
        #print "pulse the red and green pins"
        pulsePin(LED_PIN, 300, False)      
        pulsePin(STICK_LED_GRN_PIN, 100, False)     

@setHook(HOOK_100MS)
def timer100msEvent(currentMs):
    """Hooked into the HOOK_100MS event. Called every 100ms"""
    global secondCounter
    secondCounter += 1
    if secondCounter >= 5:
        doEveryHalfSecond()
        secondCounter = 0

def beginCountdown():
    """The alarm has been triggered; For the SNAPstick it means 'display the alarm LEDs'"""    
    global alarmArmed
    alarmArmed = True

def alarmCutOffRequested():  
    """This function actually disables the local alarm indicator; came from the buzzer unit"""
    global alarmArmed
    alarmArmed = False

def alarmCutOff():  
    """This function will inform the buzzer unit of an alarmCut0ff request"""
    mcastRpc(1,2,"alarmCutOff")

def soundTheAlarm():
    """The alarm has occurred; For the SNAPstick it means 'turn off the LED'"""
    global alarmArmed
    alarmArmed = False
