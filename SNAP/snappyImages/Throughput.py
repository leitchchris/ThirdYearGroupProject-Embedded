# Copyright (C) 2011 Synapse Wireless, Inc.
# Subject to your agreement of the disclaimer set forth below, permission is given by Synapse Wireless, Inc. ("Synapse") to you to freely modify, redistribute or include this SNAPpy code in any program. The purpose of this code is to help you understand and learn about SNAPpy by code examples.
# BY USING ALL OR ANY PORTION OF THIS SNAPPY CODE, YOU ACCEPT AND AGREE TO THE BELOW DISCLAIMER. If you do not accept or agree to the below disclaimer, then you may not use, modify, or distribute this SNAPpy code.
# THE CODE IS PROVIDED UNDER THIS LICENSE ON AN "AS IS" BASIS, WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, WITHOUT LIMITATION, WARRANTIES THAT THE COVERED CODE IS FREE OF DEFECTS, MERCHANTABLE, FIT FOR A PARTICULAR PURPOSE OR NON-INFRINGING. THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE COVERED CODE IS WITH YOU. SHOULD ANY COVERED CODE PROVE DEFECTIVE IN ANY RESPECT, YOU (NOT THE INITIAL DEVELOPER OR ANY OTHER CONTRIBUTOR) ASSUME THE COST OF ANY NECESSARY SERVICING, REPAIR OR CORRECTION. UNDER NO CIRCUMSTANCES WILL SYNAPSE BE LIABLE TO YOU, OR ANY OTHER PERSON OR ENTITY, FOR ANY LOSS OF USE, REVENUE OR PROFIT, LOST OR DAMAGED DATA, OR OTHER COMMERCIAL OR ECONOMIC LOSS OR FOR ANY DAMAGES WHATSOEVER RELATED TO YOUR USE OR RELIANCE UPON THE SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGES OR IF SUCH DAMAGES ARE FORESEEABLE. THIS DISCLAIMER OF WARRANTY AND LIABILITY CONSTITUTES AN ESSENTIAL PART OF THIS LICENSE. NO USE OF ANY COVERED CODE IS AUTHORIZED HEREUNDER EXCEPT UNDER THIS DISCLAIMER.

"""
Throughput Tester - send or receive packets as fast as possible

This script is made to load on two boards, at least one being a demonstration board
Initially both units will display "--" on the display
Pressing the button on one board will start transmitting broadcast packets and display "On",
to stop sending press the button again
The receiving unit will display the number of packets received "rP".
Pressing the button on the receiving unit will toggle to display dropped packets "dP".
Pressing the button a third time will toggle to display link quality percent "lP".
Holding the button on the receiving unit will tell the sending unit to send unicast pacets "uc".
Holding the button again on the receiving unit will switch the sending unit to send broadcast packets "bc".
"""


from synapse.evalBase import *
from synapse.switchboard import *


seqNum = 0
secondCounter = 0
sending = False
multicast = True
remoteAddr = '\x00\x1b\x5a'
payload = 'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdef'
freezeCounter = 0
rxDisplayState = 0
buttonStateTime = 0
lqSum = 0

@setHook(HOOK_GPIN)
def buttonEvent(pinNum, isSet):
    global sending, buttonState, freezeCounter, rxDisplayState, buttonStateTime

    if pinNum == BUTTON_PIN:
        buttonState = isSet
        if isSet and timeElapsed(buttonStateTime) < 200:
            if not sending and rcvCount == 0:
                #Don't send multicasts out packet serial
                crossConnect(DS_NULL, DS_PACKET_SERIAL)

                sending = True
                onRpcSent()
            elif sending:
                sending = False
            else: # we are a receiver
                freezeCounter = 5 # give them time to read the display mode
                if rxDisplayState == 2:
                    rxDisplayState = 0
                    SetSegments(0x5073) #rP - Received Packets
                elif rxDisplayState == 0:
                    rxDisplayState = 1
                    SetSegments(0x5e73) #dP - Dropped Packets
                else:
                    rxDisplayState = 2
                    SetSegments(0x3873) #LP - Link Percent

            writePin(LED_PIN, sending)
        buttonStateTime = getMs()

def getPercentLq():
    maxDbm = 18
    minDbm = 95
    percent = 100 - ((getLq() - maxDbm) * 100) / (minDbm - maxDbm)
    return percent

@setHook(HOOK_RPC_SENT)
def onRpcSent():
    global seqNum, rcvCount

    if sending:
        seqNum += 1
        if multicast:
            mcastRpc(1, 1, 'rcvPkt', seqNum, payload)
            SetSegments(0x3F54) #On 
        else:
            rpc(remoteAddr, 'rcvPkt', seqNum, payload)
            #display2digits(getPercentLq())
    else:
        #Set to 0 so a number doesn't show on sender
        rcvCount = 0

def rcvPkt(seq, data):
    global dropCntr, seqNum, rcvCount, remoteAddr, lqSum

    nextSeq = seqNum+1
    if seq != (nextSeq):
        dropCntr += (seq-nextSeq)
    seqNum = seq
    rcvCount += 1
    pulsePin(LED_PIN, 100, True)
    remoteAddr = rpcSourceAddr()[:]
    lqSum += getPercentLq()

def sendUnicasts(addr):
    global remoteAddr, multicast

    remoteAddr = addr[:]
    multicast = False

def sendMulticasts():
    global multicast

    multicast = True

@setHook(HOOK_STARTUP)
def startupEvent():
    global buttonState

    # Detect and initialize the hardware (assumes running on an evaluation board)
    detectEvalBoards()
    SetSegments(0x4040) #--

    # Monitor for button-press events
    monitorPin(BUTTON_PIN, True)
    setRate(3)

    # Initialize button-detect variables
    buttonState = readPin(BUTTON_PIN)

@setHook(HOOK_100MS)
def time100MsHook(time):
    global secondCounter, rcvCount, dropCntr, freezeCounter, buttonStateTime, buttonState, multicast, lqSum

    secondCounter += 1
    if secondCounter >= 10:
        secondCounter = 0
        if not sending:
            if freezeCounter == 0:
                if rcvCount != 0:
                    if rxDisplayState == 0:
                        display2digits(rcvCount)
                    elif rxDisplayState == 1:
                        display2digits(dropCntr)
                    else:
                        display2digits(lqSum / rcvCount)
                else:
                    SetSegments(0x4040) #--
                    multicast = True
            rcvCount = 0
            dropCntr = 0
            lqSum = 0

    if freezeCounter > 0:
        freezeCounter -= 1

    if not sending and rcvCount > 0 and not buttonState and timeElapsed(buttonStateTime) >= 1000:
        freezeCounter = 5
        if multicast:
            SetSegments(0x1c58) #uc
            rpc(remoteAddr, 'sendUnicasts', localAddr())
        else:
            SetSegments(0x7c58) #bc
            rpc(remoteAddr, 'sendMulticasts')
        multicast = not multicast
        buttonState = True
        buttonStateTime = time

def timeElapsed(startTime):
    current = getMs()
    if current > startTime:
        delta = current - startTime
    else:
        delta = (0xffff - startTime) + 1 + current
    return delta

def toggleType(addr):
    if sending and multicast:
        sendUnicasts(addr)
    else:
        sendMulticasts()

if platform == 'RF200' or platform == 'RF300' or platform == 'RF301':
    @setHook(HOOK_10MS)
    def every10Ms(tick):
        updateSevenSegmentDisplay()

