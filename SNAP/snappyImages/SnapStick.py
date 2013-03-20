"""Standard reference script for SnapStick - Sets LED green and pulses on USB rx data"""

# LEDs are active-low
RED_LED = 5
GRN_LED = 6

STAT_UART1_RX = 3

@setHook(HOOK_STARTUP)
def init():
    setPinDir(GRN_LED, True)
    setPinDir(RED_LED, True)
    
    writePin(GRN_LED, False)
    writePin(RED_LED, True)

@setHook(HOOK_100MS)
def tick():
    if getStat(STAT_UART1_RX) > 0:
        pulsePin(RED_LED, 50, False)

