"""
/********************************************************************
  Author			: Frank Greig  
  Last Modified 	: 3rd January 2012    	Created  :  29th March 2012           
  File				: StringV8.py
  Target Hardware	: Synapse Wireless - RF100 & RF301 
  Firmware Version	: 2.4.20  
  Version			: 1.0.0

  Description	:   SPI interface for WS2801 Ledstrip. |Uses characters to select the LED patterns 
   
   Requires: 
            SN171 Prototype Board
            For RF100 GPIO12 - MOSI and GPIO13 - SCLK 
            For RF301 GPIO5  - MOSI and GPIO6  - SCLK 
 
  Comments:     SPI appears to work fine on both RF100 and RF301 modules.              
*******************************************************************************/
"""
from synapse.RF100 import *



STRIP_LENGTH = 16                         # number of LEDs in the strip
STRIP_BYTES = STRIP_LENGTH * 3           #  * 3 bytes for RGB ( 24-bits per diode

OFF      = '\x00\x00\x00'      # all OFF
WHITE    = '\xFF\xFF\xFF'      # all RGB
YELLOW   = '\xFF\xFF\x00'      # all RED + GREEN
RED      = '\xFF\x00\x00'      # all RED
GREEN    = '\x00\xFF\x00'      # all GREEN
BLUE     = '\x00\x00\xFF'      # all BLUE
MAGENTA  = '\xFF\x00\xFF'      # all RED + BLUE
LTBLUE   = '\x00\xFF\xFF'      # all GREEN + BLUE
PURPLE   = '\x80\x20\x80'      # all GREEN + BLUE

LEDstring = ''
count = 0
   
@setHook(HOOK_STARTUP)
def startupEvent():
    spiInit(False,False, True, False)   # 2-wire MOSI & SCLK only, latch data on clk leading edge, data change on clk =0 
   
    #setPinDir(GREEN_LED, True)        # set the LED pins to be 'outputs'  
    #setPinDir(YELLOW_LED, True)
       
    #  -----------------------------------------
    
def updateLEDString(blinkpattern):
    global  LEDstring
    
    LEDstring = ''
    if (blinkpattern== '1'):
        toggleLedString1_1(BLUE,WHITE)           # Alternate two colours     
    if (blinkpattern== '2'):
        toggleLedString1_1(PURPLE,WHITE)           # Alternate two colours     
    if (blinkpattern== '3'):
        toggleLedString1_1(RED,WHITE)             # Alternate two colours  
    if (blinkpattern== '4'):
        buildLedStringRandom()                  # Send random RGB string to LEDs
    if (blinkpattern== '5'):
        buildLedString2_2(MAGENTA,WHITE)      # 2 ON  2 OFF colour sequence
    if (blinkpattern== '6'):
        buildLedString2_2(OFF,WHITE)          # 2 ON  2 OFF colour sequence
    if (blinkpattern== '7'):  
        toggleLedString2_2(RED,BLUE)           # 1 ON  1 OFF colour sequence
    if (blinkpattern== '8'):
        buildLedString(YELLOW)
    
    spiWrite(LEDstring)              # Send RGB string to LEDs      
    spiWrite(LEDstring)              # Send RGB string to LEDs      
  #  pulsePin(GREEN_LED,100,True)
    

def toggleLedString1_1(COLOUR1,COLOUR2):
    global count
    
    if (count & 0x01) == 0:
        buildLedString1_1(COLOUR1,COLOUR2)           # 1 ON  1 OFF colour sequence
    else:
        buildLedString1_1(COLOUR2,COLOUR1)           # 1 ON  1 OFF colour sequence
    count +=1
  
def toggleLedString2_2(COLOUR1,COLOUR2):
    global count
    
    if (count & 0x01) == 0:
        buildLedString2_2(COLOUR1,COLOUR2)           # 1 ON  1 OFF colour sequence
    else:
        buildLedString2_2(COLOUR2,COLOUR1)           # 1 ON  1 OFF colour sequence
    count +=1
      
def buildLedString1_1(COLOUR1,COLOUR2):
    global  LEDstring
    
    RGBbytes =0
    while (RGBbytes < STRIP_BYTES):
       if (RGBbytes & 0x01) == 1:
           LEDstring += COLOUR1
       else:  
            LEDstring +=COLOUR2
       RGBbytes += 1
    
 
 
def buildLedString2_2(COLOUR1,COLOUR2):
    global  LEDstring
    RGBcount = 0
    RGBbytes =0
    while (RGBbytes < STRIP_BYTES):
       if (RGBcount & 0x01) == 1:
           LEDstring += COLOUR1
           LEDstring += COLOUR1
       else:  
            LEDstring += COLOUR2
            LEDstring += COLOUR2
       RGBbytes += 2
       RGBcount +=1
    
 
def buildLedStringRandom():
    global  LEDstring
    LEDstring = ''
    RGBbytes =0
    while (RGBbytes < STRIP_BYTES):
       LEDstring += chr(random() >> 4)
       RGBbytes += 1
    
 
def buildLedString(colour):
    global  LEDstring
    LEDstring = ''
    RGBbytes =0
    while (RGBbytes < STRIP_BYTES):
       LEDstring += colour
       RGBbytes +=1
    
   
  