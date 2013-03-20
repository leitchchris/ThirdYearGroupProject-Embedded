"""
/********************************************************************
  Author			: Frank Greig  
  Last Modified 	: 10th July	       Created  :  12th May 2012
  File			    : SensorBaseNodeSN171.py
  Target Hardware	: Synapse Wireless - RF100 
  Firmware Version	: 2.4.20
  Version		    : 1.0.0
  Description	: 
     
  Requires:
            SN171 and RF100 module with pushbutton connected, tilt switch and photosensor
*******************************************************************************/
"""
# Use Synapse Evaluation Board definitions
from RF100 import *

# -------------  Global Constants  -----------------------------------
portalAddr   = '\x00\x00\x02'     # hard-coded address for Portal
MCUBaseAddr  = '\x03\xB9\x95'     # hard-coded address for LED strip driver node

GREEN_LED   = GPIO_1
YELLOW_LED  = GPIO_2
BUTTON_PIN  = GPIO_5
TiltSwitch1 = GPIO_13

NodeNum = " Chris"

# -------------  Global variables  -----------------------------------
numbuttonpresses =0
photoVal =0
tiltcount = 0

Nodestr = " Node" + NodeNum + ":  "

@setHook(HOOK_STARTUP)
def startupEvent():
    """This is hooked into the HOOK_STARTUP event"""  
    
    setPinDir(GREEN_LED, True) 
    setPinDir(YELLOW_LED, True)
     
    # Set tilt switches as input, and set a HOOK_GPIN invocation when they change state
    setPinDir(BUTTON_PIN ,False)
    monitorPin(BUTTON_PIN,True)
    
    setPinDir(TiltSwitch1 ,False)
    setPinPullup(TiltSwitch1,True)    # Enable 25k pull-up resistor
    monitorPin(TiltSwitch1,True)
  
#******************************************************************
#***    Button handler...
#******************************************************************
#   This function reacts to button presses or tilt switch changes.
#   When the switches change state it increments a simple count.
@setHook(HOOK_GPIN)
def buttonEvent(pin,isSet):
    global numbuttonpresses, tiltcount
    
    if (pin == BUTTON_PIN) and isSet:    # If the event is caused be the button push increment the count
        numbuttonpresses += 1
        pulsePin(GREEN_LED, 200, False)  
               
    if (pin == TiltSwitch1) and isSet:    # If event is caused by the tiltswitch increment the count
        tiltcount += 1
        pulsePin(GREEN_LED, 200, True) 
         
   
@setHook(HOOK_1S)
def updateSensors():
    global photoVal, numbuttonpresses, tiltcount 
   
    ReadPhotoSensor()
    pulsePin(YELLOW_LED, 200, False)
   
    # Send the data to the Portal node
    eventString = Nodestr + " Buttonpresses >  "+ str(numbuttonpresses) + "   Tilts > " + str(tiltcount) + "   Photocell > " + str(photoVal)  
    rpc(portalAddr, "logEvent", eventString)       
    rpc(MCUBaseAddr, "updateSensorData", eventString)     # Send the data to the base station data collection node
        

def ReadPhotoSensor():
    """This will gather the info from the sensor and send it to the Portal log """
    global photoVal

    photoVal = readAdc(3)                                   # connected to GPIO15 fg03/12
    # pulsePin(YELLOW_LED, 500, False)     
    