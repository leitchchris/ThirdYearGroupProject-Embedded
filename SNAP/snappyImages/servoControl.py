# Copyright (C) 2011 Synapse Wireless, Inc.
# Subject to your agreement of the disclaimer set forth below, permission is given by Synapse Wireless, Inc. ("Synapse") to you to freely modify, redistribute or include this SNAPpy code in any program. The purpose of this code is to help you understand and learn about SNAPpy by code examples.
# BY USING ALL OR ANY PORTION OF THIS SNAPPY CODE, YOU ACCEPT AND AGREE TO THE BELOW DISCLAIMER. If you do not accept or agree to the below disclaimer, then you may not use, modify, or distribute this SNAPpy code.
# THE CODE IS PROVIDED UNDER THIS LICENSE ON AN "AS IS" BASIS, WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, WITHOUT LIMITATION, WARRANTIES THAT THE COVERED CODE IS FREE OF DEFECTS, MERCHANTABLE, FIT FOR A PARTICULAR PURPOSE OR NON-INFRINGING. THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE COVERED CODE IS WITH YOU. SHOULD ANY COVERED CODE PROVE DEFECTIVE IN ANY RESPECT, YOU (NOT THE INITIAL DEVELOPER OR ANY OTHER CONTRIBUTOR) ASSUME THE COST OF ANY NECESSARY SERVICING, REPAIR OR CORRECTION. UNDER NO CIRCUMSTANCES WILL SYNAPSE BE LIABLE TO YOU, OR ANY OTHER PERSON OR ENTITY, FOR ANY LOSS OF USE, REVENUE OR PROFIT, LOST OR DAMAGED DATA, OR OTHER COMMERCIAL OR ECONOMIC LOSS OR FOR ANY DAMAGES WHATSOEVER RELATED TO YOUR USE OR RELIANCE UPON THE SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGES OR IF SUCH DAMAGES ARE FORESEEABLE. THIS DISCLAIMER OF WARRANTY AND LIABILITY CONSTITUTES AN ESSENTIAL PART OF THIS LICENSE. NO USE OF ANY COVERED CODE IS AUTHORIZED HEREUNDER EXCEPT UNDER THIS DISCLAIMER.

"""
One example of using PWM.py
This demo uses Pulse Width Modulation (PWM) to control a servo motor connected
to pin GPIO 0 of a SN171 Proto Board.

For servo control, we need a pulse stream at 50 HZ (1 pulse every 20 milliseconds)
The pulse *width* needs to be varied from 1 millisecond to 2 milliseconds.
NOTE! Your particular servo may need longer and/or shorter pulses to cover its
full range, this example uses the "textbook" timings, see for example
http://www.societyofrobots.com/actuators_servos.shtml
"""

from synapse.PWM import *

# Pre-calculated from:
#    count = desired_period * BUSCLK / divisor
#    with desired Pulse Period = 20 milliseconds, and divisor = 128
MAX_SERVO_TICKS = 3124

@setHook(HOOK_STARTUP)
def startupEvent():
    setTimebaseWord(7, MAX_SERVO_TICKS)
    setPwmPercent(50) # start with the servo motor centered 

def setPwmPercent(percentage):
    """set servo motor position in %0-100"""
    if percentage < 0:
        percentage = 0
    if percentage > 100:
        percentage = 100
    # Map "servo position" (0%-100%) onto "pulse width" (5%-10%)
    low = MAX_SERVO_TICKS / 20  # 5% of 20 ms pulse is 1 ms, /20 = *.05
    high = MAX_SERVO_TICKS / 10 # 10% of 20 ms pulse is 2 ms, /10 = *.1
    diff = high - low
    delta = (diff * percentage) / 100
    width = low + delta
    #print MAX_SERVO_TICKS,' ',low,' ',high,' ',diff,' ',delta,' ',width
    setDutyCycleWord(True, width)