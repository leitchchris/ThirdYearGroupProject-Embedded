# Copyright (C) 2011 Synapse Wireless, Inc.
# Subject to your agreement of the disclaimer set forth below, permission is given by Synapse Wireless, Inc. ("Synapse") to you to freely modify, redistribute or include this SNAPpy code in any program. The purpose of this code is to help you understand and learn about SNAPpy by code examples.
# BY USING ALL OR ANY PORTION OF THIS SNAPPY CODE, YOU ACCEPT AND AGREE TO THE BELOW DISCLAIMER. If you do not accept or agree to the below disclaimer, then you may not use, modify, or distribute this SNAPpy code.
# THE CODE IS PROVIDED UNDER THIS LICENSE ON AN "AS IS" BASIS, WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, WITHOUT LIMITATION, WARRANTIES THAT THE COVERED CODE IS FREE OF DEFECTS, MERCHANTABLE, FIT FOR A PARTICULAR PURPOSE OR NON-INFRINGING. THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE COVERED CODE IS WITH YOU. SHOULD ANY COVERED CODE PROVE DEFECTIVE IN ANY RESPECT, YOU (NOT THE INITIAL DEVELOPER OR ANY OTHER CONTRIBUTOR) ASSUME THE COST OF ANY NECESSARY SERVICING, REPAIR OR CORRECTION. UNDER NO CIRCUMSTANCES WILL SYNAPSE BE LIABLE TO YOU, OR ANY OTHER PERSON OR ENTITY, FOR ANY LOSS OF USE, REVENUE OR PROFIT, LOST OR DAMAGED DATA, OR OTHER COMMERCIAL OR ECONOMIC LOSS OR FOR ANY DAMAGES WHATSOEVER RELATED TO YOUR USE OR RELIANCE UPON THE SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGES OR IF SUCH DAMAGES ARE FORESEEABLE. THIS DISCLAIMER OF WARRANTY AND LIABILITY CONSTITUTES AN ESSENTIAL PART OF THIS LICENSE. NO USE OF ANY COVERED CODE IS AUTHORIZED HEREUNDER EXCEPT UNDER THIS DISCLAIMER.

"""
One example of using PWM.py
This demo uses Pulse Width Modulation (PWM) to vary the brightness of the
yellow LED on the SN163 Bridge Demonstration Board and the SN111 End Device
Demonstration Board. To run this demo on a SN171 Proto Board, you would have
to attach your own LED to pin GPIO 0 - the two LEDs built-in to the Proto
Board are on the wrong pins for this example.
"""

from synapse.PWM import *

# You can change these in the script, or on-the-fly with the
# "setXXX" routines below.
ledMinValue = 5
ledMaxValue = 1024
ledStep = 25
ledValue = 5

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
    setTimebaseWord(1, ledMaxValue) # divisorCode 1 = divisor of 2

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
    setDutyCycleWord(True, ledValue)

