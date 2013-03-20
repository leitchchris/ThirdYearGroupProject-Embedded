"""
/********************************************************************
  Author			: Frank Greig  
  Last Modified 	: 3rd January 2013	       Created  :  12th May 2012      
  File				: WiFlyBridgeV0.py
  Target Hardware	: Synapse Wireless - RF100  
  Firmware Version	: 2.4.19  
  Version			: 1.0.0

  Description	:   Data received on Wifly node is soft connected to a SNAP node which transmits a blinkpattern 
                    character to the LED strip SNAP controller. When associated and the Telnet connection is made the GREEN LED on the WiFly module is on.
                    A slow flash indicates association but no connection. 
                    
   Requires:  Softconnect running on the host MCU, a Telnet connection into the Wifly module.
   
  
   Status : works perfectly with LEDStringV8.py running on the LED strip node.               
******************************************************************************/
"""
from synapse.RF100 import *
from synapse.switchboard import *

portalAddr   = '\x00\x00\x01'     # hard-coded address for Portal
LEDriverAddr = '\x03\xBF\x3E'     # hard-coded address for LED strip driver node 

   
@setHook(HOOK_STARTUP)
def startupEvent():
   
    # Initialize UART
    initUart(1, 57600)          # 57600 baud
    flowControl(1, False)       # No flow control
    stdinMode(1, True)          # Character Mode, Echo On
    stdinEvent(1)
    
    crossConnect(DS_UART1, DS_STDIO) # Connect received serial data to UART1 pins 
    
    
@setHook(HOOK_STDIN)    
def stdinEvent(blinkpattern):    # Executes when a single character is received on UART 1
    eventString = "Current LED Pattern  >>  " + str(blinkpattern)    # Send the data to the Portal node
    rpc(portalAddr, "logEvent", eventString)
    rpc(LEDriverAddr, "updateLEDString", blinkpattern[0])     # Send the blinkpattern to the LED strip controller node


       
   
