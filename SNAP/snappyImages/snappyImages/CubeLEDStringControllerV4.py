"""
/********************************************************************
  Author			: Frank Greig  
  Last Modified 	: 30th December 2012	       Created  :  12th May 2012
  File			    : CubeLEDStrincontrollerV2.py
  Target Hardware	: Synapse Wireless - RF100 
  Firmware Version	: 2.4.20
  Version		    : 1.0.0
  Description	: 
     This controller script update the led string pattern using a touch widget and two tilt switches.
      
  Requires:
            RF100 module with phidget touch panel and two tilt switches

*******************************************************************************/
"""
# Use Synapse Evaluation Board definitions
from RF100 import *

# -------------  Global Constants  -----------------------------------
portalAddr   = '\x00\x00\x01'     # hard-coded address for Portal
LEDriverAddr = '\x03\xBF\x3E'     # hard-coded address for LED strip driver node
# LEDriverAddr = '\x00\x19\x45'     # hard-coded address for LED strip driver node


RED_LED  = GPIO_11
Touch    = GPIO_18
Tilt1    = GPIO_17
Tilt2    = GPIO_16

TOUCHTHRESHOLD = 500  # Minimum for detected touch sensor 
MAXDELAY = 100        # With a timer hook of 10 millisecond this is 200 x 10 = 2s
MINDELAY = 5         # This is set purely for visual comfort at 100ms

# -------------  Global variables  -----------------------------------
blinkspeed = MINDELAY
blinkpattern = 1
now       = 0

@setHook(HOOK_STARTUP)
def startupEvent():
    """This is hooked into the HOOK_STARTUP event"""  
    
    setPinDir(RED_LED, True)   # set the LED pin to be output  
    
    # Set tilt switches as input, and set a HOOK_GPIN invocation when they change state
    setPinDir(Tilt1 ,False)
    setPinPullup(Tilt1,True)
    monitorPin(Tilt1,True)
    
    setPinDir(Tilt2 ,False)
    setPinPullup(Tilt2,True)
    monitorPin(Tilt2,True)
  
#******************************************************************
#***    Button handler...
#******************************************************************
#   This is the function that will react to button presses.
#   When the tilt switches change state it increments or decrements the delay time for updating the LED string.
# Note that this event handler gets run on both edges of the switch pulse, hence the need for 'gotbothedges'
@setHook(HOOK_GPIN)
def buttonEvent(pin,isSet):
    global blinkpattern,blinkspeed
    
    if (pin == Tilt2) and isSet:    # If event is caused by the tiltswitch
        blinkspeed += 5
    
    if  blinkpattern > 8:       # Don't exceed 10ms x MAXDELAY value
        blinkpattern = 1  
        
    if (pin == Tilt1) and isSet:    # If event is caused by the tiltswitch
        blinkpattern +=1
        
    if  blinkspeed > MAXDELAY:       # Don't exceed 10ms x MAXDELAY value
        blinkspeed = MINDELAY  
            
   
            
   
   

@setHook(HOOK_1S)
def updateBlinkpattern():
    global blinkpattern,blinkspeed
     # Send the data to the Portal node
    eventString = "LED Pattern >> " + str(blinkpattern) +  "    Blink speed >> " + str(blinkspeed)
    rpc(portalAddr, "logEvent", eventString)        
   
@setHook(HOOK_10MS)
def updateSensors():
   global blinkspeed, now
      
   now += 1        
   if now == blinkspeed:
        updateLEDpattern()
        pulsePin(RED_LED, 200, True)
        now = 0 
 
   if now >= MAXDELAY:
        now = 0
   
             
def updateLEDpattern():
    """Get current number of button presses and send it to portal and the controller node"""
    
    eventString = "Current LED Pattern  >>  " + str(blinkpattern)    # Send the data to the Portal node
   #rpc(portalAddr, "logEvent", eventString)
    rpc(LEDriverAddr, "updateLEDString", blinkpattern)     # Send the data to the LED controller node
   

