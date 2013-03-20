'''
This program and the accompanying materials are
made available under the terms of the Eclipse Public License v1.0
which accompanies this distribution, and is available at
http://www.eclipse.org/legal/epl-v10.html
Contributor: Synapse Wireless Inc., Huntsville, Alabama, 35806, USA
'''

setDisable = 0
pre_shared_pass = "ourPass" # hard-coded password

def Enable_lock(password):
    '''Enable the lockdown by providing the correct password'''
    if password == pre_shared_pass:
        saveNvParam(52, 1)
        reboot()
    
def Disable_lock(password):
    '''Disable the lockdown by providing the correct password'''
    global setDisable
    # You cannot directly set the lockdown from an over-the-air RPC
    # Instead, set a flag for the next timer hook
    if password == pre_shared_pass:
        setDisable = 1 

@setHook(HOOK_1S)
def timer_1sec():
    '''One Second Event'''
    global setDisable
    if setDisable:
        setDisable = 0
        # This can only be set indirectly
        saveNvParam(52,0)
        reboot()