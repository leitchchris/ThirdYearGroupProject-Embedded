# Copyright (C) 2011 Synapse Wireless, Inc.
# Subject to your agreement of the disclaimer set forth below, permission is given by Synapse Wireless, Inc. ("Synapse") to you to freely modify, redistribute or include this SNAPpy code in any program. The purpose of this code is to help you understand and learn about SNAPpy by code examples.
# BY USING ALL OR ANY PORTION OF THIS SNAPPY CODE, YOU ACCEPT AND AGREE TO THE BELOW DISCLAIMER. If you do not accept or agree to the below disclaimer, then you may not use, modify, or distribute this SNAPpy code.
# THE CODE IS PROVIDED UNDER THIS LICENSE ON AN "AS IS" BASIS, WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, WITHOUT LIMITATION, WARRANTIES THAT THE COVERED CODE IS FREE OF DEFECTS, MERCHANTABLE, FIT FOR A PARTICULAR PURPOSE OR NON-INFRINGING. THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE COVERED CODE IS WITH YOU. SHOULD ANY COVERED CODE PROVE DEFECTIVE IN ANY RESPECT, YOU (NOT THE INITIAL DEVELOPER OR ANY OTHER CONTRIBUTOR) ASSUME THE COST OF ANY NECESSARY SERVICING, REPAIR OR CORRECTION. UNDER NO CIRCUMSTANCES WILL SYNAPSE BE LIABLE TO YOU, OR ANY OTHER PERSON OR ENTITY, FOR ANY LOSS OF USE, REVENUE OR PROFIT, LOST OR DAMAGED DATA, OR OTHER COMMERCIAL OR ECONOMIC LOSS OR FOR ANY DAMAGES WHATSOEVER RELATED TO YOUR USE OR RELIANCE UPON THE SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGES OR IF SUCH DAMAGES ARE FORESEEABLE. THIS DISCLAIMER OF WARRANTY AND LIABILITY CONSTITUTES AN ESSENTIAL PART OF THIS LICENSE. NO USE OF ANY COVERED CODE IS AUTHORIZED HEREUNDER EXCEPT UNDER THIS DISCLAIMER.

"""
BatteryMonitor.py - Uses an external reference circuit to monitor battery power

Requires 1 chip and 1 10K resistor

Wiring:

GPIO 12 - Digital output, used to power the external circuit
If you care more about keeping IO pins than current draw,
power the circuit from one of the VCC connectors instead.

GPIO 11 AKA ADC(7) - used in ADC mode to read the battery level
"""
#
# Analog Devices ADR510
# Digi-Key # ADR510ARTZ-REEL7CT-ND
# 
#                              ________
# GPOUT >---/\/\/\/-----O-----|        |---------O GND
#             10K       |   1 | ADR510 | 2
#                       |     |________|
# ADC IN <--------------          3(nc)
#
# ( current draw when active is 150-250 uA )
#
# GPOUT may be driven high just during measurement to conserve power,
# or instead connect straight to Vcc to save an IO pin.
#
#Since Vref is 1.0V, the calculation is very straightforward.
#
#Vcc = 1024 / readAdc(7)
#

from synapse.platforms import *

OUTPUT_PIN = GPIO_12 # chosen because it was next to GPIO 11
ADC_PIN = GPIO_11 # chosen because it was the ADC pin closest to the corner
ADC_CHAN = 7

secondCounter = 0

@setHook(HOOK_STARTUP)
def startupEvent():
    setPinDir(ADC_PIN, False) # NOT an output
    setPinDir(OUTPUT_PIN, True) # IS an output
    writePin(OUTPUT_PIN, True) # default to powering the circuit

def powerUpVoltageMonitor():
    """Power up the voltage monitoring circuit"""
    writePin(OUTPUT_PIN, True)

def powerDownVoltageMonitor():
    """Power down the circuit. Reported values are bogus"""
    writePin(OUTPUT_PIN, False)

def readBattery():
    """returns battery voltage in .1 volt increments, assuming circuit is powered"""
    refAdc = readAdc(ADC_CHAN)
    battery = (10240 / refAdc) + 1 # + 1 to compensate for truncation effects
    return battery

@setHook(HOOK_100MS)
def tickEvent(currentMs):
    global secondCounter
    secondCounter += 1
    if secondCounter >= 10:
        secondCounter = 0
        batteryX10 = readBattery()
        print 'battery=',batteryX10 / 10,'.',batteryX10 % 10
