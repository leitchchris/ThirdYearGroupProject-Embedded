# Copyright (C) 2011 Synapse Wireless, Inc.
# Subject to your agreement of the disclaimer set forth below, permission is given by Synapse Wireless, Inc. ("Synapse") to you to freely modify, redistribute or include this SNAPpy code in any program. The purpose of this code is to help you understand and learn about SNAPpy by code examples.
# BY USING ALL OR ANY PORTION OF THIS SNAPPY CODE, YOU ACCEPT AND AGREE TO THE BELOW DISCLAIMER. If you do not accept or agree to the below disclaimer, then you may not use, modify, or distribute this SNAPpy code.
# THE CODE IS PROVIDED UNDER THIS LICENSE ON AN "AS IS" BASIS, WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, WITHOUT LIMITATION, WARRANTIES THAT THE COVERED CODE IS FREE OF DEFECTS, MERCHANTABLE, FIT FOR A PARTICULAR PURPOSE OR NON-INFRINGING. THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE COVERED CODE IS WITH YOU. SHOULD ANY COVERED CODE PROVE DEFECTIVE IN ANY RESPECT, YOU (NOT THE INITIAL DEVELOPER OR ANY OTHER CONTRIBUTOR) ASSUME THE COST OF ANY NECESSARY SERVICING, REPAIR OR CORRECTION. UNDER NO CIRCUMSTANCES WILL SYNAPSE BE LIABLE TO YOU, OR ANY OTHER PERSON OR ENTITY, FOR ANY LOSS OF USE, REVENUE OR PROFIT, LOST OR DAMAGED DATA, OR OTHER COMMERCIAL OR ECONOMIC LOSS OR FOR ANY DAMAGES WHATSOEVER RELATED TO YOUR USE OR RELIANCE UPON THE SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGES OR IF SUCH DAMAGES ARE FORESEEABLE. THIS DISCLAIMER OF WARRANTY AND LIABILITY CONSTITUTES AN ESSENTIAL PART OF THIS LICENSE. NO USE OF ANY COVERED CODE IS AUTHORIZED HEREUNDER EXCEPT UNDER THIS DISCLAIMER.

#
# STM32W108xB_LedCycling.py - an example of controlling the brightness of an LED by
# varying the PWM waveform driving it.
#

from synapse.STM32W108xB_PWM import *

GREEN_LED_PIN = 14 # DiZiC MB851 Evaluation Board
ledPin = GREEN_LED_PIN

# You can change these in the script, or on-the-fly with the "setXXX" routines below.
# In this example, I made it so that duty cycle COUNT and PERCENTAGE mapped 1:1
# That does not have to be the case, you actually have a full 16 bits to play with.
ledMinValue = 0
ledMaxValue = 100
ledStep = 5
ledValue = 50

def setMin(value):
    """Change the minimum pulse width"""
    global ledMinValue
    ledMinValue = value

def setMax(value):
    """Change the maximum pulse width"""
    global ledMaxValue
    ledMaxValue = value

def setStep(value):
    """Change the pulse width delta value"""
    global ledStep
    ledStep = value

def setValue(value):
    """Change the current pulse width value (0-100)"""
    global ledValue
    ledValue = value

@setHook(HOOK_STARTUP)
def startupEvent():
    """Default at startup to cycling the on-board GREEN LED"""
    startCycling(GREEN_LED_PIN)

def startCycling(io):
    """Setup to do LED brightness via PWM on the specified IO"""
    global ledPin
    ledPin = io
    # Prescalar of 10 was experimentally determined to be flicker-free
    # Divisor of 99 was to make dutyCycle map 1:1 to percentage
    pwmInitTimer(ledPin, 10, 99)
    pwmInitChannel(ledPin, ledValue, False)

@setHook(HOOK_100MS)
def timer100msEvent(currentMs):
    """Adjust the LED brightness 10 times a second via PWM"""
    global ledStep, ledValue
    ledValue += ledStep
    if ledStep > 0:
        if ledValue >= ledMaxValue:
            ledValue = ledMaxValue
            ledStep = -ledStep
    else:
        if ledValue <= ledMinValue:
            ledValue = ledMinValue
            ledStep = -ledStep
    pwmSetDutyCycle(ledPin, ledValue)
