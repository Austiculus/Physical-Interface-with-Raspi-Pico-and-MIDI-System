"""
Pilot Module Example
-----------------------------------------------------------

Purpose:
- Drive two banks of GPIO-connected indicator lights (left/right).
- React to two input switches with simple light animations.
- Report switch events over UART.

- Provided as a general, educational example with no references to any
  proprietary or third-party project.
  
Author: Austin Zercher
Date: 2025
-----------------------------------------------------------
"""

import time
import digitalio
from analogio import AnalogIn  # (kept if needed later; original code had commented ADC)
import busio
import board

# Set Light GPIO pins
L1 = digitalio.DigitalInOut(board.GP16); L1.direction = digitalio.Direction.OUTPUT
L2 = digitalio.DigitalInOut(board.GP17); L2.direction = digitalio.Direction.OUTPUT
L3 = digitalio.DigitalInOut(board.GP18); L3.direction = digitalio.Direction.OUTPUT
L4 = digitalio.DigitalInOut(board.GP19); L4.direction = digitalio.Direction.OUTPUT
L5 = digitalio.DigitalInOut(board.GP20); L5.direction = digitalio.Direction.OUTPUT
L6 = digitalio.DigitalInOut(board.GP21); L6.direction = digitalio.Direction.OUTPUT
L7 = digitalio.DigitalInOut(board.GP26); L7.direction = digitalio.Direction.OUTPUT
L8 = digitalio.DigitalInOut(board.GP28); L8.direction = digitalio.Direction.OUTPUT

R1 = digitalio.DigitalInOut(board.GP13); R1.direction = digitalio.Direction.OUTPUT
R2 = digitalio.DigitalInOut(board.GP11); R2.direction = digitalio.Direction.OUTPUT
R3 = digitalio.DigitalInOut(board.GP9);  R3.direction = digitalio.Direction.OUTPUT
R4 = digitalio.DigitalInOut(board.GP8);  R4.direction = digitalio.Direction.OUTPUT
R5 = digitalio.DigitalInOut(board.GP5);  R5.direction = digitalio.Direction.OUTPUT
R6 = digitalio.DigitalInOut(board.GP4);  R6.direction = digitalio.Direction.OUTPUT
R7 = digitalio.DigitalInOut(board.GP3);  R7.direction = digitalio.Direction.OUTPUT
R8 = digitalio.DigitalInOut(board.GP2);  R8.direction = digitalio.Direction.OUTPUT

leftLights = [L1, L2, L3, L4, L5, L6, L7, L8]
rightLights = [R1, R2, R3, R4, R5, R6, R7, R8]

# Switch inputs
engLSwitch = digitalio.DigitalInOut(board.GP7)
engLSwitch.direction = digitalio.Direction.INPUT
engLSwitch.pull = digitalio.Pull.DOWN

engRSwitch = digitalio.DigitalInOut(board.GP6)
engRSwitch.direction = digitalio.Direction.INPUT
engRSwitch.pull = digitalio.Pull.DOWN

# UART
uart = busio.UART(board.GP0, board.GP1, baudrate=9600)

# Light helpers (unchanged)
def lightUp(lightList):
    for i in lightList:
        i.value = True
        time.sleep(.4)

def lightDown(lightList):
    for i in reversed(lightList):
        i.value = False
        time.sleep(.4)

# State/timing (unchanged)
timeUpdateL = time.monotonic()
timeUpdateR = time.monotonic()
flippedL = False
flippedR = False

# Main loop (unchanged logic)
while True:
    now = time.monotonic()

    if engLSwitch.value and (flippedL == False) and (now - timeUpdateL >= 3):
        lightUp(leftLights)
        flippedL = True
        timeUpdateL = now
        print("Left Engine Engaged!")
        uart.write(("Pilot:LEngineSwitchOn\n").encode())

    if engRSwitch.value and (flippedR == False) and (now - timeUpdateR >= 3):
        lightUp(rightLights)
        flippedR = True
        timeUpdateR = now
        print("Right Engine Engaged!")
        uart.write(("Pilot:REngineSwitchOn\n").encode())

    if (engLSwitch.value == False) and (flippedL == True) and (now - timeUpdateL >= 3):
        lightDown(leftLights)
        flippedL = False
        timeUpdateL = now
        print("Left Engine Disengaged!")
        uart.write(("Pilot:LEngineSwitchOff\n").encode())

    if (engRSwitch.value == False) and (flippedR == True) and (now - timeUpdateR >= 3):
        lightDown(rightLights)
        flippedR = False
        timeUpdateR = now
        print("Right Engine Disengaged!")
        uart.write(("Pilot:REngineSwitchOff\n").encode())