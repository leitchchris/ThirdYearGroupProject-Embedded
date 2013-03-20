"""
/********************************************************************
  Author			: Frank Greig  
  Last Modified 	: 10th July	       Created  :  12th May 2012      
  File				: SensorBaseNodeSN171.py
  Target Hardware	: Synapse Wireless - RF100  
  Firmware Version	: 2.4.20  
  Version			: 1.0.0

  Description	:   Configures node to redirect received data to
                    a Virtual Comport (VCP) 
                    
   Requires: 
            A USB-to_UART bridge - CP2103  to send sensor data to PC/RealTerm 
            OR - a USB-Stick reconfigured to act as a bridge using command line :
             "root.setup_usb_as_vcp()"  switch back with "root.setupSynapseUsb()"
  
   Comments: works perfectly sending received strings to a serial terminal               
******************************************************************************/
"""

# Use Synapse Evaluation Board definitions
from synapse.RF100 import *
from synapse.switchboard import *
 
# -------------  Global Constants  -----------------------------------
portalAddr   = '\x00\x00\x01'     # hard-coded address for Portal
MCUBaseNode  = '\x03\xB9\x95'     # hard-coded address for LED strip driver node

GREEN_LED   = GPIO_2
RED_LED     = GPIO_1
BLUE_LED    = GPIO_0

TiltSwitch1 = GPIO_13

   
@setHook(HOOK_STARTUP)
def startupEvent():
   
    # Initialize UART
    initUart(1, 57600)          # 57600 baud
    flowControl(1, False)       # No flow control
      
    crossConnect(DS_UART1, DS_STDIO) # Connect received serial data to UART1 pins 
    
      # Set GPIOs for LEDs as outputs
    setPinDir(GREEN_LED, True) 
    setPinDir(RED_LED, True)
    setPinDir(BLUE_LED, True)
    
    writePin(GREEN_LED, True)   # Turn LEDs OFF
    writePin(RED_LED, True) 
    writePin(BLUE_LED, True) 
    
    
    #  -----------------------------------------
    
# This runs when a remote procedure call in a sensor node calls it.  
def updateSensorData(sensordata):
    print sensordata
    pulsePin(BLUE_LED, 100, False) 
   
    
