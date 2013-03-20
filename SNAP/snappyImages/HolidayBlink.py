# Copyright (C) 2011 Synapse Wireless, Inc.
# Subject to your agreement of the disclaimer set forth below, permission is given by Synapse Wireless, Inc. ("Synapse") to you to freely modify, redistribute or include this SNAPpy code in any program. The purpose of this code is to help you understand and learn about SNAPpy by code examples.
# BY USING ALL OR ANY PORTION OF THIS SNAPPY CODE, YOU ACCEPT AND AGREE TO THE BELOW DISCLAIMER. If you do not accept or agree to the below disclaimer, then you may not use, modify, or distribute this SNAPpy code.
# THE CODE IS PROVIDED UNDER THIS LICENSE ON AN "AS IS" BASIS, WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, WITHOUT LIMITATION, WARRANTIES THAT THE COVERED CODE IS FREE OF DEFECTS, MERCHANTABLE, FIT FOR A PARTICULAR PURPOSE OR NON-INFRINGING. THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE COVERED CODE IS WITH YOU. SHOULD ANY COVERED CODE PROVE DEFECTIVE IN ANY RESPECT, YOU (NOT THE INITIAL DEVELOPER OR ANY OTHER CONTRIBUTOR) ASSUME THE COST OF ANY NECESSARY SERVICING, REPAIR OR CORRECTION. UNDER NO CIRCUMSTANCES WILL SYNAPSE BE LIABLE TO YOU, OR ANY OTHER PERSON OR ENTITY, FOR ANY LOSS OF USE, REVENUE OR PROFIT, LOST OR DAMAGED DATA, OR OTHER COMMERCIAL OR ECONOMIC LOSS OR FOR ANY DAMAGES WHATSOEVER RELATED TO YOUR USE OR RELIANCE UPON THE SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGES OR IF SUCH DAMAGES ARE FORESEEABLE. THIS DISCLAIMER OF WARRANTY AND LIABILITY CONSTITUTES AN ESSENTIAL PART OF THIS LICENSE. NO USE OF ANY COVERED CODE IS AUTHORIZED HEREUNDER EXCEPT UNDER THIS DISCLAIMER.

"""
  Holiday Light Show Demo for EK2100 Kit (for use on SNAP Stick 100)

    This Snappy script demonstrates how information gathered from 
    sensors onboard a SNAP node can be communicated to other 
    nodes and used to initiate other tasks.
    
    To be run on the SNAP Stick 100 only
    
"""

# Use Synapse Evaluation Board definitions
from synapse.evalBase import *

#Globals
secondCounter = 0
redLEDPin = GPIO_0
greenLEDPin = GPIO_1   
itsChristmas = False 
itsHalloween = False

@setHook(HOOK_STARTUP)
def startupEvent():
    """This is hooked into the HOOK_STARTUP event"""
    # set the LED pins to be 'outputs'  
    setPinDir(redLEDPin, True)
    setPinDir(greenLEDPin, True)  
    
def doEverySecond():
    """Things to be done every second""" 
    if itsChristmas:
        #print "pulse the Christmas pins"
        pulsePin(redLEDPin, 1000, False) 
    if itsHalloween:
        #print "pulse the Halloween pins"
        pulsePin(redLEDPin, 200, False)      
        pulsePin(greenLEDPin, 200, False)     

@setHook(HOOK_100MS)
def timer100msEvent(currentMs):
    """Hooked into the HOOK_100MS event. Called every 100ms"""
    global secondCounter
    secondCounter += 1
    if secondCounter >= 10:
        doEverySecond()
        secondCounter = 0
      
def christmasBlink():
    """Light the red and green LEDs"""
    global itsChristmas, itsHalloween
    itsHalloween = False
    itsChristmas = True
  
def halloweenBlink():
    """Light the red and amber LEDs"""
    global itsChristmas, itsHalloween
    itsHalloween = True
    itsChristmas = False
  
def disableLEDs():
    """Turn off the LEDs"""
    global itsChristmas, itsHalloween
    itsHalloween = False
    itsChristmas = False

