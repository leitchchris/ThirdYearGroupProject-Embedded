"""
/********************************************************************
  Author			: Frank Greig  
  Last Modified 	: 14th December 2012	       Created  :  14th December 2012
  File			    : M41T00V1.py
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
portalAddr = '\x00\x00\x01'     # hard-coded address for Portal <------------<<<<<<<<

GREEN_LED   = GPIO_1
YELLOW_LED  = GPIO_2
BUTTON_PIN  = GPIO_5

M41T00_ADDRESS = 0xD0      # slave address is (0)1101000 which shifts to 1101000(R/W)

retries = 1

# -------------  Global variables  -----------------------------------
# Global M41T00 Time / Date - Integers - default bootup
M41T00_MONTH    = 1
M41T00_DATE     = 1
M41T00_YEAR     = 0
M41T00_HOURS    = 12
M41T00_MINUTES  = 0
M41T00_SECONDS  = 0
M41T00_DOW      = 1  # Day of week --> Sun = 1, Mon = 2
 
# Startup Hook
#--------------------    
@setHook(HOOK_STARTUP)
def start():
       
    # Initialize all non user pins to output/low for minimum power consumption
    setPinDir(GPIO_0, True) 
    writePin(GPIO_0, False) 
    
    setPinDir(GREEN_LED, True)     # SN171 LED #1 GRN (right)
    writePin(GREEN_LED, False)
       
    setPinDir(YELLOW_LED, True)    # SN171 LED #2  YEL (left)
    writePin(YELLOW_LED, False)
    
    setPinDir(GPIO_3, True) 
    writePin(GPIO_3, False)
    
    setPinDir(GPIO_4, True) 
    writePin(GPIO_4, False)
    
    setPinDir(BUTTON_PIN, False)      # PushButton switch on SN171 GPIO 5
    setPinPullup(BUTTON_PIN, True)  
    
    setPinDir(GPIO_6, True)
    writePin(GPIO_6, False)
    
    setPinDir(GPIO_7, False)         # Uart 1 Input - connected on SN171 board
    #writePin(GPIO_7, True)
    
    setPinDir(GPIO_8, True)          # Uart 1 Output - connected on SN171 board
    writePin(GPIO_8, False)
    
    setPinDir(GPIO_9, True)
    writePin(GPIO_9, False)
    
    setPinDir(GPIO_10, True)   
    writePin(GPIO_10, False)
    
    setPinDir(GPIO_11, True)        # Analog 7
    writePin(GPIO_11, False)
    
    setPinDir(GPIO_12, True)        # Analog 6 
    writePin(GPIO_12, False)
  
    setPinDir(GPIO_13, True)        # Analog 5
    writePin(GPIO_13, False)
    
    setPinDir(GPIO_14, True)         # Analog 4
    writePin(GPIO_14, False)
    
    setPinDir(GPIO_15, True)         # Analog 3
    writePin(GPIO_15, False)
    
    setPinDir(GPIO_16, True)         # Analog 2
    writePin(GPIO_16, False)
   
    M41T00_initRTTC()               # Initialise I2C and set initial date and time
    


@setHook(HOOK_1S)                 # Update date and time every one second
def GetRTTCValues():
    
    writeClockReg(7, 0)                #  Register 7  Bit 7 clear OUT bit - LED on RTTC chip
    pulsePin(GREEN_LED, 75, True)      # Test only Pulse the LED for visual
    getTimeDate()                      # Read and send date and time registers in M41T00
    writeClockReg(7, 128)              #  Register 7  Bit 7 set OUT bit - LED on RTTC chip
    
      


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
    
    # FOR TESTING ONLY !
    eventString = "Date: " + str(M41T00_MONTH) + "/" + str(M41T00_DATE) + "/" + str(M41T00_YEAR) + " " "Time: " + str(M41T00_HOURS) + ":" + str(M41T00_MINUTES) + ":" + str(M41T00_SECONDS) + " DOW = " + str(M41T00_DOW)  
    rpc(portalAddr, "logEvent", eventString)
    
 
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
        
    """The countdown chain is reset whenever the seconds register
    is written. Write transfers occur on the acknowledge
    from the DS3231. Once the countdown chain is reset, to
    avoid rollover issues the remaining time and date registers
    must be written within 1 second."""
        

def M41T00_initRTTC():
    i2cInit(False)                        # No pullups = false 
    setTimeDate(23,59,50,6,12,31,1999)    # set time to  23:59:50 on December 31st 1999
