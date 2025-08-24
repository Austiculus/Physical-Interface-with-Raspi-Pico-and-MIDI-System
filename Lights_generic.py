"""
Randomized Lighting Panel Example
-----------------------------------------------------------

Purpose:
- Randomly activate a subset of GPIO-connected LEDs, hold for a short time,
  then clear and repeat.

- Written for MicroPython (uses `machine.Pin`).
- This is a general educational example with no proprietary identifiers.
- Pin mapping preserved to match the original logic.

Author: Austin Zercher
Date: 2025
-----------------------------------------------------------
"""

from machine import Pin
import time
import random

Seconds = 0
numLED = 0
activeLED = []

# Top Left Pins
p1 = Pin(28, Pin.OUT)
p2 = Pin(27, Pin.OUT)
p3 = Pin(26, Pin.OUT)
p4 = Pin(22, Pin.OUT)

# Top Right Pins
p5 = Pin(19, Pin.OUT)
p6 = Pin(18, Pin.OUT)
p7 = Pin(17, Pin.OUT)
p8 = Pin(16, Pin.OUT)

# Bottom Pins
p9  = Pin(2, Pin.OUT)
p10 = Pin(3, Pin.OUT)
p11 = Pin(4, Pin.OUT)
p12 = Pin(5, Pin.OUT)
p13 = Pin(10, Pin.OUT)
p14 = Pin(11, Pin.OUT)
p15 = Pin(12, Pin.OUT)
p16 = Pin(13, Pin.OUT)

listLED = [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14, p15, p16]

# Main loop (unchanged logic)
while True:
    numLED = random.randint(6, 10)
    print(numLED)

    # Choose unique pins
    activeLED = []
    for n in range(numLED):
        LEDchoice = random.choice(listLED)
        if LEDchoice not in activeLED:
            activeLED.append(LEDchoice)
            print(LEDchoice)
        else:
            while LEDchoice in activeLED:
                LEDchoice = random.choice(listLED)
            activeLED.append(LEDchoice)

    seconds = random.randint(300, 400)
    print(seconds)

    for v in activeLED:
        v.value(1)

    time.sleep_ms(seconds)

    for v in activeLED:
        v.value(0)