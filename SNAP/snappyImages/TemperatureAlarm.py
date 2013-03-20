# Copyright (C) 2011 Synapse Wireless, Inc.
# Subject to your agreement of the disclaimer set forth below, permission is given by Synapse Wireless, Inc. ("Synapse") to you to freely modify, redistribute or include this SNAPpy code in any program. The purpose of this code is to help you understand and learn about SNAPpy by code examples.
# BY USING ALL OR ANY PORTION OF THIS SNAPPY CODE, YOU ACCEPT AND AGREE TO THE BELOW DISCLAIMER. If you do not accept or agree to the below disclaimer, then you may not use, modify, or distribute this SNAPpy code.
# THE CODE IS PROVIDED UNDER THIS LICENSE ON AN "AS IS" BASIS, WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, WITHOUT LIMITATION, WARRANTIES THAT THE COVERED CODE IS FREE OF DEFECTS, MERCHANTABLE, FIT FOR A PARTICULAR PURPOSE OR NON-INFRINGING. THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE COVERED CODE IS WITH YOU. SHOULD ANY COVERED CODE PROVE DEFECTIVE IN ANY RESPECT, YOU (NOT THE INITIAL DEVELOPER OR ANY OTHER CONTRIBUTOR) ASSUME THE COST OF ANY NECESSARY SERVICING, REPAIR OR CORRECTION. UNDER NO CIRCUMSTANCES WILL SYNAPSE BE LIABLE TO YOU, OR ANY OTHER PERSON OR ENTITY, FOR ANY LOSS OF USE, REVENUE OR PROFIT, LOST OR DAMAGED DATA, OR OTHER COMMERCIAL OR ECONOMIC LOSS OR FOR ANY DAMAGES WHATSOEVER RELATED TO YOUR USE OR RELIANCE UPON THE SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGES OR IF SUCH DAMAGES ARE FORESEEABLE. THIS DISCLAIMER OF WARRANTY AND LIABILITY CONSTITUTES AN ESSENTIAL PART OF THIS LICENSE. NO USE OF ANY COVERED CODE IS AUTHORIZED HEREUNDER EXCEPT UNDER THIS DISCLAIMER.

"""
  Temperature Alarm Demo for EK2100 (for use on proto-board)

    This Snappy script is used on the proto-board module and accompanies
    the Temperature Alarm script running on a SNAPstick.
    It will monitor for a temperature threshold and begin a timer once
    triggered. The alarm will sound if the cut-off is not executed before 
    the timer expires.

    To be run on: proto-board only
    
    Hardware Requirements:  Thermistor
                            Pull-up resistor
                            Buzzer

"""

# Use Synapse Evaluation Board definitions
from synapse.evalBase import *

secondCounter = 0
greenLedPin = GPIO_1
buzzerPin = GPIO_9
adcThreshold = 425 # Default to a little hotter than room temp. User can change this on the fly (higher is colder)

@setHook(HOOK_STARTUP)
def startupEvent():
    """This is hooked into the HOOK_STARTUP event"""
    initProtoHw()
    monitorPin(BUTTON_PIN, True) # Monitor for button-press events
    # Setup the buzzer 
    setPinDir(buzzerPin, True)
    writePin(buzzerPin, False)

def setThreshold(newThreshold):
    """Change the threshold at which the alarm sounds (higher is colder)"""
    global adcThreshold
    adcThreshold = newThreshold

def sensorUpdate():
    """Read the temperature from the sensor"""
    global adcThreshold 
    adcValue = readAdc(0) # Check the temperature
    print "Raw ADC value: ", adcValue #DEBUG
 
    if adcValue < adcThreshold: # If temp is over the limit (below the raw value)..., 
        beginCountdown() #...start the countdown to the alarm

def soundTheAlarm():
    """Activate the buzzer"""
    global countdown, buzzerPin
    print "Sound the Alarm" #DEBUG
    countdown = False
    writePin(greenLedPin, False) # Turn off the green LED
    mcastRpc(1,2,"soundTheAlarm")
    pulsePin(buzzerPin, 1500, True)

def beginCountdown():
    """Begin a 5 second countdown that will lead to the alarm sounding"""
    global countdown, alarmCounter, greenLedPin
    if not countdown: # Don't restart things if it has already triggered
        print "Begin Countdown" #DEBUG
        blinkLed(1000) # Flash yellow LED
        writePin(greenLedPin, True) # Light the green LED
        mcastRpc(1,2,"beginCountdown") # Tell any  other nodes
        countdown = True
        alarmCounter = 0
    
def alarmCutOff():
    """Disable the alarm before it goes off"""
    global countdown, alarmCounter
    writePin(greenLedPin, False) # Turn off the green LED    

    # Report to remote nodes that that the buzzer unit has seen the alarmCutOff
    mcastRpc(1,2,"alarmCutOffRequested")
    
    pulsePin(buzzerPin, 20, True) # Chirp the local buzzer
    countdown = False
    alarmCounter = 0

def doEverySecond():
    """Things to be done every second"""    
    global alarmCounter, countdown
    blinkLed(200)
    sensorUpdate()
    if countdown:
        alarmCounter += 1
        print "Alarm Count= ", alarmCounter #DEBUG
        if alarmCounter >= 5:
            soundTheAlarm()

@setHook(HOOK_100MS)
def timer100msEvent(msTick):
    """Hooked into the HOOK_100MS event"""
    global secondCounter
    secondCounter += 1
    if secondCounter >= 10:
        doEverySecond()      
        secondCounter = 0
    
@setHook(HOOK_GPIN)
def buttonEvent(pinNum, isSet):
    """Hooked into the HOOK_GPIN event. Configured to shut off the alarm"""
    if pinNum == BUTTON_PIN:
        if not isSet:
            alarmCutOff()

