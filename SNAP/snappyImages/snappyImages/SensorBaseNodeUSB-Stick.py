"""
/********************************************************************
  Author			: Frank Greig  
  Last Modified 	: 23rd May 2012	Created  :  22nd May 2012           
  File				: SensorBaseNodeUSB-Stick.py
  Target Hardware	: Synapse Wireless - RF100  
  Firmware Version	: 2.4.20  
  Version			: 1.0.0

  Description	:   Snapstick used as USB-to_UART bridge to send sesor data to RealTerm 
   
   Requires: 
            Snapstick reconfigured with CP2102 acting as bridge
           
 
  Comments:     SPI appears to work fine on both RF100 and RF301 modules.              
******************************************************************************/
"""
from synapse.RF100 import *
from synapse.switchboard import *
 
GREEN_LED   = 1 
RED_LED     = 0
   
@setHook(HOOK_STARTUP)
def startupEvent():
   
    # Initialize UART
    initUart(1, 57600)          # 57600 baud
    flowControl(1, False)       # No flow control

    # Connect UART to transparent data endpoint.
    #   The default transparent configuration is broadcast
    # crossConnect(DS_UART1, DS_TRANSPARENT)
    crossConnect(DS_UART1, DS_STDIO)
    # Enable bridge connections on the other UART
    # crossConnect(DS_UART1, DS_PACKET_SERIAL)
    
    setPinDir(GREEN_LED, True)        # set the LED pins to be 'outputs'  
    setPinDir(RED_LED, True)
       
    #  -----------------------------------------
    
def updateSensorData(eventString):
    global  LEDstring
    print eventString
    pulsePin(RED_LED, 200, True)  
    
