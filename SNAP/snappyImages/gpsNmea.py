# Copyright (C) 2011 Synapse Wireless, Inc.
# Subject to your agreement of the disclaimer set forth below, permission is given by Synapse Wireless, Inc. ("Synapse") to you to freely modify, redistribute or include this SNAPpy code in any program. The purpose of this code is to help you understand and learn about SNAPpy by code examples.
# BY USING ALL OR ANY PORTION OF THIS SNAPPY CODE, YOU ACCEPT AND AGREE TO THE BELOW DISCLAIMER. If you do not accept or agree to the below disclaimer, then you may not use, modify, or distribute this SNAPpy code.
# THE CODE IS PROVIDED UNDER THIS LICENSE ON AN "AS IS" BASIS, WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, WITHOUT LIMITATION, WARRANTIES THAT THE COVERED CODE IS FREE OF DEFECTS, MERCHANTABLE, FIT FOR A PARTICULAR PURPOSE OR NON-INFRINGING. THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE COVERED CODE IS WITH YOU. SHOULD ANY COVERED CODE PROVE DEFECTIVE IN ANY RESPECT, YOU (NOT THE INITIAL DEVELOPER OR ANY OTHER CONTRIBUTOR) ASSUME THE COST OF ANY NECESSARY SERVICING, REPAIR OR CORRECTION. UNDER NO CIRCUMSTANCES WILL SYNAPSE BE LIABLE TO YOU, OR ANY OTHER PERSON OR ENTITY, FOR ANY LOSS OF USE, REVENUE OR PROFIT, LOST OR DAMAGED DATA, OR OTHER COMMERCIAL OR ECONOMIC LOSS OR FOR ANY DAMAGES WHATSOEVER RELATED TO YOUR USE OR RELIANCE UPON THE SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGES OR IF SUCH DAMAGES ARE FORESEEABLE. THIS DISCLAIMER OF WARRANTY AND LIABILITY CONSTITUTES AN ESSENTIAL PART OF THIS LICENSE. NO USE OF ANY COVERED CODE IS AUTHORIZED HEREUNDER EXCEPT UNDER THIS DISCLAIMER.

"""GPS Interface: NMEA-0183 device connected to a ProtoBoard.

Intercept STDOUT in Portal to see GPS information in EventLog.

Decoded NMEA sentences:
 GPGGA (Fix Data) - time, lat, lon, fix, sats, precision, altitude,...
   Ex:  "$GPGGA,060055.000,0000.0000,N,00000.0000,E,0,00,99.0,0082.0,M,18.0,M,,*58"
 GPRMC (Transit Data) - time, status, lat, lon, speed, course, date,...
   Ex:  "$GPRMC,060055.000,V,0000.0000,N,00000.0000,E,0.0,0.0,280108,0.0,W,N*0A"
 GPGSA (Satellite Data)
   Ex:  "$GPGSA,A,1,,,,,,,,,,,,,99.0,99.0,99.0*00"

Max NMEA sentence length is 82 bytes.  Since that exceeds current stdin line-buffer limit (40),
we handle this in character mode.

"""

from synapse.evalBase import *
from synapse.switchboard import *

pollCount = 0
enableState = False

# Hardware configuration:
#   UART0 connected to GPS serial out (TXO)
#   GPS_ENABLE_PIN connected to GPS active high enable (ENABLE)

GPS_ENABLE_PIN = GPIO_7

@setHook(HOOK_STARTUP)
def startup():
    initProtoHw()
    monitorPin(BUTTON_PIN, True)
    setPinDir(GPS_ENABLE_PIN, True)
    writePin(GPS_ENABLE_PIN, True)
    initUart(0, 4800)
    stdinMode(1, False)   # Char mode, no echo
    
    # Connect GPS serial output to STDIN, where our event handler will parse the messages
    crossConnect(DS_UART0, DS_STDIO)

@setHook(HOOK_100MS)
def poll100ms(msTick):
    global pollCount
    pollCount += 1
    if pollCount & 1:
        blinkLed(50)
        
    # Dump info every 5 seconds
    if (pollCount % 50) == 0:
        dumpGpsInfo()

@setHook(HOOK_GPIN)
def buttonEvent(pin, isSet):
    """Button press enables / disables GPS module"""
    global enableState
    if not isSet:
        enableState = not enableState
        writePin(GPS_ENABLE_PIN, enableState)
        writePin(1, enableState)  # Green LED reflects state

def dumpGpsInfo():
    global utc_hr, utc_min, utc_sec, utc_ms
    global lat_deg, lat_min, lat_frac_min, lat_sec, curTok
    global lng_deg, lng_min, lng_frac_min, lng_sec, curTok
    global numSatellites, altitude, fixStat

    print 'Time: ', utc_hr, ':', utc_min, ':', utc_sec
    print 'Latitude:  ', lat_deg, 'd ', lat_min, 'm ', lat_sec, 's - ', lat_pole
    print 'Longitude: ', lng_deg, 'd ', lng_min, 'm ', lng_sec, 's - ', lng_meridian
    print 'Altitude:  ', altitude
    print numSatellites, ' sats, ', 'fix ok.' if fixStat else 'no fix.'


# Time
utc_hr = 0
utc_min = 0
utc_sec = 0
utc_ms = 0

# Latittude
lat_deg = 0
lat_min = 0
lat_frac_min = 0
lat_sec = 0
lat_pole = None

# Longitude
lng_deg = 0
lng_min = 0
lng_frac_min = 0
lng_sec = 0
lng_meridian = None

fixStat = 0          # nonzero is valid fix
numSatellites = 0    # 0-12
altitude = 0


def parseTime():
    global utc_hr, utc_min, utc_sec, utc_ms, curTok
    utc_hr = int(curTok[:2])
    utc_min = int(curTok[2:4])
    utc_sec = int(curTok[4:6])
    utc_ms = int(curTok[7:])
    

def parseLat():
    global lat_deg, lat_min, lat_frac_min, lat_sec, curTok
    lat_deg = int(curTok[:2])
    lat_min = int(curTok[2:4])
    lat_frac_min = int(curTok[5:])
    lat_sec = (int(curTok[5:8]) * 6) / 100
    
def parseLon():
    global lng_deg, lng_min, lng_frac_min, lng_sec, curTok
    lng_deg = int(curTok[:3])
    lng_min = int(curTok[3:5])
    lng_frac_min = int(curTok[6:])
    lng_sec = (int(curTok[6:9]) * 6) / 100
    

# States:
#   0 - Idle
#   1 - Sentence ID
#   2 - GPGGA: time
#   3 - GPGGA: latitude
#   4 - GPGGA: N/S
#   5 - GPGGA: longitude
#   6 - GPGGA: E/W
#   7 - GPGGA: Fix
#   8 - GPGGA: # satellites
#   9 - GPGGA: HDOP
#   10 - GPGGA: altitude

state = 0
curTok = ''

def procTok(curToken):
    """Process NMEA tokens"""
    global state
    global lat_pole, lng_meridian
    global fixStat, numSatellites, altitude

    if state == 1:
        if curToken == 'GPGGA':
            state = 2
        elif curToken == 'GPRMC':
            state = 20
        elif curToken == 'GPGSA':
            state = 40
        else:
            state = 0
    elif state == 2:
        if len(curToken) == 10:
            parseTime()
            state = 3
        else:
            state = 0
    elif state == 3:
        if len(curToken) == 9:
            parseLat()
            state = 4
        else:
            state = 0
    elif state == 4:
        if len(curToken) == 1:
            lat_pole = 'N' if curToken == 'N' else 'S'
            state = 5
        else:
            state = 0
    elif state == 5:
        if len(curToken) == 10:
            parseLon()
            state = 6
        else:
            state = 0
    elif state == 6:
        if len(curToken) == 1:
            lng_meridian = 'E' if curToken == 'E' else 'W'
            state = 7
        else:
            state = 0
    elif state == 7:
        fixStat = int(curToken)
        state = 8
    elif state == 8:
        numSatellites = int(curToken)
        state = 9
    elif state == 9:
        # Discard HDOP
        state = 10
    elif state == 10:
        altitude = int(curToken)
        state = 0
    else:
        state = 0
        

@setHook(HOOK_STDIN)
def stdinEvent(buf):
    """Receive handler for character input on UART0.
       The parameter 'buf' will contain one or more received characters. 
    """
    global state, curTok
    n = len(buf)
    i = 0
    while(i < n):
        c = buf[i]
        i += 1
        
        if len(curTok) > 20:
            state = 0
        if state == 0:
            # Look for 'start' delimiter
            if c == '$':
                state = 1
                
        else:
            # Look for 'token' delimiter
            if c == ',' or c == '\r':
                procTok(curTok)
                curTok = ''
            else:
                # Accumulate characters to build next token
                curTok += c


