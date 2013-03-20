"""
  Author			: Chris Leitch  
  Last Modified 	: 05 March 2013       Created  :  05 March 2013
  File			    : Test1-GroupProject.py
  Target Hardware	: Synapse Wireless - RF100 
  Firmware Version	: 2.4.19
  Version		    : 1.0.0
  Description	    : A beginning to get remote procedures for sensors 
     
  Requires:
            RF100 module with photsensor ,tilt switch and LEDs
"""

# Use Synapse Evaluation Board definitions
from RF100 import *
from synapse.switchboard import *


# -------------  Global Constants  -----------------------------------
portalAddr   = '\x00\x00\x09'     # hard-coded address for Portal


@setHook(HOOK_STARTUP)
def init():
    """This is hooked into the HOOK_STARTUP event"""  
    
    #initialise the uart
    initUart(1, 57600)
    crossConnect(DS_UART1, DS_STDIO)
    
    #setup for STDIN
    stdinMode(0, False)
    
@setHook(HOOK_STDIN)
def inputFromSerial(dataIn):
    print'INCOMING!'
    print dataIn
    
def outputToSerial():
    print'$$$',
    #print'\r'
    print"open 192.168.0.3 5000"
    #print'\r'
    print"Hello this is a test!"
    #print'\r'
    print'$$$'
    print'close'

