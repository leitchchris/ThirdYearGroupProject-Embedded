"""
/********************************************************************
  Author			: Frank Greig  
  Last Modified 	: 10th |July 2012	       Created  :  12th May 2012
  File			    : Test1.py
  Target Hardware	: Synapse Wireless - RF100 
  Firmware Version	: 2.4.20
  Version		    : 1.0.0
  Description	: 
     
  Requires:
            SN171 and RF100 module with photsensor and tilt switch and touch sensor
            *******************************************************************************/
"""
# Use Synapse Evaluation Board definitions
from RF100 import *

# -------------  Global Constants  -----------------------------------
portalAddr   = '\x00\x00\x01'     # hard-coded address for Portal
MasterBaseNode0 = '\x00\x8D\x08'     # hard-coded address for LED strip driver node
MasterBaseNode1 = '\x00\x19\x45'     # hard-coded address for LED strip driver node
MasterBaseNode2 = '\x00\x6C\x8D'     # hard-coded address for LED strip driver node

GREEN_LED   = GPIO_1
YELLOW_LED  = GPIO_2
BUTTON_PIN  = GPIO_5
TiltSwitch1 = GPIO_13
Touch       = GPIO_17

NodeNum = "7"
# -------------  Global variables  -----------------------------------
numbuttonpresses =0
photoVal =0
tiltcount = 0


Nodestr = " Node" + NodeNum + " :   "

@setHook(HOOK_STARTUP)
def startupEvent():
    """This is hooked into the HOOK_STARTUP event"""  
    
    # Set GPIOs for LEDs as outputs
    setPinDir(GREEN_LED, True) 
    setPinDir(YELLOW_LED, True)
         
    # Set tilt and pushbutton as input, and set the HOOK_GPIN invocation when they change state
    setPinDir(BUTTON_PIN ,False)
    monitorPin(BUTTON_PIN,True)
    
    setPinDir(TiltSwitch1 ,False)
    setPinPullup(TiltSwitch1,True)    # Enable 25k pull-up resistor
    monitorPin(TiltSwitch1,True)
  
#******************************************************************
#***    Button handler...
#******************************************************************
#   This function reacts to GPIO input events. Any change on a digital input pin causes this event handler to run
@setHook(HOOK_GPIN)
def buttonEvent(pin,isSet):
    global numbuttonpresses, tiltcount
    
    if (pin == TiltSwitch1) and isSet:    # If event is caused by the tiltswitch
        tiltcount += 1
        pulsePin(GREEN_LED, 200, True) 
                
    if (pin == BUTTON_PIN) and isSet:    # If the event is caused be the button push  
        numbuttonpresses += 1
        pulsePin(GREEN_LED, 200, True)  

@setHook(HOOK_1S)
def updateSensors():
    global photoVal, numbuttonpresses, tiltcount, touchVal 
   
    ReadSensors()
    pulsePin(YELLOW_LED, 200, False)
    
    # Send the sensor data to the Portal event log 
    eventString = Nodestr + " Touch >> " + str(touchVal) + "   Tilts >> " + str(tiltcount) + "   Photocell >> " + str(photoVal)  
    rpc(portalAddr, "logEvent", eventString) 
    rpc(MasterBaseNode0, "updateSensorData", eventString)     # Send the data to the base station data collection node
   
    # rpc(MasterBaseNode1, 'updateSensorData', tiltcount,photoval)     

      
         

def ReadSensors():
    """This reads ADC Channels  """
    global photoVal, touchVal 

    photoVal = readAdc(3)           # Read photosensor on GPIO15
    touchVal = readAdc(1)           # Read phidget touch sensor on GPIO17

    