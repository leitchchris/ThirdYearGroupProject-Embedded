# Copyright (C) 2011 Synapse Wireless, Inc.
# Subject to your agreement of the disclaimer set forth below, permission is given by Synapse Wireless, Inc. ("Synapse") to you to freely modify, redistribute or include this SNAPpy code in any program. The purpose of this code is to help you understand and learn about SNAPpy by code examples.
# BY USING ALL OR ANY PORTION OF THIS SNAPPY CODE, YOU ACCEPT AND AGREE TO THE BELOW DISCLAIMER. If you do not accept or agree to the below disclaimer, then you may not use, modify, or distribute this SNAPpy code.
# THE CODE IS PROVIDED UNDER THIS LICENSE ON AN "AS IS" BASIS, WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, WITHOUT LIMITATION, WARRANTIES THAT THE COVERED CODE IS FREE OF DEFECTS, MERCHANTABLE, FIT FOR A PARTICULAR PURPOSE OR NON-INFRINGING. THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE COVERED CODE IS WITH YOU. SHOULD ANY COVERED CODE PROVE DEFECTIVE IN ANY RESPECT, YOU (NOT THE INITIAL DEVELOPER OR ANY OTHER CONTRIBUTOR) ASSUME THE COST OF ANY NECESSARY SERVICING, REPAIR OR CORRECTION. UNDER NO CIRCUMSTANCES WILL SYNAPSE BE LIABLE TO YOU, OR ANY OTHER PERSON OR ENTITY, FOR ANY LOSS OF USE, REVENUE OR PROFIT, LOST OR DAMAGED DATA, OR OTHER COMMERCIAL OR ECONOMIC LOSS OR FOR ANY DAMAGES WHATSOEVER RELATED TO YOUR USE OR RELIANCE UPON THE SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGES OR IF SUCH DAMAGES ARE FORESEEABLE. THIS DISCLAIMER OF WARRANTY AND LIABILITY CONSTITUTES AN ESSENTIAL PART OF THIS LICENSE. NO USE OF ANY COVERED CODE IS AUTHORIZED HEREUNDER EXCEPT UNDER THIS DISCLAIMER.

"""Doodle Pad Controller for the ZIC2410
   This script is to be used with the ZIC2410 Eval board
   Turning the pots will result in an ouput on the ZIC2410-LCD board"""
padFound = False # Has a board with a doodle pad (LCD) been found
padAddr = None # Address of the doodle pad
curr_lf_rt_val = 0 
curr_up_dn_val = 0
plotEnabled = False
TX_LED = 3

def startup():
    global plotEnabled
    # look for a doodlePad
    mcastRpc(1,1, "askPad")
    mcastRpc(1,1, "lcdPlot")    
    # Initialize "INT0" GPIO as an "enable" button input
    setPinDir(18, False)
    setPinPullup(18, True)
    monitorPin(18, True)
    # Initialize "INT2" GPIO as an "clear" button input
    setPinDir(19, False)
    setPinPullup(19, True)
    monitorPin(19, True)
    # Intialize the tx-enable pin
    setPinDir(TX_LED, True)
    writePin(TX_LED, plotEnabled)
    
def tellPad():
    """Function called by the doodle pad (LCD board)"""
    global padAddr
    padAddr = rpcSourceAddr()
    
def buttonEvent(pin, isSet):
    global plotEnabled
    if not isSet:
        if pin == 18:
            enablePlot(not plotEnabled)
        if pin == 19:
            if padAddr:
                rpc(padAddr, "lcdPlot")
            else:
                mcastRpc(1,1, "lcdPlot")

def enablePlot(yesNo):
    """Enable/Disable the plot transmissions"""
    global plotEnabled
    plotEnabled = yesNo
    writePin(TX_LED, plotEnabled)
    
def timer100msEvent(currentMs):
    global padAddr, plotEnabled
    # The LCD is 64 pixels high and 128 pixels wide; ADC readings 0-255
    lf_rt_val = readAdc(0) # Pot 1 is left/right 
    up_dn_val = readAdc(1) # Pot 2 is up/down 

    if plotEnabled:
        if padAddr:
            rpc(padAddr, "lcdPlot", lf_rt_val/2, up_dn_val/4, True)
        else:
            mcastRpc(1,1, "lcdPlot", lf_rt_val/2, up_dn_val/4, True)
      
        
# Set event hook functions
snappyGen.setHook(SnapConstants.HOOK_STARTUP, startup)
snappyGen.setHook(SnapConstants.HOOK_100MS, timer100msEvent)
snappyGen.setHook(SnapConstants.HOOK_GPIN, buttonEvent)