"""
E10example.py - just an example for a SNAP Engine running INSIDE an E10
"""
from synapse.platforms import *

# The SNAP Engine controls an LED labeled "A" on the "wireless" end of the unit
# (next to the MODE button)
LED_A_GREEN = GPIO_0
LED_A_RED = GPIO_1

@setHook(HOOK_STARTUP)
def startup():
    setPinDir(LED_A_GREEN, True)
    setPinDir(LED_A_RED, True)
    setLedAGreen()

def setLedAOff():
    writePin(LED_A_GREEN, False)
    writePin(LED_A_RED, False)

def setLedAGreen():
    writePin(LED_A_GREEN, True)
    writePin(LED_A_RED, False)

def setLedARed():
    writePin(LED_A_GREEN, False)
    writePin(LED_A_RED, True)

def setLedAYellow():
    writePin(LED_A_GREEN, True)
    writePin(LED_A_RED, True)
