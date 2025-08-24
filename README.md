# Physical Interface with Raspi Pico and MIDI System

General, educational examples for building modular physical interfaces with Raspberry Pi Pico.
These scripts demonstrate:
- Reading inputs (buttons, switches, potentiometers)
- Driving indicator lights / light panels
- UART messaging between multiple microcontrollers
- Converting messages to USB-MIDI for use with host software (DAWs/VJ tools)

> **NDA Safety:** This repository is intentionally generic. It does not reference or
> reveal any proprietary systems, brand names, or third-party IP. All code and
> diagrams are provided solely as educational examples.

## Modules

- **`radio.py`** — Reads three potentiometers and three buttons; reports values via UART.
- **`pilot.py`** — Drives left/right banks of GPIO lights in response to two switches; reports events via UART.
- **`navigation.py`** — Demonstrates keypad + four switches, visual feedback, and simple 4-key code matching with UART reporting.
- **`rand_lights.py`** — (MicroPython) Randomized light panel controller for GPIO-connected LEDs.
- **`master.py`** — Central controller that reads UART from multiple modules and outputs USB-MIDI Note/CC events.

## Getting Started

1. **Install firmware**
   - CircuitPython for `radio.py`, `pilot.py`, `navigation.py`, and `master.py`.
   - MicroPython for `rand_lights.py`.

2. **Libraries (CircuitPython)**
   - `adafruit_midi`
   - `usb_midi` (built-in on CircuitPython with USB support)
   - For the navigation example: appropriate Adafruit Trellis library (as referenced in the script).

3. **Wiring (UART)**
   - Share GND between devices.
   - Connect TX of a module to RX of the master (and vice-versa when needed).
   - Configure pins as shown in each script.

4. **Running**
   - Copy a module file to a Pico as `code.py` (or import as a module if you prefer).
   - For `master.py`, connect the Pico to a computer via USB; it will appear as a MIDI device.

## Message Format

Modules send newline-terminated strings such as:

Radio:Pot1:32768
Radio:back:1
Pilot:LEngineSwitchOn
Navi:Code:[0, 1, 2, 3]

The master parses these messages and emits corresponding MIDI Note/CC events.

## Notes

- Pin assignments, timings, and mappings are examples you can customize.
- The repository intentionally avoids any references to non-public systems or projects.
- Use at your own discretion and test thoroughly in your environment.

## License

MIT License — suitable for personal/educational use.
