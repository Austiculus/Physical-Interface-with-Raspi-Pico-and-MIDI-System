"""
Master MIDI Converter Example
-----------------------------------------------------------

Purpose:
- Act as a central controller on a Raspberry Pi Pico (CircuitPython).
- Read delimited messages from multiple UART buses.
- Convert messages into USB-MIDI Note/CC events for a host computer.

Notes:
- This is a generic educational template and does not reference any proprietary
  projects, software titles, or third-party IP.
- Compatible with DAWs/VJ software that accept standard USB-MIDI.

Author: Austin Zercher
Date: 2025

Dependencies:
- CircuitPython with USB MIDI support
- adafruit_midi
-----------------------------------------------------------
"""

import time
import board
import busio

import usb_midi
import adafruit_midi
from adafruit_midi.control_change import ControlChange
from adafruit_midi.note_off import NoteOff
from adafruit_midi.note_on import NoteOn

# MIDI channel assignments (unchanged)
channels = {
    "Navi": 0,
    "Pilot": 1,
    "Radio": 2
}

# MIDI note mappings (unchanged)
naviMidiNotes = {
    "Button1": 1,
    "Button2": 2,
    "Button3": 3,
    "Button4": 4,
    "Code1": 11,
    "Code2": 12,
    "Code3": 13,
    "Code4": 14
}

pilotMidiNotes = {
    "LEngineSwitchOn": 1,
    "REngineSwitchOn": 2,
    "LEngineSwitchOff": 3,
    "REngineSwitchOff": 4
}

radioMidiNotes = {
    "Back": 1,
    "Pause": 2,
    "Skip": 3
}

# Setup MIDI I/O (unchanged)
midi = adafruit_midi.MIDI(
    midi_in=usb_midi.ports[0],
    midi_out=usb_midi.ports[1],
    in_channel=0,
    out_channel=0
)

# Setup UART buses (unchanged)
bus0 = busio.UART(board.GP0, board.GP1, 9600, timeout=0.1)  # Pilot + Radio
bus1 = busio.UART(board.GP4, board.GP5, 9600, timeout=0.1)  # Navi

buffer0 = b""
buffer1 = b""
updateGap = 0.1
timeUpdate = time.monotonic()

# Main loop (unchanged logic)
while True:
    now = time.monotonic()
    if now - timeUpdate >= updateGap:
        timeUpdate = now

        data0 = bus0.read(32)
        data1 = bus1.read(32)

        if data0:
            buffer0 += data0
        if data1:
            buffer1 += data1

        # ---------- Pilot & Radio ----------
        if b"\n" in buffer0:
            lines = buffer0.split(b"\n")
            buffer0 = lines[-1]  # Keep the incomplete line
            for line in lines[:-1]:
                command = line.decode().strip()
                print(command)
                # Pilot commands
                if command.startswith("Pilot:"):
                    cmd = command.replace("Pilot:", "")
                    if cmd in pilotMidiNotes:
                        note = pilotMidiNotes[cmd]
                        midi.send(NoteOn(note, 120, channel=channels["Pilot"]))
                    elif cmd.startswith("Thrst:"):
                        try:
                            value = int(cmd.replace("Thrst:", ""))
                            midi.send(ControlChange(1, value, channel=channels["Pilot"]))
                        except ValueError:
                            print("Invalid Pilot Thrust:", cmd)

                # Radio commands
                elif command.startswith("Radio:"):
                    cmd = command.replace("Radio:", "")
                    if cmd in radioMidiNotes:
                        note = radioMidiNotes[cmd]
                        midi.send(NoteOn(note, 120, channel=channels["Radio"]))
                    elif cmd.startswith("Pot"):
                        try:
                            pot_num = int(cmd[3])
                            value = int(cmd.split(":")[1])
                            midi.send(ControlChange(pot_num, value, channel=channels["Radio"]))
                        except (IndexError, ValueError):
                            print("Invalid Radio Pot:", cmd)

        # ---------- Navigation ----------
        if b"\n" in buffer1:
            lines = buffer1.split(b"\n")
            buffer1 = lines[-1]
            for line in lines[:-1]:
                command = line.decode().strip()
                if command.startswith("Navi:"):
                    cmd = command.replace("Navi:", "")
                    if cmd in naviMidiNotes:
                        note = naviMidiNotes[cmd]
                        midi.send(NoteOn(note, 120, channel=channels["Navi"]))