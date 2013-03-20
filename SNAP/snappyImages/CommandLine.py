# Copyright (C) 2011 Synapse Wireless, Inc.
# Subject to your agreement of the disclaimer set forth below, permission is given by Synapse Wireless, Inc. ("Synapse") to you to freely modify, redistribute or include this SNAPpy code in any program. The purpose of this code is to help you understand and learn about SNAPpy by code examples.
# BY USING ALL OR ANY PORTION OF THIS SNAPPY CODE, YOU ACCEPT AND AGREE TO THE BELOW DISCLAIMER. If you do not accept or agree to the below disclaimer, then you may not use, modify, or distribute this SNAPpy code.
# THE CODE IS PROVIDED UNDER THIS LICENSE ON AN "AS IS" BASIS, WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, WITHOUT LIMITATION, WARRANTIES THAT THE COVERED CODE IS FREE OF DEFECTS, MERCHANTABLE, FIT FOR A PARTICULAR PURPOSE OR NON-INFRINGING. THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE COVERED CODE IS WITH YOU. SHOULD ANY COVERED CODE PROVE DEFECTIVE IN ANY RESPECT, YOU (NOT THE INITIAL DEVELOPER OR ANY OTHER CONTRIBUTOR) ASSUME THE COST OF ANY NECESSARY SERVICING, REPAIR OR CORRECTION. UNDER NO CIRCUMSTANCES WILL SYNAPSE BE LIABLE TO YOU, OR ANY OTHER PERSON OR ENTITY, FOR ANY LOSS OF USE, REVENUE OR PROFIT, LOST OR DAMAGED DATA, OR OTHER COMMERCIAL OR ECONOMIC LOSS OR FOR ANY DAMAGES WHATSOEVER RELATED TO YOUR USE OR RELIANCE UPON THE SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGES OR IF SUCH DAMAGES ARE FORESEEABLE. THIS DISCLAIMER OF WARRANTY AND LIABILITY CONSTITUTES AN ESSENTIAL PART OF THIS LICENSE. NO USE OF ANY COVERED CODE IS AUTHORIZED HEREUNDER EXCEPT UNDER THIS DISCLAIMER.

'''SNAPpy Command Line Demo
    Sample SNAPpy script to demonstrate one method of implementing a simple command line interface.
    This script is intended to be used with the SN111/SN163 evaluation boards.
    Connect a serial cable to the RS-232 port and open a connection at 38,400 baud, N,8,1.
    
    NOTE:  This script captures UART1 for the CLI.  DO NOT LOAD ON YOUR BRIDGE unless your PacketSerial
           connection is via UART0.
'''

from synapse.evalBase import *
from synapse.switchboard import *
from synapse.sysInfo import *

@setHook(HOOK_STARTUP)
def startupEvent():
    detectEvalBoards()
    crossConnect(DS_STDIO, DS_UART1)
    initUart(1, 38400)
    stdinMode(0, True)      # Line Mode, Echo On

    stdinEvent('?')

def getCmdArg(input):
    """Parse out a single int or string argument from given command-line input"""
    global cmd, arg
    cmd = ''
    arg = None
    i = 0
    while i < len(input):
        c = input[i]
        if c == ' ':
            if '0' <= input[i+1] <= '9':
                arg = int(input[i:])
                input = cmd
            else:
                arg = input[i+1:]
                input = cmd
            break

        cmd += c
        i += 1
  
@setHook(HOOK_STDIN)    
def stdinEvent(data):
    ''' Process command line input '''
    global cmd, arg

    if data == '?':
        help()
    elif len(data):
        getCmdArg(data)
        ret = None
        print
        
        if arg != None:
            ret = cmd(arg)
        else:
            ret = cmd()
    
        if ret != None:
            print " => ", ret
            
    print "\r\n>",

#----- The following are some simple functions for us to easily invoke from CLI -----

def help():
    print "\r\nThis sample CLI can call any SNAPpy function."
    print "Enter a function name [' ' + optional argument]"

def ver():
    print "SNAP v", getInfo(SI_TYPE_VERSION_MAJOR), '.', getInfo(SI_TYPE_VERSION_MINOR)
    print "Device Type: ", deviceType
    
def led(pinState):
    setPinDir(LED_PIN, True)
    writePin(LED_PIN, pinState)

def echo(text):
    print text
        
def disp(num):
    display2digits(num)

def beep(ms):
    pulsePin(PROTO_BUZZER_PIN, ms, True)

