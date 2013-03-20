# Frank Greig   - Dec 2012
# http://forums.synapse-wireless.com/showthread.php?t=519&highlight=bit-banged
# has routines for repeated start  - required by MPR121 and is not in SNAP routines @ version 2.4.19

# http://forums.synapse-wireless.com/showthread.php?t=519&highlight=bit-banged
#----------------------------------------------------------------------------------
"""
    Read the SMB battery parameters
    This uses the SN171 protoboard with
    connections as follows:     
        I2C Data:  GPIO17
        I2C Clock: GPIO18
        1K pullup resistors from 3.3V to GPIO17 and GPIO18

    Uses bit-banged routines instead of the built-in I2C functions 
    User function is ReadSMBData() at bottom 

    rpc() returns to SMBData() in your app:

    public void SMBData( byte[] Addr, int code, int val )
        where:  Addr is the MAC address of the responding Node 
                code is the SMB register:
                    0x1C = Serial Number
                    0x10 = Full Charge Capacity
                    0x12 = Remaining Time
                    0x09 = Voltage
                    0x0A = Current
                    0x08 = Temperature
                    0x0D = Charge Level
                    0x17 = Cycle Count
                    0x3F = Cell 1 Voltage
                    0x3E = Cell 2 Voltage
                    0x3D = Cell 3 Voltage
                val is the value in the register
"""

#----------------------------------------------------------------------------------
# Use Synapse Evaluation Board definitions 
from synapse.switchboard import *
from synapse.evalBase import *

BATTERY_ADDRESS = 0x16                 # SMB battery address 
retries = 4
secondCounter = 0
receivedData = 0


#----------------------------------------------------------------------------------
def startupEvent():
    """This is hooked into the HOOK_STARTUP event"""
    # Go ahead and redirect STDOUT to Portal now 
    ucastSerial( "\x00\x00\x01" )      # put your correct Portal address here! 
    crossConnect( DS_STDIO, DS_TRANSPARENT )
    setPinDir( 9, True )               # buzzer + 

#----------------------------------------------------------------------------------
def hexNibble( nibble ):
    '''Convert a numeric nibble 0x0-0xF to its ASCII string representation "0"-"F"'''
    hexStr = "0123456789ABCDEF"
    return hexStr[ nibble & 0xF ]

#----------------------------------------------------------------------------------
def printHex( byte ):
    '''print a byte in hex - input is an integer, not a string'''
    print hexNibble(byte >> 4),
    print hexNibble(byte),             # no trailing CR/LF 

#----------------------------------------------------------------------------------
def dumpHex( str ):
    '''dump a string of bytes in hex'''
    count = len( str )
    index = 0
    while index < count:
        printHex( ord( str[ index ] ) )
        index += 1
    print
    return ""

#----------------------------------------------------------------------------------
def tellBlinkLED():
         global blinktheLED
         blinktheLED = 1

#----------------------------------------------------------------------------------
def tellNoBlinkLED():
         global blinktheLED
         blinktheLED = 0

#----------------------------------------------------------------------------------
def tellSerialNumber():
    v1 = ""
    v1 = ReadSMBData( 0x16, 0x1C, 2 )
    print "SerialNumber: ", dumpHex( v1 )
    b = ord( v1[ 0 ] )
    b += ( ord( v1[ 1 ] ) * 256 )
    rpc( rpcSourceAddr(), 'SMBData', localAddr(), 1, b )
    
#----------------------------------------------------------------------------------
def tellFullChargeCapacity():
    v2 = ""
    v2 = ReadSMBData( 0x16, 0x10, 2 )
    print "FCC: ", dumpHex( v2 )
    b = ord( v2[ 0 ] )
    b += ( ord( v2[ 1 ] ) * 256 )
    rpc( rpcSourceAddr(), 'SMBData', localAddr(), 2, b )

#----------------------------------------------------------------------------------
def tellRemainingTime():
    v3 = ""
    v3 = ReadSMBData( 0x16, 0x12, 2 )
    print "RemainingTime: ", dumpHex( v3 )
    b = ord( v3[ 0 ] )
    b += ( ord( v3[ 1 ] ) * 256 )
    rpc( rpcSourceAddr(), 'SMBData', localAddr(), 3, b )
    
#----------------------------------------------------------------------------------
def tellVoltage():
    v4 = ""
    v4 = ReadSMBData( 0x16, 0x09, 2 )
    print "Voltage: ", dumpHex( v4 )
    b = ord( v4[ 0 ] )
    b += ( ord( v4[ 1 ] ) * 256 )
    rpc( rpcSourceAddr(), 'SMBData', localAddr(), 4, b )

#----------------------------------------------------------------------------------
def tellCurrent():
    v5 = ""
    v5 = ReadSMBData( 0x16, 0x0A, 2 )
    print "Current: ", dumpHex( v5 )
    b = ord( v5[ 0 ] )
    b += ( ord( v5[ 1 ] ) * 256 )
    rpc( rpcSourceAddr(), 'SMBData', localAddr(), 5, b )
    
#----------------------------------------------------------------------------------
def tellTemperature():
    v6 = ""
    v6 = ReadSMBData( 0x16, 0x08, 2 )
    print "Temperature: ", dumpHex( v6 )
    b = ord( v6[ 0 ] )
    b += ( ord( v6[ 1 ] ) * 256 )
    rpc( rpcSourceAddr(), 'SMBData', localAddr(), 6, b )
    
#----------------------------------------------------------------------------------
def tellChargeLevel():
    v7 = ""
    v7 = ReadSMBData( 0x16, 0x0D, 2 )
    print "ChargeLevel: ", dumpHex( v7 )
    b = ord( v7[ 0 ] )
    b += ( ord( v7[ 1 ] ) * 256 )
    rpc( rpcSourceAddr(), 'SMBData', localAddr(), 7, b )
    
#----------------------------------------------------------------------------------
def tellCycleCount():
    v8 = ""
    v8 = ReadSMBData( 0x16, 0x17, 2 )
    print "CycleCount: ", dumpHex( v8 )
    b = ord( v8[ 0 ] )
    b += ( ord( v8[ 1 ] ) * 256 )
    rpc( rpcSourceAddr(), 'SMBData', localAddr(), 8, b )
    
#----------------------------------------------------------------------------------
def tellCell1Voltage():
    v9 = ""
    v9 = ReadSMBData( 0x16, 0x3F, 2 )
    print "Cell1: ", dumpHex( v9 )
    b = ord( v9[ 0 ] )
    b += ( ord( v9[ 1 ] ) * 256 )
    rpc( rpcSourceAddr(), 'SMBData', localAddr(), 9, b )
    
#----------------------------------------------------------------------------------
def tellCell2Voltage():
    v10 = ""
    v10 = ReadSMBData( 0x16, 0x3E, 2 )
    print "Cell2: ", dumpHex( v10 )
    b = ord( v10[ 0 ] )
    b += ( ord( v10[ 1 ] ) * 256 )
    rpc( rpcSourceAddr(), 'SMBData', localAddr(), 10, b )
    
#----------------------------------------------------------------------------------
def tellCell3Voltage():
    v11 = ""
    v11 = ReadSMBData( 0x16, 0x3D, 2 )
    print "Cell3: ", dumpHex( v11 )
    b = ord( v11[ 0 ] )
    b += ( ord( v11[ 1 ] ) * 256 )
    rpc( rpcSourceAddr(), 'SMBData', localAddr(), 11, b )
    
#----------------------------------------------------------------------------------
#----------------------------------------------------------------------------------
def doEverySecond():
    """Tasks that are executed every second"""
    global deviceType, blinktheLED
    blinkDurationMs = 200
    if deviceType != "Stick":
        if blinktheLED == 1:
            blinkLed( blinkDurationMs )
       
#----------------------------------------------------------------------------------
def timer100msEvent( currentMs ):
    """Hooked into the HOOK_100MS event"""
    global secondCounter

    secondCounter += 1
    if secondCounter >= 10:
        doEverySecond()
        secondCounter = 0




#----------------------------------------------------------------------------------
#--- SMB Routines -----------------------------------------------------------------
#----------------------------------------------------------------------------------

#**********************************************************************************
#	 waitSome											  10/10/08
#  Description: Brief delay between pin assignments 
#   Parameters: counts to delay 
# Return Value: 
#   Processing: 
#    Called By: 
#     Comments: 
#**********************************************************************************

def waitSome( delayCount ):		       # brief delay 
    index = 0
    while ( index < delayCount ):
        index += 1
    return
#--- end of waitSome() ------------------------------------------------------------




#**********************************************************************************
#    SMBStart                                              10/10/08
#  Description: Send  bus start condition.
#   Parameters: 
# Return Value: 
#   Processing: 
#    Called By: ReadSMBData()
#     Comments: Data goes low while Clock is high
#**********************************************************************************

def SMBStart():
    setPinDir( 17, False )
    waitSome( 10 )
    setPinDir( 18, False )
    waitSome( 10 )
    if ( readPin( 17 ) == 0 ):
        return ( 1 )
    if ( readPin( 18 ) == 0 ):         # test if clock is low
        if ( SMBClockTest() ):         # wait on clock for a short time
            return ( 1 )               # return with error condition        
    writePin( 17, False )              # set data pin latch to 0
    setPinDir( 17, True )              # set pin to output to drive low
    waitSome( 10 )

    return ( 0 )					   # no error 
#--- end of SMBStart() ------------------------------------------------------------




#**********************************************************************************
#    SMBRestart                                             10/10/08
#  Description: Send  bus restart condition.
#   Parameters: 
# Return Value: 
#   Processing: 
#    Called By: ReadSMBData()
#     Comments: Data goes low while Clock is high
#**********************************************************************************

def SMBRestart():
    writePin( 18, False )              # set clock pin latch to 0
    setPinDir( 18, True )              # set clock pin to output to drive low
    waitSome( 10 )
    setPinDir( 17, False )             # release data pin to float high
    waitSome( 10 )
    setPinDir( 18, False )             # release clock pin to float high
    waitSome( 10 )
    writePin( 17, False )              # set data pin latch to 0
    setPinDir( 17, True )              # set data pin output to drive low
    waitSome( 10 )
#--- end of SMBRestart() ----------------------------------------------------------




#**********************************************************************************
#    SMBStop                                                 10/10/08
#  Description: Send  bus stop condition.
#   Parameters: 
# Return Value: 
#   Processing: 
#    Called By: ReadSMBData()
#     Comments: Data goes high while Clock is high
#**********************************************************************************

def SMBStop():
    writePin( 18, False )              # set clock pin latch to 0
    setPinDir( 18, True )              # set clock pin to output to drive low
    waitSome( 10 )
    writePin( 17, False )              # set data pin latch to 0
    setPinDir( 17, True )              # set data pin output to drive low
    waitSome( 10 )
    setPinDir( 18, False )             # release clock pin to float high
    waitSome( 10 )
    setPinDir( 17, False )             # release data pin to float high
    waitSome( 10 )
#--- end of SMBStop() -------------------------------------------------------------




#**********************************************************************************
#    SMBWrite                                                 10/10/08
#  Description: This routine writes a single byte to the  bus. 
#   Parameters: Single data byte for  bus. 
# Return Value: error condition if bus error occurred 
#   Processing: 
#    Called By: ReadSMBData()
#     Comments: Data must be stable when Clock goes high
#**********************************************************************************

def SMBWrite( data_out ):
    numBits = 8                        # initialize bit counter
    writePin( 18, False )              # set latch to 0

    while ( numBits > 0 ):
        if ( readPin( 18 ) == 0 ):     # test if clock is low
            if ( SMBClockTest() ):     # wait on clock for a short time
                return ( 1 )           # return with error condition        
        else:
            if ( data_out & 0x80 ):
                setPinDir( 18, True )  # set clock pin output to drive low
                waitSome( 10 )
                setPinDir( 17, False ) # release data line to float high 
                waitSome( 10 )
                setPinDir( 18, False ) # release clock line to float high 
                waitSome( 10 )
            else:                      # transmit out logic 0
                setPinDir( 18, True )  # set clock pin output to drive low
                waitSome( 10 )
                writePin( 17, False )  # set data pin latch to 0
                setPinDir( 17, True )  # set data pin output to drive low 
                waitSome( 10 )
                setPinDir( 18, False ) # release clock line to float high 
                waitSome( 10 )

        data_out = data_out << 1
        numBits -= 1

    return ( 0 )                       # return with no error
#--- end of SMBWrite() ------------------------------------------------------------




#**********************************************************************************
#    SMBRead                                                  10/10/08
#  Description: Read single byte from  bus. 
#   Parameters: 
# Return Value: data byte or error condition 
#   Processing: 
#    Called By: ReadSMBData()
#     Comments: 
#**********************************************************************************

def SMBRead():
    dataHi = 0
    dataLo = 0
    count = 0
    global receivedData
    receivedData = 0
    numBits = 8                        # set bit count for byte 

    writePin( 18, False )              # set clock pin latch to 0

    while ( numBits > 0 ):
        setPinDir( 18, True )          # set clock pin output to drive low
        waitSome( 10 )
        setPinDir( 17, False )         # release data line to float high
        waitSome( 10 )
        setPinDir( 18, False )         # release clock line to float high 
        waitSome( 10 )

        if ( readPin( 18 ) == 0 ):     # test for clock low 
            if ( SMBClockTest() ):     # 30 cycles clock wait routine 
                return ( 1 )           # return with error condition 

        receivedData = receivedData << 1   # shift byte by 1 

        dataHi = 0
        dataLo = 0
        count = 0

        while ( count < 5 ):
            if ( readPin( 17 ) == 1 ): # is data line high
                dataHi += 1
            else:
                dataLo += 1
            count += 1

        if ( dataHi > dataLo ):
            receivedData |= 0x01       # set bit 0 to logic 1
        else:
            receivedData &= ~0x01

        numBits -= 1                   # stay until 8 bits have been acquired

    return ( 0 )                       # return with no error
#--- end of SMBRead() -------------------------------------------------------------




#**********************************************************************************
#    SMBClockTest                                              10/10/08
#  Description: This function allows for a slave device 
#               to stretch the clock low. 
#   Parameters: 
# Return Value: error condition status 
#   Processing: 
#    Called By: SMBStart(), SMBWrite(), SMBRead()
#     Comments: 
#**********************************************************************************

def SMBClockTest():
    loop_count = 255
    while ( loop_count > 1 ):
        if ( readPin( 18 ) ):
            return ( 0 )               # return with no error
        loop_count -= 1
        waitSome( 10 )
    return ( 1 )                       # return with clock error
#--- end of SMBClockTest() --------------------------------------------------------




#**********************************************************************************
#    SMBAck                                                    10/10/08
#  Description: This function generates a bus acknowledge sequence. 
#   Parameters: 
# Return Value: error condition status 
#   Processing: 
#    Called By: ReadSMBData()
#     Comments: 
#**********************************************************************************

def SMBAck():
    writePin( 18, False )              # set clock pin latch to 0  
    setPinDir( 18, True )              # set clock pin to output to drive low
    waitSome( 10 )
    setPinDir( 17, False )             # release data line to float high 
    waitSome( 10 )
    setPinDir( 18, False )             # release clock line to float high
    waitSome( 10 )

    if ( readPin( 17 ) ):              # error if ack = 1, slave did not ack
        return ( 1 )                   # return with acknowledge error
    else:
        return ( 0 )                   # return with no error
#--- end of SMBAck() --------------------------------------------------------------




#**********************************************************************************
#    ReadSMBData                                             10/10/08
#  Description: Bit-bangs the  bus.
#               Retrieves the contents of one SMB register.
#   Parameters: address  - SMB address, 0x16 for SMB battery 
#               command  - desired register 
#               numBytes - number of bytes to retrieve 
# Return Value: data read as a string 
#   Processing: 
#    Called By: 
#     Comments: Data must be stable when Clock goes high
#       Sample: ReturnBuff = ReadSMBData( 0x16, 0x10, 2 )  # FCC 
#**********************************************************************************

def ReadSMBData( address, command, numBytes ):
    global receivedData
    returnData = ""
    SMBStart()
    SMBWrite( address )                # write address 
    SMBAck()
    SMBWrite( command )                # write command 
    SMBAck()
    waitSome( 3 )
    SMBRestart()                       # generate  bus restart condition

    SMBWrite( address | 0x01 )         # WRITE 1 byte - R/W bit should be 1 for read
    SMBAck()

    while ( numBytes > 0 ):            # read numBytes
        numBytes -= 1
        if ( SMBRead() == 0 ):
            returnData += chr ( receivedData )
        else:
            SMBStop()
            return ( 1 )               # return with error

        if ( numBytes == 0 ):          # initiate NOT ACK
            setPinDir( 18, True )      # make clock pin output to drive low
            waitSome( 3 )
            setPinDir( 17, False )     # release data line to float high 
            waitSome( 10 )
            setPinDir( 18, False )     # release clock line to float high 
            waitSome( 3 )
        else:                          # else initiate ACK condition
            setPinDir( 18, True )      # make clock pin output to drive low
            waitSome( 3 )
            writePin( 17, False )      # set data pin latch to 0
            setPinDir( 17, True )      # make data pin output to drive low
            waitSome( 10 )
            setPinDir( 18, False )     # release clock line to float high 
            waitSome( 3 )

    SMBStop()

    return ( returnData )              # return with no error
#--- end of ReadSMBData() ---------------------------------------------------------


#----------------------------------------------------------------------------------
# Set event hook functions
snappyGen.setHook( SnapConstants.HOOK_STARTUP, startupEvent )
snappyGen.setHook( SnapConstants.HOOK_100MS, timer100msEvent )


#--- end of ReadSMB.py ------------------------------------------------------------

