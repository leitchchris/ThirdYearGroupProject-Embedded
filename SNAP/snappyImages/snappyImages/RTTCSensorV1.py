"""
/********************************************************************
  Author			: Frank Greig  
  Last Modified 	: 14th December 2012	       Created  :  14th December 2012
  File			    : RTTCSensorV1.py
  Target Hardware	: Synapse Wireless - RF100 
  Firmware Version	: 2.4.19
  Version		    : 1.0.0
  Description	: Basically an I2c bus test for M41T00 RTTC interface. 
                  Sets the intial date and time then reads all registers at 1 scond interval to check that the RTTC is updating
                  autonomously. The M41T00 OUT pin is also toggled (REG 7 bit 7) to give a visual indication of bus operation.
     
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
portalAddr = '\x00\x00\x01'       # hard-coded address for Portal <------------<<<<<<<<
MCUBaseNode  = '\x03\xB9\x95'     # hard-coded address for network base station

GREEN_LED   = GPIO_1
YELLOW_LED  = GPIO_2
BUTTON_PIN  = GPIO_5
TiltSwitch1 = GPIO_13

M41T00_ADDRESS = 0xD0      # slave address is (0)1101000 which shifts to 1101000(R/W)
NodeNum = "GQ"
retries = 1

# -------------  Global variables  -----------------------------------
# Global M41T00 Time / Date - Integers - default bootup
global M41T00_MONTH ,M41T00_DATE ,M41T00_YEAR 
global M41T00_HOURS  , M41T00_MINUTES , M41T00_SECONDS  
global M41T00_DOW                                            # Day of week --> Sun = 1, Mon = 2
 

numbuttonpresses =0
photoVal =0
tiltcount = 0

Nodestr = "Node >> " + NodeNum + " :   "
 
# Startup Hook
#--------------------    
@setHook(HOOK_STARTUP)
def start():
       
     # Set GPIOs for LEDs as outputs
    setPinDir(GREEN_LED, True) 
    setPinDir(YELLOW_LED, True)
         
    # Set tilt and pushbutton as input, and set the HOOK_GPIN invocation when they change state
    setPinDir(BUTTON_PIN ,False)
    monitorPin(BUTTON_PIN,True)
    
    setPinDir(TiltSwitch1 ,False)
    setPinPullup(TiltSwitch1,True)    # Enable 25k pull-up resistor
    monitorPin(TiltSwitch1,True)
    
    M41T00_initRTTC()               # Initialise I2C and set initial date and time
    

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


@setHook(HOOK_1S)                 # Update date and time every one second
def updateSensors():
      
    ReadSensors()     # Read sensor data and send data to the Portal event log 
    eventString = Nodestr + "     Tilts >> " + str(tiltcount) + "   Photocell >> " + str(photoVal)  
    rpc(portalAddr, "logEvent", eventString) 
   
    writeClockReg(7, 0)                #  Register 7  Bit 7 clear OUT bit - LED on RTTC chip
    pulsePin(GREEN_LED, 75, True)      # Test only Pulse the LED for visual
   
    getTimeDate()                      # Read and send date and time registers in M41T00
    eventString = "Date : " + str(M41T00_MONTH) + "/" + str(M41T00_DATE) + "/" + str(M41T00_YEAR) + "    Time : " + str(M41T00_HOURS) + ":" + str(M41T00_MINUTES) + ":" + str(M41T00_SECONDS) + "     DOW = " + str(M41T00_DOW)  
    rpc(portalAddr, "logEvent", eventString)
    
    
   
    writeClockReg(7, 128)              #  Register 7  Bit 7 set OUT bit - LED on RTTC chip
   
    



def ReadSensors():
    """This reads ADC Channels  """
    global photoVal 

    photoVal = readAdc(3)           # Read photosensor on GPIO15
  
 

def buildRtcCmd(registerAddress, isRead):
    slaveAddress = M41T00_ADDRESS
    if isRead:
        slaveAddress |= 1      # read

    cmd = ""
    cmd += chr( slaveAddress )
    cmd += chr( registerAddress )

    return cmd

def readClock(firstReg, numRegs):                                  # does not work ????  
    """read a string of registers from the RTC"""
    cmd = buildRtcCmd(firstReg, False)  
    i2cWrite(cmd, retries, False)  

    cmd = chr( M41T00_ADDRESS | 1 )
    result = i2cRead(cmd, numRegs, retries, False) 
             
    return result

def displayClockTime(): #Status: Ok
    Seconds = bcdToDec(readClockReg(0) & 0x7F)
    Minutes = bcdToDec(readClockReg(1))
    Hours   = bcdToDec(readClockReg(2) & 0x3F)    
    DOW     = bcdToDec(readClockReg(3))
       
    eventString = "Elapsed Time : " + str(Hours) + ":" + str(Minutes) + ":" + str(Seconds) + " DOW = " + str(DOW) 
    rpc(portalAddr, "logEvent", eventString)
    
    
def displayClockDate(): #Status: Ok
    Date    = bcdToDec(readClockReg(4))
    Month   = bcdToDec(readClockReg(5))
    Year    = bcdToDec(readClockReg(6))
   
    eventString = "Date: " + str(Month) + "/" + str(Date) + "/" + str(Year) 
    rpc(portalAddr, "logEvent", eventString)
    
    

def readClockReg(register): #Status: Ok --> Returns an integer - manually convert this integer dec to hex - do not modify !!!!
    """read a single numeric register from the RTC"""
    cmd = buildRtcCmd(register, False)
    i2cWrite(cmd, retries, False)

    cmd = chr( M41T00_ADDRESS | 1 )
    resultStr = i2cRead(cmd, 1, retries, False)
    
    result = ord( resultStr[0] )
    
    return result


def writeClockReg(register, value):
    """write a numeric register value to the RTC"""
    cmd = buildRtcCmd(register, False)
    cmd += chr(value)
    i2cWrite(cmd, retries, False)
       
    
def decToBcd(val):
    return ( (val/10*16) + (val%10) ) 

def bcdToDec(val):
    return ( (val/16*10) + (val%16) )   


def getTimeDate(): #Status: ok
    global M41T00_SECONDS
    global M41T00_MINUTES
    global M41T00_HOURS
    global M41T00_DOW
    global M41T00_DATE
    global M41T00_MONTH
    global M41T00_YEAR
    
    M41T00_SECONDS = bcdToDec(readClockReg(0) & 0x7F)
    M41T00_MINUTES = bcdToDec(readClockReg(1))
    M41T00_HOURS   = bcdToDec(readClockReg(2) & 0x3F)  # Military Time   
    M41T00_DOW     = bcdToDec(readClockReg(3))
    M41T00_DATE    = bcdToDec(readClockReg(4))
    M41T00_MONTH   = bcdToDec(readClockReg(5))
    M41T00_YEAR    = bcdToDec(readClockReg(6))
    
   
 
def setTimeDate(hourINT,minuteINT,secondINT,dowINT,monthINT,dateINT,yearINT):
    """set hour(Military Time), minute, second, dow, month, date, year - each must an integer"""
    # Range or input checking is NOT performed. <---------------<<<<<<<<<<<
    writeClockReg(0, decToBcd(secondINT))  # 0 - 59 - Seconds
    writeClockReg(1, decToBcd(minuteINT))  # 0 - 59 - Minutes
    writeClockReg(2, decToBcd(hourINT))    # 0 - 23 - Hours Military Time ONLY!
    writeClockReg(3, decToBcd(dowINT))     # 1 -  7 - DOW - Day of week - Sun = 1
    writeClockReg(4, decToBcd(dateINT))    # 1 - 31 - Date
    writeClockReg(5, decToBcd(monthINT))   # 1 - 12 - Month 
    writeClockReg(6, decToBcd(yearINT))    # 0 - 99 - Year    
        
   
        

def M41T00_initRTTC():
    i2cInit(False)                        # No pullups = false 
    setTimeDate(23,59,50,6,12,31,1999)    # set time to  23:59:50 on December 31st 1999
