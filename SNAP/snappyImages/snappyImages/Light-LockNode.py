"""
  Author			: Chris Leitch  
  Last Modified 	: 24 April 2013       Created  :  05 March 2013
  File			    : Light-LockNode.py
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

BLUE_LED  = GPIO_0
RED_LED = GPIO_1
GREEN_LED   = GPIO_2
Light = GPIO_3
Servo = GPIO_4
TiltSwitch1 = GPIO_15

@setHook(HOOK_STARTUP)
def startupEvent(): 
    
    # Set GPIOs for control as outputs
    setPinDir(GREEN_LED, True) 
    setPinDir(BLUE_LED, True)
    setPinDir(RED_LED, True)
    setPinDir(Light, True)
    setPinDir(Servo, True)
             
    # Set tilt as input, and set the HOOK_GPIN invocation when they change state    
    setPinDir(TiltSwitch1 ,False)
    monitorPin(TiltSwitch1,True)
    
    
#******************************************************************
#***    Tilt Handler
#******************************************************************
#   This function reacts to GPIO input events. Any change on a digital input pin causes this event handler to run
@setHook(HOOK_GPIN)
def tiltEvent(pin,isSet):
    
    if (pin == TiltSwitch1) and isSet:    # If event is caused by the tiltswitch
        tiltcount += 1
        pulsePin(BLUE_LED, 200, False) 
        pulsePin(RED_LED, 200, False)
        pulsePin(BLUE_LED, 200, False) 
        pulsePin(RED_LED, 200, False)
        pulsePin(BLUE_LED, 200, False) 
        pulsePin(RED_LED, 200, False)
            
def GreenLedOn():
    writePin(GREEN_LED, False)					#sets the pin the green led is connected to as high
    eventString = "  Green Led On"				#creates a event string containing given wording
    rpc(portalAddr, "logEvent", eventString)	#remote calls the "logEvent" on the portal node for debugging
    

def GreenLedOff():
    writePin(GREEN_LED, True)					#sets the pin the green led is connected to as low
    eventString = "  Green Led Off"
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
    
def LightOn():
    writePin(Light, False)
    eventString = "  Lamp On"
    rpc(portalAddr, "logEvent", eventString)
    
def LightOff():
    writePin(Light, True)
    eventString = "  Lamp Off"
    rpc(portalAddr, "logEvent", eventString)

def ServoOn():
    writePin(Servo, False)
    eventString = "  Servo On"
    rpc(portalAddr, "logEvent", eventString)
    
def ServoOff():
    writePin(Servo, True)
    eventString = "  Servo Off"
    rpc(portalAddr, "logEvent", eventString)