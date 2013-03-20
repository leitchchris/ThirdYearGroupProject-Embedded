"""
/********************************************************************
  Author			: Frank Greig  
  Last Modified 	: 3rd January 2013	       Created  :  12th May 2012    
  File			    : F120SensorV0.py
  Target Hardware	: Synapse Wireless - RF100 
  Firmware Version	: 2.4.20
  Version		    : 1.0.0
  Description	: 
     
  Requires:
            F120 Expanson board Sensor  RF100 module with photsensor and tilt switch
            Sends data to C8051F120 connected node
            *******************************************************************************/
"""
# Use Synapse Evaluation Board definitions
from RF100 import *

# -------------  Global Constants  -----------------------------------
portalAddr   = '\x00\x00\x01'     # hard-coded address for Portal
MCUBaseNode  = '\x03\xB9\x95'     # hard-coded address for LED strip driver node

GREEN_LED   = GPIO_2
RED_LED     = GPIO_1
BLUE_LED    = GPIO_0

TiltSwitch1 = GPIO_13


NodeNum = "ZZ"
# -------------  Global variables  -----------------------------------
photoVal =0
tiltcount = 0

Nodestr = " Node " + NodeNum + " :   "

@setHook(HOOK_STARTUP)
def startupEvent():
    """This is hooked into the HOOK_STARTUP event"""  
    
    # Set GPIOs for LEDs as outputs
    setPinDir(GREEN_LED, True) 
    setPinDir(RED_LED, True)
    setPinDir(BLUE_LED, True)
    
    writePin(GREEN_LED, True)   # Turn LEDs OFF
    writePin(RED_LED, True) 
    writePin(BLUE_LED, True) 
   
         
    # Set tilt  as input, and set the HOOK_GPIN invocation when they change state
    setPinDir(TiltSwitch1 ,False)
    monitorPin(TiltSwitch1,True)
  
#******************************************************************
#***    Button handler...
#******************************************************************
#   This function reacts to GPIO input events. Any change on a digital input pin causes this event handler to run
@setHook(HOOK_GPIN)
def buttonEvent(pin,isSet):
    global tiltcount
    
    if (pin == TiltSwitch1) and isSet:    # If event is caused by the tiltswitch
        tiltcount += 1
       
                
    

@setHook(HOOK_1S)
def updateSensors():
   # global photoVal, numbuttonpresses, tiltcount, touchVal 
   
    ReadSensors()
    pulsePin(RED_LED, 100, False)
    pulsePin(GREEN_LED, 100, False) 
    pulsePin(BLUE_LED, 100, False) 
  
    # Send the sensor data to the Portal event log 
    eventString = Nodestr + " Tilts >> " + str(tiltcount) + "   Photocell >> " + str(photoVal)  
    rpc(portalAddr, "logEvent", eventString) 
    rpc(MCUBaseNode, "updateSensorData", eventString)     # Send the data to the base station data collection node
   
    # rpc(MasterBaseNode1, 'updateSensorData', tiltcount,photoval)     

      
         

def ReadSensors():
    """This reads ADC Channels  """
    global photoVal 
    photoVal = readAdc(3)           # Read photosensor on GPIO15
  
    