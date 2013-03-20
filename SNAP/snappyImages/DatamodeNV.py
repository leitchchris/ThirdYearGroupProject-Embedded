# Copyright (C) 2011 Synapse Wireless, Inc.
# Subject to your agreement of the disclaimer set forth below, permission is given by Synapse Wireless, Inc. ("Synapse") to you to freely modify, redistribute or include this SNAPpy code in any program. The purpose of this code is to help you understand and learn about SNAPpy by code examples.
# BY USING ALL OR ANY PORTION OF THIS SNAPPY CODE, YOU ACCEPT AND AGREE TO THE BELOW DISCLAIMER. If you do not accept or agree to the below disclaimer, then you may not use, modify, or distribute this SNAPpy code.
# THE CODE IS PROVIDED UNDER THIS LICENSE ON AN "AS IS" BASIS, WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, WITHOUT LIMITATION, WARRANTIES THAT THE COVERED CODE IS FREE OF DEFECTS, MERCHANTABLE, FIT FOR A PARTICULAR PURPOSE OR NON-INFRINGING. THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE COVERED CODE IS WITH YOU. SHOULD ANY COVERED CODE PROVE DEFECTIVE IN ANY RESPECT, YOU (NOT THE INITIAL DEVELOPER OR ANY OTHER CONTRIBUTOR) ASSUME THE COST OF ANY NECESSARY SERVICING, REPAIR OR CORRECTION. UNDER NO CIRCUMSTANCES WILL SYNAPSE BE LIABLE TO YOU, OR ANY OTHER PERSON OR ENTITY, FOR ANY LOSS OF USE, REVENUE OR PROFIT, LOST OR DAMAGED DATA, OR OTHER COMMERCIAL OR ECONOMIC LOSS OR FOR ANY DAMAGES WHATSOEVER RELATED TO YOUR USE OR RELIANCE UPON THE SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGES OR IF SUCH DAMAGES ARE FORESEEABLE. THIS DISCLAIMER OF WARRANTY AND LIABILITY CONSTITUTES AN ESSENTIAL PART OF THIS LICENSE. NO USE OF ANY COVERED CODE IS AUTHORIZED HEREUNDER EXCEPT UNDER THIS DISCLAIMER.

"""
Example of using two SNAP wireless nodes to replace a RS-232 cable
After loading this script into a SNAP node, invoke the setOtherNode(address)
function (contained within this script) so that each node gets told "who his
counterpart node is". You only have to do this once (the value will be preserved
across power outages and reboots) but you DO have to tell BOTH nodes who their
counterparts are!
The otherNodeAddr value will be saved as NV Parameter 254, change this if needed.
Legal ID numbers for USER NV Params range from 128-254.
Node addresses are the last three bytes of the MAC Address
MAC Addresses can be read off of the RF Engine sticker
For example, a node with MAC Address 001C2C1E 86001B67 is address 001B67
In SNAPpy format this would be address "\x00\x1B\x67"
"""
from synapse.switchboard import *
OTHER_NODE_ADDR_ID = 254

@setHook(HOOK_STARTUP)
def startupEvent():
    """System startup code, invoked automatically (do not call this manually)"""
    global otherNodeAddr
    initUart(1, 9600) # <= put your desired baudrate here!
    flowControl(1, False) # <= set flow control to True or False as needed
    crossConnect(DS_UART1, DS_TRANSPARENT)
    otherNodeAddr = loadNvParam(OTHER_NODE_ADDR_ID)
    ucastSerial(otherNodeAddr)
    
def setOtherNode(address):
    """Call this at least once, and specify the OTHER node's address"""
    global otherNodeAddr
    otherNodeAddr = address
    saveNvParam(OTHER_NODE_ADDR_ID, otherNodeAddr)
    ucastSerial(otherNodeAddr)
    
    
    
    