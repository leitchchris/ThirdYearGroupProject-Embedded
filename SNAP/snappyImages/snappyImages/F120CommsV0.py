"""
/********************************************************************
  Author			: Frank Greig  
  Last Modified 	: 29th December 2012	       Created  :  29th December 2012
  File			    : F120CommsV0.py
  Target Hardware	: Synapse Wireless - RF100 
  Firmware Version	: 2.4.19
  Version		    : 1.0.0
  Description	: Basically an I2c bus test for comms to an F120 MCU. 
  Requires:
            RF100 module connected to the C8051F120 expansion port. 
            RF100 is the bus master and the F120 is the slave device - addresss - 0xF0
            GPIO 17 [RFET pin # 19] [SDA] & GPIO 18 [RFET pin # 20] [SCL]
            
                      
Working Status:         Ok - single byte read and writes are functioning.
                        To be tested  - multi-byte read and writes.

*******************************************************************************/
 """

# Use Synapse Evaluation Board definitions
from RF100 import *

# -------------  Global Constants  -----------------------------------
portalAddr = '\x00\x00\x01'     # hard-coded address for Portal <------------<<<<<<<<
F120_ADDRESS = 0xF0             # slave address for the C8051F120
retries = 1

# -------------  Global variables  -----------------------------------
count = 0
numerrors = 0
 
# Startup Hook
#--------------------    
@setHook(HOOK_STARTUP)
def start():
    i2cInit(False)                        #  Initialise I2C - no pullups
    
@setHook(HOOK_1S)                 # Update date and time every one second
def I2CBusTests():
    global count,numerrors
  
   # writeByte(count)                
    
    dataval = readByte();
    if dataval !=count: 
        numerrors +=1
    eventString = "f120 data >>  " + str(dataval) + "    num errors >>  " + str(numerrors)   
    rpc(portalAddr, "logEvent", eventString)
    
    count +=1 
    if dataval == 255: 
        dataval = 0
        count = 0
      

def readByte():    # read a single byte from slave device 
    cmd = ""
    cmd = chr( F120_ADDRESS | 1 )
    resultStr = i2cRead(cmd, 1, retries, False)
    
    result = ord( resultStr[0] )
    return result

def writeByte(value):     # write a single byte to slave device 
    cmd = ""
    cmd = chr(F120_ADDRESS)
    cmd += chr(value)
    i2cWrite(cmd, retries, False)
  
         
def readBytes(numBytes):     # read a string of bytes from the slave  - to be tested!
    cmd = ""
    cmd = chr( F120_ADDRESS | 1 )
    result = i2cRead(cmd, numBytes, retries, False) 
             
    return result

