"""
  Author			: Chris Leitch  
  Last Modified 	: 12 April 2013       Created  :  05 March 2013
  File			    : Test1-GroupProject.py
  Target Hardware	: Synapse Wireless - RF100 
  Firmware Version	: 2.4.19
  Version		    : 1.0.0
  Description	    : A working server to snap via wifi hub node
     
  Requires:
            RF100 module with photsensor ,tilt switch and LEDs
"""

# Use Synapse Evaluation Board definitions
from RF100 import *
from synapse.switchboard import *


# -------------  Global Constants  -----------------------------------
portalAddr   = '\x00\x00\x09'     # hard-coded address for Portal

nodeAddr = '\x04\x35\x1D'

@setHook(HOOK_STARTUP)
def init():
    """This is hooked into the HOOK_STARTUP event"""  
    
    #initialise the uart
    initUart(1, 57600)
    crossConnect(DS_STDIO, DS_UART1)
    
    #setup for STDIN
    stdinMode(0, True)
    
@setHook(HOOK_STDIN)
def stdinEvent(data):    
    
    print data
    
    if data == 'greenOn':
        remoteLedGreenOn()
        
    elif data == 'greenOff':
        remoteLedGreenOff()
        
    elif data == 'pulseBlue':
        remoteLedBlue()
        
    elif data == 'pulseRed':
        remoteLedRed()
            
    elif data == 'reboot':
        rebootWiFly()
        
    elif data == 'light':
        lightReadings()
        
    dataIn = ''
    

def enterCommandMode(): #activates command mode on the RN-171-XV module
    print'$$$',
    print'',
    
def rebootWiFly(): #reboots the RN-171-XV module
    print'reboot'     
    
def showResult(obj):
    print obj

def lightReadings(): #displays light reading from remote node, sends to server
    rpc(nodeAddr, 'callback', 'showResult', 'readAdc', 2)

def closeSerial(): # You should close the TCP connection before you run 'enterCommandMode()'
    print'close' 
    

def remoteLedRed():
    print'Red LEDs'
    rpc(nodeAddr, 'RedLedPulse')
    

def remoteLedGreenOn():
    print'Green LEDs'
    rpc(nodeAddr, 'GreenLedOn')
    

def remoteLedGreenOff():
    print'Green LEDs'
    rpc(nodeAddr, 'GreenLedOff')
    

def remoteLedBlue():
    print'Blue LEDs'
    rpc(nodeAddr, 'BlueLedPulse')