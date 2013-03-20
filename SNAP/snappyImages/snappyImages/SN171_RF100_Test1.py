"""
/********************************************************************
  Author			: Frank Greig  
  Last Modified 	: 12th May 2012	       Created  :  12th May 2012
  File			    : Test1.py
  Target Hardware	: Synapse Wireless - RF100 
  Firmware Version	: 2.4.20
  Version		    : 1.0.0
  Description	: 
     
  Requires:
            SN171 and RF100 module with phidget touch panel and two tilt switches

*******************************************************************************/
"""
# Use Synapse Evaluation Board definitions
from RF100 import *

# -------------  Global Constants  -----------------------------------
portalAddr   = '\x00\x00\x01'     # hard-coded address for Portal

GREEN_LED   = GPIO_1
YELLOW_LED  = GPIO_2
BUTTON_PIN  = GPIO_5

NodeNum = "1"
# -------------  Global variables  -----------------------------------
numbuttonpresses =0
photoVal =0

Nodestr = " Node" + NodeNum + " :   "

@setHook(HOOK_STARTUP)
def startupEvent():
    """This is hooked into the HOOK_STARTUP event"""  
    
    setPinDir(GREEN_LED, True) 
    setPinDir(YELLOW_LED, True)
    
      
    # Set tilt switches as input, and set a HOOK_GPIN invocation when they change state
    setPinDir(BUTTON_PIN ,False)
    monitorPin(BUTTON_PIN,True)
  
#******************************************************************
#***    Button handler...
#******************************************************************
#   This is the function that will react to button presses.
#   When the tilt switches change state it increments or decrements the delay time for updating the LED string.
# Note that this event handler gets run on both edges of the switch pulse, hence the need for 'gotbothedges'
@setHook(HOOK_GPIN)
def buttonEvent(pin,isSet):
    global numbuttonpresses
    
    if (pin == BUTTON_PIN) and isSet:    # If the event is caused be the button push  increment count
        numbuttonpresses += 1
               
    pulsePin(GREEN_LED, 200, False)  
       
   

@setHook(HOOK_1S)
def updateSensors():
    global counter
    global photoVal
    global numbuttonpresses
   
   
    ReadPhotoSensor()
    pulsePin(YELLOW_LED, 200, False)
   
    # Send the data to the Portal node
    eventString = Nodestr + "    Buttonpresses  >>  "+ str(numbuttonpresses) + "          Photocell >>  " + str(photoVal)  
    rpc(portalAddr, "logEvent", eventString)       
         

def ReadPhotoSensor():
    """This will gather the info from the sensor and send it to the Portal log """
    global photoVal

    photoVal = readAdc(3)                                   # connected to GPIO15 fg03/12

    # pulsePin(YELLOW_LED, 500, False)     