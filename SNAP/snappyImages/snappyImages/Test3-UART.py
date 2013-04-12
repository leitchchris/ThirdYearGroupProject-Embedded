"""
  Author			: Chris Leitch  
  Last Modified 	: 12 April 2013       Created  :  05 March 2013
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

node1Addr = '\x04\x35\x1D'

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
    if data == 'greenOn':
        remoteLedGreenOn()
        
    elif data == 'greenOff':
        remoteLedGreenOff()
        
    
    dataIn = ''

def rebootWiFly(): #reboots the RN-171-XV module
    print'reboot'     
    

def enterCommandMode(): #activates command mode on the RN-171-XV module
    print'$$$',
    print'',
    

def openOutputToSerial():  #opens tcp connection to the given ip address and port
    print"open 192.168.0.1 5000"
    

def talkToSerial(): #sends any text input out to the serial connection
    print'helllllllllllllllllooooooooooooooooo'  
    print'*OPEN*'
    

def closeSerial(): #Should close the TCP connection if you run 'enterCommandMode()' first while a connection is open
    print'close' 
    

def remoteLedRed():
    print'Red LEDs'
    rpc(node1Addr, 'RedLedPulse')
    

def remoteLedGreenOn():
    print'Green LEDs'
    rpc(node1Addr, 'GreenLedOn')
    

def remoteLedGreenOff():
    print'Green LEDs'
    rpc(node1Addr, 'GreenLedOff')
    

def remoteLedBlue():
    print'Blue LEDs'
    rpc(node1Addr, 'BlueLedPulse')