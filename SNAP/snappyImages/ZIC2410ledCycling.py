# Copyright (C) 2011 Synapse Wireless, Inc.
# Subject to your agreement of the disclaimer set forth below, permission is given by Synapse Wireless, Inc. ("Synapse") to you to freely modify, redistribute or include this SNAPpy code in any program. The purpose of this code is to help you understand and learn about SNAPpy by code examples.
# BY USING ALL OR ANY PORTION OF THIS SNAPPY CODE, YOU ACCEPT AND AGREE TO THE BELOW DISCLAIMER. If you do not accept or agree to the below disclaimer, then you may not use, modify, or distribute this SNAPpy code.
# THE CODE IS PROVIDED UNDER THIS LICENSE ON AN "AS IS" BASIS, WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, WITHOUT LIMITATION, WARRANTIES THAT THE COVERED CODE IS FREE OF DEFECTS, MERCHANTABLE, FIT FOR A PARTICULAR PURPOSE OR NON-INFRINGING. THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE COVERED CODE IS WITH YOU. SHOULD ANY COVERED CODE PROVE DEFECTIVE IN ANY RESPECT, YOU (NOT THE INITIAL DEVELOPER OR ANY OTHER CONTRIBUTOR) ASSUME THE COST OF ANY NECESSARY SERVICING, REPAIR OR CORRECTION. UNDER NO CIRCUMSTANCES WILL SYNAPSE BE LIABLE TO YOU, OR ANY OTHER PERSON OR ENTITY, FOR ANY LOSS OF USE, REVENUE OR PROFIT, LOST OR DAMAGED DATA, OR OTHER COMMERCIAL OR ECONOMIC LOSS OR FOR ANY DAMAGES WHATSOEVER RELATED TO YOUR USE OR RELIANCE UPON THE SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGES OR IF SUCH DAMAGES ARE FORESEEABLE. THIS DISCLAIMER OF WARRANTY AND LIABILITY CONSTITUTES AN ESSENTIAL PART OF THIS LICENSE. NO USE OF ANY COVERED CODE IS AUTHORIZED HEREUNDER EXCEPT UNDER THIS DISCLAIMER.

"""
One example of using ZIC2410_PWM.py
This demo uses Pulse Width Modulation (PWM) to vary the brightness
of two LEDs connected to port pins P3.6 and P3.7.
Note that such LEDs are NOT built-in to the CEL EVB1/2/3 boards.
(You will have to hook up your won LEDs to see this demo in action)
"""

from synapse.ZIC2410_PWM import *

# You can change these in the script, or on-the-fly with the
# multiple "setXXX" routines below.
led1MinValue = 0
led1MaxValue = 255
led1Step = 20
led1Value = 0

led2MinValue = 0
led2MaxValue = 255
led2Step = 40
led2Value = 0

def setMin1(value):
    """Change the minimum pulse width"""
    global led1MinValue
    led1MinValue = value

def setMax1(value):
    """Change the maximum pulse width for the PWM2 LED"""
    global led1MaxValue
    led1MaxValue = value

def setStep1(value):
    """Change the pulse width delta value for the PWM2 LED"""
    global led1Step
    led1Step = value

def setValue1(value):
    """Change the current pulse width value for the PWM2 LED"""
    global led1Value
    led1Value = value

def setMin2(value):
    """Change the minimum pulse width for the PWM2 LED"""
    global led2MinValue
    led2MinValue = value

def setMax2(value):
    """Change the maximum pulse width for the PWM3 LED"""
    global led2MaxValue
    led2MaxValue = value

def setStep2(value):
    """Change the pulse width delta value for the PWM3 LED"""
    global led2Step
    led2Step = value

def setValue2(value):
    """Change the current pulse width value for the PWM3 LED"""
    global led2Value
    led2Value = value

@setHook(HOOK_STARTUP)
def startupEvent():
    setPinDir(PWM2_PIN, True)
    setPwm(PWM2_PIN, 400, led1MaxValue)

    setPinDir(PWM3_PIN, True)
    setPwm(PWM3_PIN, 400, led2MaxValue)

@setHook(HOOK_100MS)
def timer100msEvent(currentMs):
    global led1Step, led1Value, led2Step, led2Value

    led1Value += led1Step
    if led1Step > 0:
        if led1Value >= led1MaxValue:
            led1Value = led1MaxValue
            led1Step = -led1Step
    else:
        if led1Value <= led1MinValue:
            led1Value = led1MinValue
            led1Step = -led1Step
    setDutyCycle(PWM2_PIN, led1Value)

    led2Value += led2Step
    if led2Step > 0:
        if led2Value >= led2MaxValue:
            led2Value = led2MaxValue
            led2Step = -led2Step
    else:
        if led2Value <= led2MinValue:
            led2Value = led2MinValue
            led2Step = -led2Step
    setDutyCycle(PWM3_PIN, led2Value)
