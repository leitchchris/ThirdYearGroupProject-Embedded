# Copyright (C) 2011 Synapse Wireless, Inc.
# Subject to your agreement of the disclaimer set forth below, permission is given by Synapse Wireless, Inc. ("Synapse") to you to freely modify, redistribute or include this SNAPpy code in any program. The purpose of this code is to help you understand and learn about SNAPpy by code examples.
# BY USING ALL OR ANY PORTION OF THIS SNAPPY CODE, YOU ACCEPT AND AGREE TO THE BELOW DISCLAIMER. If you do not accept or agree to the below disclaimer, then you may not use, modify, or distribute this SNAPpy code.
# THE CODE IS PROVIDED UNDER THIS LICENSE ON AN "AS IS" BASIS, WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, WITHOUT LIMITATION, WARRANTIES THAT THE COVERED CODE IS FREE OF DEFECTS, MERCHANTABLE, FIT FOR A PARTICULAR PURPOSE OR NON-INFRINGING. THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE COVERED CODE IS WITH YOU. SHOULD ANY COVERED CODE PROVE DEFECTIVE IN ANY RESPECT, YOU (NOT THE INITIAL DEVELOPER OR ANY OTHER CONTRIBUTOR) ASSUME THE COST OF ANY NECESSARY SERVICING, REPAIR OR CORRECTION. UNDER NO CIRCUMSTANCES WILL SYNAPSE BE LIABLE TO YOU, OR ANY OTHER PERSON OR ENTITY, FOR ANY LOSS OF USE, REVENUE OR PROFIT, LOST OR DAMAGED DATA, OR OTHER COMMERCIAL OR ECONOMIC LOSS OR FOR ANY DAMAGES WHATSOEVER RELATED TO YOUR USE OR RELIANCE UPON THE SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGES OR IF SUCH DAMAGES ARE FORESEEABLE. THIS DISCLAIMER OF WARRANTY AND LIABILITY CONSTITUTES AN ESSENTIAL PART OF THIS LICENSE. NO USE OF ANY COVERED CODE IS AUTHORIZED HEREUNDER EXCEPT UNDER THIS DISCLAIMER.

"""Cycle the LEDs on the ZIC2410 "EVB3" Evaluation Board"""

from ZIC2410EVB3 import *

led = 0

@setHook(HOOK_STARTUP)
def start():
    # On an EVB3, LED4 is on the same pin as UART0 RX
    # Shut down UART0 so we can control the pin manually
    initUart(0,0)
    
    # Initialize LED pins as outputs
    setPinDir(LED1, True)
    writePin(LED1, False)
    setPinDir(LED2, True)
    writePin(LED2, False)
    setPinDir(LED3, True)
    writePin(LED3, False)
    setPinDir(LED4, True)
    writePin(LED4, False)

@setHook(HOOK_100MS)
def timer100msEvent(currentMs):
    """On the 100ms tick, increment led count and pulse next LED"""
    global led
    led = (led + 1) % 4
    # On earlier eval boards, the "led" to "LED" mapping was more direct
    if led == 0:
        pulsePin(LED1, 75, True)
    elif led == 1:
        pulsePin(LED2, 75, True)
    elif led == 2:
        pulsePin(LED3, 75, True)
    else:
        pulsePin(LED4, 75, True)

def remoteLQ():
    """As an added bonus, respond to Link Quality Ranger requests too"""
    rpc(rpcSourceAddr(), 'remoteLQ')
