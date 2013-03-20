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
from synapse.RF100 import *
from synapse.switchboard import *
 
GREEN_LED   = GPIO_1
YELLOW_LED  = GPIO_2
   
@setHook(HOOK_STARTUP)
def startupEvent():
   
    # Initialize UART
    initUart(1, 57600)          # 57600 baud
    flowControl(1, False)       # No flow control
      
    crossConnect(DS_UART1, DS_STDIO) # Connect received serial data to UART1 pins 
    
    setPinDir(GREEN_LED, True)        # set the LED pins to be 'outputs'  
    setPinDir(YELLOW_LED, True)
    
    #  -----------------------------------------
    
# This runs when a remote procedure call in a sensor node calls it.  
def updateSensorData(sensordata):
    print sensordata
    # pulsePin(GREEN_LED, 200, True)  
    
