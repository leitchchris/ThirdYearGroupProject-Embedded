"""
/********************************************************************
  Author			: Frank Greig  
  Last Modified 	: 29th December 2012	       Created  :  29th December 2012
  File			    : F120CommsV0.py
  Target Hardware	: Synapse Wireless - RF100 
  Firmware Version	: 2.4.19
  Version		    : 1.0.0
  Description	: Basically an I2c bus test for comms to an F120 MCU. 
                  
  Requires:
            SN171 and RF100 module with M41T00 RTTC connected on I2C pins. 
            GPIO 17 [RFET pin # 19] [SDA] & GPIO 18 [RFET pin # 20] [SCL]
            
                      
Working Status:         Ok - no bugs except doing multi register reads using readClock(firstReg, numRegs)
                        does not work? Single register reads will do the job.

*******************************************************************************/
 """

# Use Synapse Evaluation Board definitions
from RF100 import *

# -------------  Global Constants  -----------------------------------

# -------------  Global variables  -----------------------------------
 
# Startup Hook
#--------------------    
@setHook(HOOK_STARTUP)
def start():
    setPinDir(GPIO_17, True) 
    setPinDir(GPIO_18, True)     # 
    
@setHook(HOOK_100MS)                 # Update date and time every one second
def I2CBusTests():
    pulsePin(GPIO_17, 40, True)      # Test only Pulse the LED for visual
    pulsePin(GPIO_18, 25, True)      # Test only Pulse the LED for visual
   


