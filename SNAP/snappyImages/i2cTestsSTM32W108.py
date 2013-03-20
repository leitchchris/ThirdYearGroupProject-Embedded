# Copyright (C) 2011 Synapse Wireless, Inc.
# Subject to your agreement of the disclaimer set forth below, permission is given by Synapse Wireless, Inc. ("Synapse") to you to freely modify, redistribute or include this SNAPpy code in any program. The purpose of this code is to help you understand and learn about SNAPpy by code examples.
# BY USING ALL OR ANY PORTION OF THIS SNAPPY CODE, YOU ACCEPT AND AGREE TO THE BELOW DISCLAIMER. If you do not accept or agree to the below disclaimer, then you may not use, modify, or distribute this SNAPpy code.
# THE CODE IS PROVIDED UNDER THIS LICENSE ON AN "AS IS" BASIS, WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, WITHOUT LIMITATION, WARRANTIES THAT THE COVERED CODE IS FREE OF DEFECTS, MERCHANTABLE, FIT FOR A PARTICULAR PURPOSE OR NON-INFRINGING. THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE COVERED CODE IS WITH YOU. SHOULD ANY COVERED CODE PROVE DEFECTIVE IN ANY RESPECT, YOU (NOT THE INITIAL DEVELOPER OR ANY OTHER CONTRIBUTOR) ASSUME THE COST OF ANY NECESSARY SERVICING, REPAIR OR CORRECTION. UNDER NO CIRCUMSTANCES WILL SYNAPSE BE LIABLE TO YOU, OR ANY OTHER PERSON OR ENTITY, FOR ANY LOSS OF USE, REVENUE OR PROFIT, LOST OR DAMAGED DATA, OR OTHER COMMERCIAL OR ECONOMIC LOSS OR FOR ANY DAMAGES WHATSOEVER RELATED TO YOUR USE OR RELIANCE UPON THE SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGES OR IF SUCH DAMAGES ARE FORESEEABLE. THIS DISCLAIMER OF WARRANTY AND LIABILITY CONSTITUTES AN ESSENTIAL PART OF THIS LICENSE. NO USE OF ANY COVERED CODE IS AUTHORIZED HEREUNDER EXCEPT UNDER THIS DISCLAIMER.

"""
I2C test/demo routines. The chip specific stuff has been split out
into separate files, see M41T81.py, CAT24C128.py and LIS302DL.py.
"""

retries = 1 # It's possible this might need to be increased for really slow devices

from synapse.platforms import *
from synapse.hexSupport import *
from synapse.M41T81 import *    # Example Real Time Clock (RTC) chip
from synapse.CAT24C128 import * # Example Serial EEPROM chip
from synapse.LIS302DL import * # Example MEMS Accelerometer chip
from synapse.switchboard import *

def status():
    status = getI2cResult()
    print "status=",status

def init():
    # Go ahead and redirect STDOUT to Portal now
    ucastSerial("\x00\x00\x01") # put your correct Portal address here!
    crossConnect(DS_STDIO,DS_TRANSPARENT)

    #i2cInit(False) # This is equivalent to the next line
    i2cInit(False, 2, 1) # MEMS chip has internal pullups

def write(str):
    bytesWritten = i2cWrite(str,retries,False)
    print bytesWritten," bytes written"

def read(str):
    response = i2cRead(str,20,retries,False)
    print len(response),response

def testReadEEPROM(chipAddress, memoryAddress, dataLen):
    result = readEEPROM(chipAddress, memoryAddress, dataLen)
    dumpHex(result)

@setHook(HOOK_STARTUP)
def startupEvent():
    init()
