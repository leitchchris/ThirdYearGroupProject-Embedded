"""
  Author			: Chris Leitch  
  Last Modified 	: 12 April 2013       Created  :  05 March 2013
  File			    : Test1-GroupProject.py
  Target Hardware	: Synapse Wireless - RF100 
  Firmware Version	: 2.4.19
  Version		    : 1.0.0
  Description	    : A sensor (light) reader and lock/light control node 
     
  Requires:
            RF100 module with photsensor ,tilt switch and LEDs
"""
# Use Synapse Evaluation Board definitions
from RF100 import *


# -------------  Global Constants  -----------------------------------
portalAddr   = '\x00\x00\x09'     # hard-coded address for Portal

GREEN_LED   = GPIO_2
RED_LED = GPIO_1
BLUE_LED  = GPIO_0

BUTTON_PIN  = GPIO_5
TiltSwitch1 = GPIO_15

NodeNum = "1"


# -------------  Global variables  -----------------------------------

Nodestr = " Node" + NodeNum + " :   "


@setHook(HOOK_STARTUP)
def startupEvent():
    """This is hooked into the HOOK_STARTUP event"""  
    
    # Set GPIOs for LEDs as outputs
    setPinDir(GREEN_LED, True) 
    setPinDir(BLUE_LED, True)
    setPinDir(RED_LED, True)
             
    # Set tilt and pushbutton as input, and set the HOOK_GPIN invocation when they change state    
    setPinDir(TiltSwitch1 ,False)
    monitorPin(TiltSwitch1,True)
    
    
#******************************************************************
#***    Tilt/Button Handler
#******************************************************************
#   This function reacts to GPIO input events. Any change on a digital input pin causes this event handler to run
@setHook(HOOK_GPIN)
def buttonEvent(pin,isSet):
    
    if (pin == TiltSwitch1) and isSet:    # If event is caused by the tiltswitch
        tiltcount += 1
        pulsePin(GREEN_LED, 500, False) 
        pulsePin(RED_LED, 1000, False)
    

def GreenLedOn():
    writePin(GREEN_LED, False)
    eventString = "  Green Led On "
    rpc(portalAddr, "logEvent", eventString)
    

def GreenLedOff():
    writePin(GREEN_LED, True)
    eventString = "  Green Led Off "
    rpc(portalAddr, "logEvent", eventString)   
    

def RedLedPulse():
    pulsePin(RED_LED, 500, False)
    redTriggered += 1
    eventString = "Red Led Triggered >> " + str(redTriggered)
    rpc(portalAddr, "logEvent", eventString)
    

def BlueLedPulse():
    pulsePin(BLUE_LED, 500, False)
    blueTriggered += 1
    eventString = "  Blue Led Triggered >> " + str(blueTriggered)
    rpc(portalAddr, "logEvent", eventString)