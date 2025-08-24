"""
Navigation Module Example 
-----------------------------------------------------------

Purpose:
- Demonstrate keypad (NeoTrellis) and four switch inputs on a microcontroller.
- Provide visual feedback on the keypad and transmit events over UART.
- Match simple 4-key codes (four predefined sequences).

- This file is a generic educational example. It does not reference or describe
  any proprietary project, installation, or third-party IP.

Author: Austin Zercher
Date: 2025
-----------------------------------------------------------
"""

import time
import board
import busio
import digitalio
import random

import adafruit_trellis.express.m4_trellis as trellis_module

# Create the trellis instance
trellis = trellis_module.M4_Trellis_Express()

# Set up UART
uart = busio.UART(board.TX, board.RX, baudrate=9600)

# Set up switches
switch1 = digitalio.DigitalInOut(board.A2)
switch1.direction = digitalio.Direction.INPUT
switch1.pull = digitalio.Pull.DOWN

switch2 = digitalio.DigitalInOut(board.A1)
switch2.direction = digitalio.Direction.INPUT
switch2.pull = digitalio.Pull.DOWN

switch3 = digitalio.DigitalInOut(board.A0)
switch3.direction = digitalio.Direction.INPUT
switch3.pull = digitalio.Pull.DOWN

switch4 = digitalio.DigitalInOut(board.A3)
switch4.direction = digitalio.Direction.INPUT
switch4.pull = digitalio.Pull.DOWN

# Initialize last switch states for debouncing
last_switch_states = [False, False, False, False]
switches = [switch1, switch2, switch3, switch4]

# Define codes (unchanged)
code1 = [0, 1, 2, 3]
code2 = [4, 5, 6, 7]
code3 = [8, 9, 10, 11]
code4 = [12, 13, 14, 15]

Input = []
count = 0
matching = False

def random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

# Main loop (unchanged logic)
while True:
    pressed = trellis.pressed_keys

    if pressed:
        for p in pressed:
            if p not in Input:
                Input.append(p)
                count += 1
                trellis.pixels[p] = random_color()

    if count == 4:
        if Input == code1:
            matching = True
            uart.write((f"Navi:Code:{Input}\n").encode())
        elif Input == code2:
            matching = True
            uart.write((f"Navi:Code:{Input}\n").encode())
        elif Input == code3:
            matching = True
            uart.write((f"Navi:Code:{Input}\n").encode())
        elif Input == code4:
            matching = True
            uart.write((f"Navi:Code:{Input}\n").encode())

        if not matching:
            for i in Input:
                trellis.pixels[i] = (255, 0, 0)
            time.sleep(0.5)
            for i in Input:
                trellis.pixels[i] = (0, 0, 0)
            count = 0
            Input = []
        else:
            matching = False
            count = 0
            Input = []

    # Debounced switch handling
    for i, switch in enumerate(switches):
        if switch.value and not last_switch_states[i]:
            print(f"switch {i+1} pressed")
            uart.write((f"Navi:Switch{i+1}:True\n").encode())
            last_switch_states[i] = True
        elif not switch.value:
            last_switch_states[i] = False

    time.sleep(0.3)