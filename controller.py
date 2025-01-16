import hid
import requests
import threading
import time
import math
from PCpanelInputClass import Panel
import subprocess
import ctypes
from HIDread import getHID

def decimal_to_hex(decimal_number):
    """
    Converts a decimal number to hexadecimal.
    
    Args:
        decimal_number (int): The decimal number to convert.
    
    Returns:
        str: The hexadecimal representation of the number.
    """
    if not isinstance(decimal_number, int):
        raise ValueError("Input must be an integer.")
    
    return hex(decimal_number).upper()  # Remove '0x' prefix and convert to uppercase

panel = Panel()

inputs = {}
"""
Joint ID key:
1: BASE_JOINT
2: SHOULDER_JOINT
3: ELBOW_JOINT
4: EOAT_JOINT

Each joint entry is structured as:
[jointId, total travel, startPos]
"""
inputs[0] = [0, 0, 0]
inputs[1] = [0, 0, 0]
inputs[2] = [1, -4, 2] 
inputs[3] = [0, 0, 0]
inputs[4] = [4, 1.3, 2]
inputs[5] = [2, 1, -0.3]
inputs[6] = [3, -1.2, 2]
inputs[7] = [0, 0, 0]
inputs[8] = [4, 1.3, 2]

ip_addr = '192.168.0.245'

vid, pid = getHID()
vid = decimal_to_hex(vid)
pid = decimal_to_hex(pid)

h = hid.device()
h.open(int(vid,16), int(pid,16))

# Non-blocking read
h.set_nonblocking(True)

user_input = 'start'

stopToggle = False

def toggle():
    global stopToggle
    toggled = False

    
# Function to get user input
def get_input():
    global user_input
    
    input_ = None
    while input_ != 'quit':
        input_ = None
        input_ = input()

        if input_ == None:
            pass
        elif input_ == 'stop':
            user_input = 'stop'
        elif input_ == 'start':
            user_input = 'start'
        
        if input_ != None:
            print(user_input)
            
    user_input = 'exit'

# Start the input thread
input_thread = threading.Thread(target=get_input, daemon=True)
input_thread.start()

def sendCommand(command, ip_addr = ip_addr):
    url = "http://" + ip_addr + "/js?json=" + command
    response = requests.get(url)
    content = response.text
    if content != 'null':
        print(f"error - {content}")
        exit()
    else:
        
        print(command)
logCount = 0
while True: 
   
    data = h.read(3)  # read up to 64 bytes
    
    if data:
        print(data)
        inputId = panel.update(data)
        newInput = panel.knobs[inputId] if inputId in panel.knobs else panel.sliders[inputId]
        print(newInput)
        newPos = max(min(newInput[2], 255), 0) # trim
        if inputId == 1:
            command = f"\"T\":114,\"led\":{newPos}"
            command = "{" + command + "}"

        else:
            newPos = newPos / 255 # normalize
            newPos = (newPos) * (inputs[inputId][1]) + (inputs[inputId][2])    #clamp
            command = f"\"T\":101,\"joint\":{(inputs[inputId][0])},\"rad\":{round(newPos, 2)},\"spd\":0,\"acc\":0"
            command = "{" + command + "}" 

        if inputId == 1 and newInput[0] == 2:
            print("click")
            if user_input != 'stop':
                user_input = 'stop'
            else:
                user_input = 'start'

        if user_input == 'start':
            print(user_input)
            sendCommand(command)
            logCount += 1
        elif user_input == 'stop':
            pass
        elif user_input == 'exit':
            break

    if logCount >= 20:
        subprocess.run("cls", shell= True)
        logCount = 0

input_thread.join()
