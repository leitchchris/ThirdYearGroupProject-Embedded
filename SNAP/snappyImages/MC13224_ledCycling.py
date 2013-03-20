# Copyright (C) 2011 Synapse Wireless, Inc.
# Subject to your agreement of the disclaimer set forth below, permission is given by Synapse Wireless, Inc. ("Synapse") to you to freely modify, redistribute or include this SNAPpy code in any program. The purpose of this code is to help you understand and learn about SNAPpy by code examples.
# BY USING ALL OR ANY PORTION OF THIS SNAPPY CODE, YOU ACCEPT AND AGREE TO THE BELOW DISCLAIMER. If you do not accept or agree to the below disclaimer, then you may not use, modify, or distribute this SNAPpy code.
# THE CODE IS PROVIDED UNDER THIS LICENSE ON AN "AS IS" BASIS, WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, WITHOUT LIMITATION, WARRANTIES THAT THE COVERED CODE IS FREE OF DEFECTS, MERCHANTABLE, FIT FOR A PARTICULAR PURPOSE OR NON-INFRINGING. THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE COVERED CODE IS WITH YOU. SHOULD ANY COVERED CODE PROVE DEFECTIVE IN ANY RESPECT, YOU (NOT THE INITIAL DEVELOPER OR ANY OTHER CONTRIBUTOR) ASSUME THE COST OF ANY NECESSARY SERVICING, REPAIR OR CORRECTION. UNDER NO CIRCUMSTANCES WILL SYNAPSE BE LIABLE TO YOU, OR ANY OTHER PERSON OR ENTITY, FOR ANY LOSS OF USE, REVENUE OR PROFIT, LOST OR DAMAGED DATA, OR OTHER COMMERCIAL OR ECONOMIC LOSS OR FOR ANY DAMAGES WHATSOEVER RELATED TO YOUR USE OR RELIANCE UPON THE SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGES OR IF SUCH DAMAGES ARE FORESEEABLE. THIS DISCLAIMER OF WARRANTY AND LIABILITY CONSTITUTES AN ESSENTIAL PART OF THIS LICENSE. NO USE OF ANY COVERED CODE IS AUTHORIZED HEREUNDER EXCEPT UNDER THIS DISCLAIMER.

"""
One example of using MC13224_PWM.py
This demo uses Pulse Width Modulation (PWM) to vary the brightness of an
LED connected to IO 8 AKA TIO0 (TMR 0's IO pin) on the MC13224 chip (or
on a module based on that chip, such as the Synapse SM700).

Two other pins support PWM as well, look at routine setTMR() below...
"""

TMR = 0 # choices are 0/1/2 to use IO 8/9/10 AKA TIO0/TIO1/TIO2
# Timer 3 is not available for PWM because it is providing the 1 millisecond "tick"

from synapse.MC13224_PWM import *

# You can change these in the script, or on-the-fly with the
# "setXXX" routines below.
ledMinValue = 0
ledMaxValue = 10000
ledStep = 250
ledValue = 0

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
    """Change the current pulse width value"""
    global ledValue
    ledValue = value

@setHook(HOOK_STARTUP)
def startupEvent():
    # Using divisorCode 0 (24 MHZ/1) to get finest granularity
    initPWM(TMR, 0, ledMaxValue-ledValue, ledValue, False)

@setHook(HOOK_100MS)
def timer100msEvent(currentMs):
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
    setSplit(TMR, ledMaxValue, ledValue)

def setTMR(val):
    """Change the TMR pin (0-2) being PWM'd on the fly"""
    global TMR
    if val < 0:
        return
    if val > 2:
        return
    TMR = val
    startupEvent()
