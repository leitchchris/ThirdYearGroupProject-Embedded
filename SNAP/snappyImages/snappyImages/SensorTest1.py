"""
/********************************************************************
  Author			: Frank Greig  
  Last Modified 	: 18th May 2012	       Created  :  12th May 2012
  File			    : Test1.py
  Target Hardware	: Synapse Wireless - RF100 
  Firmware Version	: 2.4.20
  Version		    : 1.0.0
  Description	: 
     
  Requires:
            SN171 and RF100 module with photsensor and tilt switche
*******************************************************************************/
"""
# Use Synapse Evaluation Board definitions
from RF100 import *

# -------------  Global Constants  -----------------------------------
portalAddr   = '\x00\x00\x01'     # hard-coded address for Portal

GREEN_LED   = GPIO_2
BLUE_LED  = GPIO_0
BUTTON_PIN  = GPIO_5
TiltSwitch1 = GPIO_15


NodeNum = "2"
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
    setPinDir(BLUE_LED, True)
         
    # Set tilt and pushbutton as input, and set the HOOK_GPIN invocation when they change state
    setPinDir(BUTTON_PIN ,False)
    monitorPin(BUTTON_PIN,True)
    
    setPinDir(TiltSwitch1 ,False)
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
        pulsePin(BLUE_LED, 200, True)  

@setHook(HOOK_1S)
def updateSensors():
    global photoVal, numbuttonpresses, tiltcount#, touchVal 
   
    ReadSensors()
    
    # Send the sensor data to the Portal event log 
    eventString = Nodestr + "   Tilts >> " + str(tiltcount) + "   Photocell >> " + str(photoVal)  
    # " Touch >> "+ str(touchVal) +
    rpc(portalAddr, "logEvent", eventString)


def ReadSensors():
    """This reads ADC Channels  """
    global photoVal#, touchVal 

    photoVal = readAdc(2)           # Read photosensor on GPIO16
    